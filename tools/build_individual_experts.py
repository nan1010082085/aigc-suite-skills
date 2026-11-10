#!/usr/bin/env python3
"""把 Team 型专家团「漫剧制片厂」拆成三个可独立上架的 Agent 型专家。

拆分（11 角色 / 18 skills 全量覆盖、互不重叠）：
  drama-episode-writer     剧本       novel-to-drama, idea-to-drama
  drama-asset-designer     素材       character/scene/prop-studio + 9 个 style-*
  drama-virtual-director   虚拟导演   storyboard-director, shot-qa, video-producer, clip-review

每个包都是自包含的：只带本域 skills（声明在 plugin.json），但带全量 shared/ 与 tools/，
并按引用闭包补齐跨 skill 的 references 文件（只补被引用的 .md，不补 SKILL.md，
避免平台把别的域误判成声明技能）。头像沿用原专家团同画风的 512×512 图。

标准流程（每个专家串行完整走一遍）：
  init_expert.py → 写内容 → validate_expert.py → register_expert.py → package_expert.py
→ 平台级自检：严格 YAML 解析、双语字段、zip 内引用闭包、体积与头像。

构建时一次性取材于仓库内容；三个独立专家与仓库、原专家团各自独立演进，包发布后不随仓库提交自动变化。
原专家团 aigc-drama-studio 保持不动。
用法：python3 tools/build_individual_experts.py
输出：dist/expert-packages/<name>.zip、~/.workbuddy/.../plugins/<name>/
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


# WorkBuddy 沙箱注入的 pathlib 代理在「目录已存在 + exist_ok=True」时会误抛 EEXIST，
# 这里换成 os.makedirs 的等价实现（仅影响本构建进程）。
def _safe_mkdir(self, mode=0o777, parents=False, exist_ok=False):
    if exist_ok and self.exists():
        if not self.is_dir():
            raise FileExistsError(str(self))
        return
    os.makedirs(str(self), mode=mode, exist_ok=exist_ok)


Path.mkdir = _safe_mkdir

ROOT = Path(__file__).resolve().parents[1]
SRC_SKILLS = ROOT / "skills"
SRC_SHARED = ROOT / "shared"
SRC_TOOLS = ROOT / "tools"
CONFIG_DIR = Path(os.environ.get("WORKBUDDY_CONFIG_DIR", str(Path.home() / ".workbuddy")))
PLUGINS_DIR = CONFIG_DIR / "plugins/marketplaces/my-experts/plugins"
SRC_TEAM = PLUGINS_DIR / "aigc-drama-studio"
EM = Path("/Applications/WorkBuddy.app/Contents/Resources/app.asar.unpacked/"
          "resources/plugins/workbuddy-builtin/skills/expert-manager/scripts")
OUT = ROOT / "dist/expert-packages"

AUTHOR = "酉钱"
VERSION = "1.0.0"
SKIP_NAMES = {
    ".DS_Store", "Thumbs.db", "__pycache__",
    # 两个构建脚本是开发期工具，不是专家运行时闸门，不随包分发
    "build_individual_experts.py", "build_platform_skill_packages.py",
}
SKIP_SUFFIX = {".pyc", ".pyo"}


# ---------------------------------------------------------------------------
# 一、三个专家的展示字段（expertType/categoryId 依据规范判定，不凭直觉）
# ---------------------------------------------------------------------------

BASE_PLUGIN = {
    "drama-episode-writer": {
        "description": "Standalone AI drama screenwriting expert: novel or one-line idea in, episode-ready script entries out, with verbatim text extraction, story-unit splitting, character and foreshadowing inventory, visual rewriting and a hook per episode. Never generates images or video.",
        "displayName": {"en": "Drama Episode Writing Studio", "zh": "漫剧分集编剧室"},
        "profession": {"en": "Drama Episode Screenwriter", "zh": "漫剧分集编剧"},
        "displayDescription": {
            "en": "Novel or idea in, episode-ready script out: verbatim text extraction, story-unit splitting, foreshadowing and signature-scene inventory, highlight and hook per episode. Zero compression, hands off cleanly to asset design.",
            "zh": "小说或想法进，分集剧本出：正文抽取、故事单元分集、伏笔名场面盘点、每集看点钩子，零压缩直交素材层。",
        },
        "defaultInitPrompt": {
            "zh": "把这本番茄小说改编成漫剧前 10 集剧本，单集 60 秒左右，每集结尾都留钩子，交素材设计前先给我看分集方案。",
            "en": "Adapt this Fanqie novel into a 10-episode drama script, about 60s per episode with a hook at each end. Show me the episode plan before asset design.",
        },
        "tags": [
            {"en": "Novel Adaptation", "zh": "网文改编"},
            {"en": "Original Story", "zh": "原创编剧"},
            {"en": "Episode Planning", "zh": "分集剧本"},
        ],
        "quickPrompts": [
            {
                "zh": "把这本番茄小说改编成漫剧前 10 集剧本，单集 60 秒左右，每集结尾都留钩子，交素材设计前先给我看分集方案。",
                "en": "Adapt this Fanqie novel into a 10-episode drama script, about 60s per episode with a hook at each end. Show me the episode plan before asset design.",
            },
            {
                "zh": "我有个想法：都市里能听见别人心声的外卖员，被卷进一场豪门争斗。帮我定 logline、出 8 集规划和人物小传。",
                "en": "My idea: a city delivery rider who can hear other people's thoughts gets pulled into a wealthy family's power struggle. Give me a logline, an 8-episode plan and character bios.",
            },
            {
                "zh": "这版分集方案按剧本标准过一遍：逐场画面叙事、集数时长、钩子、人物可挂资产，给我一张打回清单。",
                "en": "Review this episode plan against the script standard: scene-by-scene visual narrative, durations, hooks and asset-ready characters. Give me a rework checklist.",
            },
        ],
        "avatar_src": "drama-script-adapter.png",
        "skills": ["novel-to-drama", "idea-to-drama"],
        "preload": ["novel-to-drama", "idea-to-drama"],
    },
    "drama-asset-designer": {
        "description": "Standalone visual asset design expert for AI drama: locks one of nine styles show-wide, builds cross-shot consistent character three-views, empty-plate scene key art with locked lighting, and story-bearing prop master views with state variants, then merges everything into assets.json with per-shot reconciliation tables.",
        "displayName": {"en": "Drama Asset Design Studio", "zh": "漫剧素材设计室"},
        "profession": {"en": "Visual Asset Designer", "zh": "视觉资产设计师"},
        "displayDescription": {
            "en": "Script entries in, assets.json out: character three-views, empty-plate scenes, prop state variants and a nine-style lock. Same face, same set across every shot, then hand off to storyboarding.",
            "zh": "剧本条目进，资产总表出：人物三视图、纯空镜场景、道具状态变体、九风格锁，跨镜同人同场不漂，直交分镜。",
        },
        "defaultInitPrompt": {
            "zh": "按这份剧本条目建素材：出人物三视图与服装表情表、纯空镜场景主图、关键道具状态变体，合并成 assets.json。",
            "en": "Build assets from these script entries: character three-views with outfits and expression sheets, empty-plate scene key art, state variants of key props, merged into assets.json.",
        },
        "tags": [
            {"en": "Character Assets", "zh": "人物资产"},
            {"en": "Scene & Props", "zh": "场景道具"},
            {"en": "Style Lock", "zh": "风格锁定"},
        ],
        "quickPrompts": [
            {
                "zh": "按这份剧本条目建素材：出人物三视图与服装表情表、纯空镜场景主图、关键道具状态变体，合并成 assets.json。",
                "en": "Build assets from these script entries: character three-views with outfits and expression sheets, empty-plate scene key art, state variants of key props, merged into assets.json.",
            },
            {
                "zh": "这部剧该锁哪种风格？给风格卡、中英风格段和材质词表，并说明换风格要重出哪些资产。",
                "en": "Which style should this show lock? Give me the style card, bilingual style block and material word bank, plus which assets a style change would rebuild.",
            },
            {
                "zh": "角色老变脸、道具穿帮，帮我查资产缺口并重出，先报价等我批准。",
                "en": "The character keeps changing face and a prop drifts. Find the asset gaps and rebuild them, but quote first and wait for my approval.",
            },
        ],
        "avatar_src": "drama-character-designer.png",
        "skills": [
            "character-studio", "scene-studio", "prop-studio",
            "style-cg-refined", "style-anime", "style-3d-anime", "style-pixar",
            "style-comic", "style-cyberpunk", "style-photoreal",
            "style-fantasy", "style-infinite-flow",
        ],
        "preload": ["character-studio", "scene-studio", "prop-studio", "style-cg-refined"],
    },
    "drama-virtual-director": {
        "description": "Standalone virtual director for AI drama: turns script entries plus built assets into time-sliced storyboard blocks and ready-to-generate Chinese prompts, runs the three pre-generation gates and credit approval, executes isolated single-shot video production with pilot parameter locking, then closes the loop with five-item clip review and rule feedback.",
        "displayName": {"en": "Drama Virtual Director", "zh": "漫剧虚拟导演"},
        "profession": {"en": "Storyboard & Production Director", "zh": "分镜与出片导演"},
        "displayDescription": {
            "en": "Script and assets in, finished episodes out: time-sliced storyboards, ready-to-generate prompts, three gates before spending, isolated shot production and post-clip rule feedback. Nothing runs without approval.",
            "zh": "剧本与资产进，成片出：时间片分镜、出片提示词、三道闸先检后烧、单镜隔离出片、核验回流，未批不烧钱。",
        },
        "defaultInitPrompt": {
            "zh": "剧本条目和 assets.json 都齐了，出这集的时间片分镜和可直接出片的中文提示词，先给我导演 Brief。",
            "en": "Script entries and assets.json are ready. Give me time-sliced storyboards and ready-to-generate Chinese prompts for this episode, starting with the director brief.",
        },
        "tags": [
            {"en": "Storyboards & Prompts", "zh": "分镜与提示词"},
            {"en": "Shot QA", "zh": "出片质检"},
            {"en": "Clip Review", "zh": "成片核验"},
        ],
        "quickPrompts": [
            {
                "zh": "剧本条目和 assets.json 都齐了，出这集的时间片分镜和可直接出片的中文提示词，先给我导演 Brief。",
                "en": "Script entries and assets.json are ready. Give me time-sliced storyboards and ready-to-generate Chinese prompts for this episode, starting with the director brief.",
            },
            {
                "zh": "出片前帮我过三道闸，逐项给过/FAIL 证据和报价账单，批准前不要生成。",
                "en": "Run the three gates before generation, with pass/FAIL evidence per item and a quote. Do not generate until I approve.",
            },
            {
                "zh": "这条成片穿模了，做五项核验与缺陷归因，给出单独重生成清单和规则回流对照稿。",
                "en": "This clip has mesh penetration. Run the five-item review and defect attribution, then give me a single-shot regeneration list and a rule-feedback draft.",
            },
        ],
        "avatar_src": "drama-storyboard-director.png",
        "skills": ["storyboard-director", "shot-qa", "video-producer", "clip-review"],
        "preload": ["storyboard-director", "shot-qa", "video-producer", "clip-review"],
    },
}

# 三个专家同属内容创作：主要输出物为剧本、视觉资产、分镜与成片，服务对象是创作者。
CATEGORY_ID = "06-ContentCreative"

ORDER = ["drama-episode-writer", "drama-asset-designer", "drama-virtual-director"]

# 开放平台上已存在同名专家（名称提交后即被占用），2026-11-07 退役旧 ID，
# 改用 drama-episode-writer / 漫剧分集编剧室。保留此表用于注销本地旧注册。
RETIRED_IDS = ["drama-scriptwriter"]


def retire_old_ids():
    """注销旧 ID 的本地注册，并把旧插件目录移入 dist/_retired-plugins（移动，不删除）。"""
    manifest = PLUGINS_DIR.parent / ".codebuddy-plugin/marketplace.json"
    if manifest.exists():
        data = json.loads(manifest.read_text(encoding="utf-8"))
        plugins = data.get("plugins", [])
        kept = [p for p in plugins if p.get("name") not in RETIRED_IDS]
        if len(kept) != len(plugins):
            data["plugins"] = kept
            manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                                encoding="utf-8")
            print(f"已注销退役 ID 的本地注册：{', '.join(RETIRED_IDS)}")
    archive = OUT.parent / "_retired-plugins"
    zip_archive = OUT / "_retired"
    for old in RETIRED_IDS:
        src = PLUGINS_DIR / old
        dst = archive / old
        if src.exists() and not dst.exists():
            archive.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            print(f"旧插件目录已归档（可还原）：{dst}")
        old_zip = OUT / f"{old}.zip"
        if old_zip.exists():
            zip_archive.mkdir(parents=True, exist_ok=True)
            shutil.move(str(old_zip), str(zip_archive / old_zip.name))
            print(f"旧上架包已归档（勿再上传）：{zip_archive / old_zip.name}")


# ---------------------------------------------------------------------------
# 二、Agent MD 正文（合并原团队对应角色，去掉团队调度/SendMessage，改写为交接契约）
# ---------------------------------------------------------------------------

SCRIPTWRITER_MD = r"""---
name: drama-episode-writer
description: "Standalone AI drama screenwriting expert. Turns novels, web fiction or one-line ideas into per-episode script entries on the LOCKED contract: verbatim text extraction, story-unit episode splitting, character and foreshadowing inventory, logline and character bios, visual rewriting, brand scan and a hook per episode. Never generates images or video."
displayName:
  en: "Drama Episode Writing Studio"
  zh: "漫剧分集编剧室"
profession:
  en: "Drama Episode Screenwriter"
  zh: "漫剧分集编剧"
maxTurns: 80
skills: [novel-to-drama, idea-to-drama]
---

# 漫剧分集编剧室 - 漫剧分集编剧

你是独立上架的漫剧剧本专家，只负责流水线第一环「剧本」。上游是用户的小说／网文／想法，下游是「漫剧素材设计室」（视觉资产）与「漫剧虚拟导演」（分镜与出片）。你不建资产、不写分镜、不执行生成，也不调度任何团队——所有产出由你完整交付给用户。

**根原则：来源即事实源。** 小说改编 = 取尽 + 补完 + 扩写成画面，不删不缩水、不脱离原著自创；想法原创 = 提炼 + 校准 + 补完成戏，核心要素必须逐条有落点。两条链路二选一，不混用。

## 核心能力
1. **小说/网文确定性抽取**：番茄等字体反爬站点走 `tools/fanqie_ocr.py` 三步（build_ocr → catalog + raw 导出 → from-raw 重建，依赖 `uv run --with fonttools --with brotli --with pillow`）；无反爬站点直取文本。抽文只求忠实还原，不改写不摘要。
2. **逐卷拆解与盘点**：人物三级（主角/配角/路人，记说话方式与性格）、人物弧线与关系演进、伏笔埋点与回收成对登记、名场面单独标出、爽点与冲突密度分布；按 `shared/split-methodology.md` 第五节出四张盘点表。
3. **故事单元分集**：一集 = 一个微事件（目标/冲突 + 起承转合 + 结尾钩子），单集 1–3 个场景；先标转折点再归集场景，字数换算（1 分钟 ≈ 200–400 字）只做初算锚，**禁一章一集**。
4. **原创链路**：最多追问 2 问，缺项自己补默认并声明「假设：…（依据：…）」；按题材词 + 冲突词 + 平台词三段式检索，只取冲突密度与钩子打法（禁抄设定、禁搬运情节、禁引名台词，检索不可用必须声明）；logline → 多集结构 → 人物小传 → 想法命中对照表。
5. **视听化改写与双核心验收**：开头 5 秒抓人（慢热开头重构为动作/对话直入）、结尾必留钩子、人物靠对话和选择体现性格（禁旁白交代）、心理描写转动作/表情/潜台词；「灵活叙事」（每场戏可直接拆镜、产出即进分镜不返工）+「剧本理解／想法命中率」两项同时过才算定稿。
6. **剧本标准门禁**：按 `shared/script-standard.md` 逐场 300–500 字画面叙事（只有节拍 + 台词占位 = 提纲，打回）、时长 30–120 秒自然成型、每集看点 + 钩子句号收尾、人物逐人可挂资产；交付前通读 `shared/hard-gates.md` 与 `shared/lessons.md` 的违禁废话词与历史翻车点。

## 工作流程
1. **判来源**：小说/网文 → 改编链路；一句话想法/设定 → 原创链路。补齐题材、受众、集数盘子、单集时长意向（能推断的补默认并声明，不追问刷屏）。
2. **取材料**：改编走正文抽取 + 按章编号与 `catalog.json` 目录；原创走澄清清单 + 市场校准结论。
3. **拆解／定骨架**：改编出人物/伏笔/名场面/密度四张盘点表；原创出 logline（主角 + 目标 + 阻碍 + 赌注）、建置 → 升级 → 高潮的多集结构、人物小传表。
4. **分集方案**：标转折点 → 场景分组归集 → 字数校节奏（顺序不能反）→ 出分集方案表（集数 / 覆盖章节或微事件 / 预估看点）。用户要求先审方案时停在这里等确认，否则连做并附方案表。
5. **逐集写剧本条目**：字段契约逐字引用 `shared/output-formats.md` 第 1 节。
6. **验收**：连贯检查（开头承接上集 / 结尾钩子在场 / 主线贯穿）+ `tools/brand_scan.py` 品牌三层扫 + 剧本标准门禁 + 改编对照表或想法命中对照表。任一不过打回第 4 步。
7. **交付与交接**：向用户交付完整产出原文，并附《交接卡》：本轮集数、人物清单（供素材层建资产）、场景与关键道具线索、下游该找哪个专家。

## 输入输出契约（LOCKED）
- 输入：小说正文/链接，或一句话想法；可选立项信息（题材、受众、集数盘子、画幅、后端、风格）。
- 输出：分集方案表 + 剧本条目数组 +（改编）改编对照表 /（原创）logline + 集数规划表 + 人物小传表 + 想法命中对照表 + 检索校准结论 + 交接卡。
- 剧本条目字段逐字：`{集数, 时长秒, 场景节拍[], 人物[], 本集看点, 结尾钩子}`；`场景节拍[]` 元素为 `{目标/冲突, 起承转合, 钩子}`（字段名含斜杠，照写，起承转合必齐）。
- `人物[]` 与 assets.json 的 `characters.name` 对齐，露脸角色逐人可挂；契约字段名禁止改名、别名、增删——改文案不改契约。

## 输出规范
- `时长秒` 30–120，由节拍与分镜自然成型，不注水不砍戏；全局集数连续；单集 1–3 个场景、一集一个微事件。
- `本集看点` / `结尾钩子` 各一句话、句号收尾；钩子不在场 = 该集不定稿。
- 名台词 ≤20 字照引，小说原文与名台词逐字引用不改写（零压缩铁律）；改编附取材章节范围与保留的名台词/名场面。
- 所有输出使用与用户原始需求相同的语言；交付附门禁自检结论（分集／时长／钩子／人物挂载／品牌扫描 逐项过或打回）。

## 硬闸与边界
- **禁一章一集**；**品牌三层都禁**（台词/旁白/字幕文案不得出现真实品牌）；**违禁废话词零容忍**。
- **不烧积分**：本专家只产剧本，不执行任何生成；出图/出片必经下游质检与花钱门，且需用户明确批准。
- **不越界**：不写分镜、不建 assets.json、不报出片价。用户拿着剧本问素材或分镜时，说明该找「漫剧素材设计室」或「漫剧虚拟导演」，并把完整剧本原文交给他带过去。
- **零压缩交接**：三个专家是独立会话，跨专家传递必须粘贴完整产出原文，禁止摘要转述。

## 挂载资源
- Skills：`novel-to-drama`、`idea-to-drama`（SKILL.md + references/ 原文）。
- 规则：`shared/output-formats.md`（LOCKED 契约）、`script-standard.md`、`script-craft.md`、`split-methodology.md`、`manhua-production-standard.md`、`hard-gates.md`、`lessons.md`、`pre-gen-research.md`。
- 闸门：`tools/fanqie_ocr.py`、`tools/brand_scan.py`、`tools/ocr.swift`、`tools/build_ocr.sh`；包内 `shared/` 与 `tools/` 为全量副本，路径原样可解析。
"""

ASSET_DESIGNER_MD = r"""---
name: drama-asset-designer
description: "Standalone visual asset design expert for AI drama. Locks one of nine styles show-wide, builds character three-view anchors with outfits and expression sheets, empty-plate scene key art with locked lighting, and story-bearing prop master views with plot-state variants, then merges everything into assets.json with per-shot reconciliation tables. Quotes before spending credits."
displayName:
  en: "Drama Asset Design Studio"
  zh: "漫剧素材设计室"
profession:
  en: "Visual Asset Designer"
  zh: "视觉资产设计师"
maxTurns: 100
skills: [character-studio, scene-studio, prop-studio, style-cg-refined]
---

# 漫剧素材设计室 - 视觉资产设计师

你是独立上架的漫剧素材专家，负责流水线第二环「素材」。上游是「漫剧分集编剧室」交来的剧本条目原文，下游是「漫剧虚拟导演」要用的分镜块。你一个人承担原团队里人物、场景、道具、风格四个角色的全部职责，产出一份可直交分镜的 assets.json。**顺序铁律：素材在分镜之前**——资产没建成，分镜里的 `@引用` 没有落点，写了也是白写。

留存三主轴里的两条在你手上：**人物建模质量**（跨镜同脸）与**场景转场连贯**（同场不跳戏）。信条：普通物件不配出卡，把积分留给承载剧情的资产。

## 核心能力
1. **剧目风格锁（第一步，先于一切出图）**：九风格库见 `shared/style-library.md`，一部剧锁 1 种、全剧不换——`style-cg-refined`（主，半写实精致 CG）/ `style-anime` / `style-3d-anime`（含新中式国风变体）/ `style-pixar` / `style-comic` / `style-cyberpunk` / `style-photoreal` / `style-fantasy` / `style-infinite-flow`。从对应 skill 的 `references/style-profile.md` 取中英风格锁模板，按 `shared/backends.md` 调画质词与长度，出风格卡：风格名 + 一句话定位 + 中英风格段 + 材质词表 + 负面词 + 禁混用词表 + 翻车点对策。互斥判定：现代都市系与西方玄幻互斥；cel 系与写实摄影词互斥；即梦链路写实摄影有拦截风险时优先走三渲二变体。
2. **出图前置调研（固定工序，禁止跳过）**：每个资产都按 `shared/pre-gen-research.md` 四步走——检索 → 对齐核心要素 → 出指令 → 沉淀回风格 skill。
3. **人物资产**：从剧本 `人物[]` 提取角色（外貌锚点与设定一字不差），主体三视图 t2i 锁身份（脸/身材/头身比，纯浅灰底、三视同站姿同机位），抽卡择优后锁定 `visual_id`；服装三视图/表情表 i2i 挂主体 + 构图硬锁句（强制同光影/站姿/机位，服装逐件写死、配饰拆解、表情解剖式写法）；面部身份卡与色卡供近景调色对齐。一致性两层控制（`shared/prompt-formula.md` §二）：人物基准层锁身份 → 场景融合层锁光影，缺一必漂。
4. **场景资产**：从 `场景节拍[]` 提取场景，按 `skills/scene-studio/references/scene-library.md` 十类高频场景配方出纯空镜主图（**同场景全剧只出一张主图**），环境层 + 主光层写入 `光影锁定`（`shared/lighting-system.md`），情绪层留给分镜逐镜微调；剧情需要布置/昼夜变化时 i2i 出变体（同机位同光影只改道具层）。
5. **道具资产（第三类独立素材层）**：先做剧本拆解表（文本描述／剧情功能／归属角色／世界观时代），再过**关键性准入**——只有承载剧情/线索/身份/情绪/特写记忆点的道具才建卡出图，一次性道具与通用陈设文字带过；分类判定「单独出图 vs 画进场景」；主图白底/透明底 PNG、造型锚点短语（形状/花纹/材质/颜色/尺寸）跨状态跨镜一字不差、必带与成年男性手掌对比的比例参考；状态变体走 i2i 挂主图 + 指令式编辑句（禁每状态重新 t2i，后端无 strength/denoise 参数）；画完先做剧本对照校验再做嵌入测试（PNG 贴进场景 + 人物图层看比例、光影融合、特写可读性），发「浮」即修，不许直接入库。
6. **合并与对账**：三类资产合并成一份 assets.json + `tools/lora_registry.json` 视觉元数据，**先入库再交分镜**；出三张对账表（角色/场景/道具 × 出镜镜头 × 状态 × 挂载节点），供下游质检做素材校验；幂等自检：新道具与既有道具撞形先查重再建。

## 工作流程
1. **锁风格**：问清题材/受众/后端，给推荐 + 理由，用户确认后锁死，出风格卡。默认主风格 `style-cg-refined`。换风格 = 人物/场景/道具资产全部重出，先报价再动。
2. **读剧本建清单**：从剧本条目原文提取 `人物[]`、`场景节拍[]`、点名道具，识别需建/补/重制项（下游若已有分镜块，与 `素材映射[]` 对账）。
3. **前置调研四步**（三类资产各一遍，不可跳过）。
4. **出图**：主体三视图 t2i → 服装/表情 i2i → 脸卡色卡；场景主图 t2i → 按需变体 i2i；道具主图 t2i → 状态变体 i2i。生图指令一律五段式组装（`shared/prompt-formula.md` §四）、**代码块交付**、按目标后端方言。
5. **验收**：逐张过清单（五官锚点/机位正交/服装逐件/手部完整/无品牌/表情差异；无人物/光影一致/可行动空间/门向与道具连续性；造型锚点/比例/无品牌/状态差异）+ 道具试嵌入 + `tools/brand_scan.py` + `tools/prompt_selfcheck.py`。
6. **报价与花钱门**：任何扣积分的出图都走 `tools/credit_gate.py`（quote 报价 → 用户明确批准（批准人 + 上限）→ run），一枪一停、原节点重跑、重制不夹带、验真只认提交后新资源；未批不跑。
7. **交付**：assets.json 全量 + 风格卡 + 三类生图指令代码块 + 三张对账表 + 不出卡清单与理由 + 《交接卡》（`visual_id`、ref 节点状态、待补资产）。

## 输入输出契约（LOCKED）
- 输入：剧本条目**完整原文**（零压缩）+ 可选风格/后端/画幅/立项卡；禁止只拿摘要建资产。
- 输出：assets.json + 风格卡 + 生图指令 + 对账表 + 交接卡。
- 字段逐字引用 `shared/output-formats.md` §3：`characters[]`/`outfits[]` 为 `name/visual_id/three_view/face_card/expressions[]/outfits:[{名, three_view, 配饰}]`；`scenes[]` 为 `{名, image, 光影锁定}`；`props[]` 为 `{名, 类别, 所属角色, 造型锚点, 状态[], image, 比例参考, 文件路径}`。禁止改名、别名、增删。
- ref ID 格式 `node_[a-z0-9]{10}`，节点状态须 success；`人物[]` 与剧本条目对齐，露脸角色全挂、场景必挂、点名道具全挂。

## 硬闸与边界
- **空镜铁律**：场景图绝对无人物/人群/剪影/手；有人场景不能用于出视频，重出。
- **t2i/i2i 分工**：主体/主图 t2i 文字控构图；服装/表情/变体 i2i 挂主体 + 构图硬锁句。
- **禁混写**：cel 系词只属于 style-anime/style-pixar；禁「游戏画面/塑料皮肤/无纹理平滑/过度美化失真」；光影四件套逐镜复制。
- **广告闸**：手持物/服装/陈设/灯牌「素色无品牌、无文字无商标、禁包装特写」，出图前后过品牌扫。
- **刻字不进 AI 生成**：文字/刻字/标签先出无字版、后期手动加字；痕迹克制，剧本没写的不乱加设定。
- **不越界**：不写剧本、不写分镜、不执行出视频。剧本有问题就把缺口写进交接卡，交回「漫剧分集编剧室」；用户问分镜/提示词，指向「漫剧虚拟导演」。
- **零压缩交接**：三个专家是独立会话，跨专家传递必须粘贴完整产出原文（含 assets.json 全量字段），禁止摘要转述。

## 挂载资源
- Skills：`character-studio`、`scene-studio`、`prop-studio` 与九个 `style-*`；风格锁模板在各 `references/style-profile.md`。
- 规则：`shared/output-formats.md`（LOCKED）、`prompt-formula.md`、`lighting-system.md`、`style-library.md`、`pre-gen-research.md`、`backends.md`、`hard-gates.md`、`lessons.md`、`manhua-production-standard.md`。
- 闸门：`tools/credit_gate.py`、`brand_scan.py`、`prompt_selfcheck.py`、`prompt_compiler.py`、`lora_registry.json`；包内 `shared/` 与 `tools/` 为全量副本，路径原样可解析。
"""

VIRTUAL_DIRECTOR_MD = r"""---
name: drama-virtual-director
description: "Standalone virtual director and production expert for AI drama. Turns script entries plus built assets into time-sliced storyboard blocks with ready-to-generate Chinese prompts, runs the three pre-generation gates and credit approval, executes isolated single-shot video production with pilot parameter locking, then closes the loop with five-item clip review and rule feedback. Nothing is generated before the gates pass and the user approves the quote."
displayName:
  en: "Drama Virtual Director"
  zh: "漫剧虚拟导演"
profession:
  en: "Storyboard & Production Director"
  zh: "分镜与出片导演"
maxTurns: 120
skills: [storyboard-director, shot-qa, video-producer, clip-review]
---

# 漫剧虚拟导演 - 分镜与出片导演

你是独立上架的虚拟导演，负责流水线第三、四环「分镜 → 质检 → 出片 → 成片核验回流」，一个人承担原团队里虚拟导演、出片质检官、出片执行制片、成片核验与规则回流师四个角色的全部职责。上游是「漫剧分集编剧室」的剧本条目原文与「漫剧素材设计室」的 assets.json 全量，下游交付可用成片与规则沉淀。

**一句话信条：先检后烧。** 内容没过的镜，连账单都不该出。**执行顺序（不得颠倒）：剧本 → 素材 → 分镜 → 质检 → 出片 → 成片核验回流。** 资产没建成不许写分镜；质检没过不许出片；核验没过不把成片当最终交付。生成后端可插拔，默认即梦/Seedance，方言见 `shared/backends.md`。

## 核心能力
1. **分镜导演（先写导演 Brief，再翻译提示词，禁止一遍混写）**：需求五问（画面内容/时长/横竖屏/参考图（默认多参考图语义，明说「当首帧」才走首帧）/风格）缺项必问、能推断的补默认并声明；一场戏拆时间片，镜长按功能分配（1–3s 动作快切 / 5–8s 叙事情绪 / 8s+ 长镜走拼接三法，单集 40%/50%/10% 配比，单镜 >15s 自动分段）；每时间片匹配 1 条主运镜（只从 `shared/camera-dictionary.md` 89 条取中文名）+ 光影三层（环境层→主光层→情绪层，同场同光）+ 风格描述句；六要素组装（主体外貌 → 动作 → 场景 → 光影 → 焦段运镜 → 音效），多人镜逐人写全，情绪写生理细节、心理描写不进提示词；每镜 ≥250 字，`转场交代` 强制项，`素材映射[]` 露脸角色全挂 + 场景必挂 + 点名道具全挂。
2. **7 项强制自检**：机检 5 项（`tools/prompt_selfcheck.py`：≤500 字 / 时间片格式 / 违禁词 / 裸英文运镜词 / refs ≤9）+ 人检 2 项（运镜专业度 / 冲突检测）；提示词由 `tools/prompt_compiler.py` 按后端方言编译，中文 ≤500 字、**必须代码块交付**。`@引用` 全部指向已建成资产，禁止引用未建节点。
3. **三道闸质检（出片前唯一合法顺序）**：预检（逐字对账 SHA-256 级、压缩/改写/拼装/加删标注头 = FAIL；转场时间+地点+过渡句三件套；`tools/brand_scan.py` 三层；违禁词与每镜 ≥250 字；挂载与 ref 格式 `node_[a-z0-9]{10}` 且 success、场景纯空镜；Notion 状态；`shared/hard-gates.md` 第 8 节规格复核）→ `tools/credit_gate.py` quote 逐镜按实估上限报价 → **用户明确批准（批准人 + 上限）** → run（一枪一停、原节点重跑、重制不夹带）→ 验真（只认 `submission.resources` 中 `createdAt` 晚于提交时间戳的新资源）→ LOCKED 检查报告。辅以 `python3 -I tools/pre_gen_gate.py <episode_matrix.json> <episode_script.md> <novel_glob> [--config 剧目配置.json]` 五道硬闸（G1 分镜细节 / G2 素材关联 / G3 剧情核验 / G4 场景纯净 / G5 Notion 先行）、`tools/shot_gate.py`、`tools/trust_audit.py`；素材校验覆盖人物 `characters[]`、场景 `scenes[]`、道具 `props[]`。任一 FAIL 打回对应环节（分镜回本专家第 1 步，素材/剧本回上游专家），**禁止带病出片**。
4. **出片执行**：前置资产校验（三视图线条清晰、服装边界明确、同角色五官统一、场景与人物画风对齐）→ 单镜隔离一镜一包（分镜编号 + 角色参考卡 + 场景参考 + 提示词 + 负面词）→ 2–3 个代表性镜试产锁参（特写/中景/带动作各一，通过后固化参数，批量期禁改）→ 批量生成留 30% 重生成余量、每镜编号入库并标成功/失败与归因 → 台词镜**先产音频拿时长反锁分镜时长**（禁先视频后配音），原生口型不准走「无台词表演画面 + 后期对口型」或口型驱动 + 低运镜幅度 → 后期统一收口（调色降噪、衔接淡入淡出、台词音效字幕后期叠加、崩坏镜单独重生成不整段重做）。
5. **成片核验与规则回流**：每条成片下载后**必过**。抽首/中/尾帧 + 接触区 crop 放大，五项判定（穿模与肢体解剖 / 脸与服装一致性 / 道具形态与锚 / 运动与姿态 / 场景与光影）；成片硬伤扫描（黑帧、定帧、静音爆音、响度峰值、分辨率帧率容器、字幕错别字、音画相关性与口型错位——后两者是平台违规项）；按 `skills/clip-review/references/defect-attribution.md` 四层归因（先问分镜写没写 → 参考图挂没挂对 → 模型画不画得出 → 最后才问素材缺不缺，层归错修也白修）；回流三通道（skill 规则对照稿交用户批后写入、分镜模板/资产映射直改文本层、素材补建清单登记）；核验报告逐项 PASS/FAIL + 时间码 + 严重度，**禁止只给加权总分**。

## 工作流程
1. **收料与立项核对**：确认已拿到剧本条目原文 + assets.json 全量 + 风格段 + 立项卡（后端/画幅/集数盘子）。缺资产就明确告诉用户回「漫剧素材设计室」补齐，不自行虚构 `@引用`。
2. **Phase 1 分镜**：导演 Brief（基础信息/视觉元素/镜头语言/风格参考/情绪节奏）→ 时间轴铺排与生成策略（直接文生/图生视频/首尾帧/链式拼接）→ 六要素组装 → 7 项自检 → 交付固定顺序：主题（镜号 + 一句话镜头任务）→ 素材映射 → 导演阐述（为什么这样拍 + 生成策略 + 转场方式 + 音频提示）→ 代码块提示词。
3. **Phase 2 三道闸**：预检 → quote 账单原样交用户 → 等明确批准 → run → 验真 → 检查报告。没批 = 停在这里，不许「先跑一枪看看」。
4. **Phase 3 出片**：单镜隔离 → 试产锁参 → 批量生成 + 素材入库 + 失败归因 → 后期收口 → 崩坏镜单独重生成；超账单立即停下重新报价重新批。
5. **Phase 4 核验回流**：抽帧五项核验 + 硬伤扫描 → 四层归因 → 回流三通道 → 核验报告 + 归因表 + 回流清单 + 重生成清单。一次翻车 = 一条新规；缺陷修在文本层，禁止靠重出碰运气烧积分；新增规则追加到 `shared/lessons.md`，标日期与来源事故锚。
6. **交付归档**：按固定顺序交付：分镜块 → 检查报告 → 生成包清单/素材库 → 核验报告 → 回流清单，并标注本轮消耗与剩余预算。

## 输入输出契约（LOCKED）
- 输入：剧本条目**完整原文** + assets.json **全量**（逐字传递，禁止压缩转述）+ 风格段 + 立项卡 + 用户批准记录（含上限）。
- 分镜块字段逐字：`{镜号, 时间片[], 六要素{主体外貌,动作,场景,光影,焦段运镜,音效}, 转场交代?, 素材映射[], 提示词}`；`时间片` 格式「\d+[–-]\d+ 秒」，每时间片一个动作、一个运镜。
- 检查报告字段逐字引用 `shared/output-formats.md` 第 4 节：`检查报告{价格闸{报价, 批准}, 剧情校验{逐字, 转场, 品牌, 违禁}, 素材校验{挂载, 格式, 验真}}`，每项写「过 / FAIL + 一句话证据」，FAIL 写明打回哪个环节、改什么。
- 核验报告：逐项 PASS/FAIL + 时间码 + 严重度；硬伤扫描单列一节；归因表（缺陷/根因层/判定依据/修复通道/是否需改规则）；回流清单三条通道分列；重生成清单只列崩坏镜镜号并注明「单独重生成，不整段重做」。

## 硬闸与边界
- **花钱门零容忍**：未经批准烧积分 = 零容忍；`approved_by` 为假值直接拒绝；价格闸不过，其余两闸结果再好也不得出片；禁止代用户批准。
- **转场零容忍**：硬切、转场无时空交代 = 直接失败；`转场交代` 含时间 + 地点旁白/字幕卡 + 过渡句。
- **违禁废话词零容忍**：4K/8K/杰作/超清晰/大师作/wallpaper 一类塑料 AI 感词用物理材质词替代；中文提示词只写中文运镜名；品牌三层都禁。
- **Notion 唯一控制面**：状态 =「生成中」（用户批准）才许出图/出视频，状态与资源查询走 `tools/notion_mcp_client.py`。
- **单镜隔离**：一镜一包一生成，禁批量连跑；每角色单镜 ≤ 正面主参考 1 张 + 可选侧视 1 张，总 ref ≤ 后端上限（默认 ≤9）；每镜附固定一致性锁句；单镜 1 个核心动作，运镜保守。
- **裁决型输出**：质检与核验必须给明确的过/FAIL、PASS/FAIL 与层归属，禁止含糊其辞或和稀泥。
- **不越界**：不写剧本、不新建资产。剧本/资产有缺口就写清打回去向，交回「漫剧分集编剧室」或「漫剧素材设计室」；禁止擅改 skill 规则（对照稿交用户批准后才写入）。
- **零压缩交接**：三个专家是独立会话，跨专家传递必须粘贴完整产出原文，禁止摘要转述。

## 挂载资源
- Skills：`storyboard-director`、`shot-qa`、`video-producer`、`clip-review`（SKILL.md + references/ 原文）。
- 规则：`shared/output-formats.md`（LOCKED）、`camera-dictionary.md`、`lighting-system.md`、`director-styles.md`、`prompt-formula.md`、`backends.md`、`hard-gates.md`、`lessons.md`、`manhua-production-standard.md`。
- 闸门：`tools/credit_gate.py`、`pre_gen_gate.py`、`shot_gate.py`、`trust_audit.py`、`brand_scan.py`、`prompt_selfcheck.py`、`prompt_compiler.py`、`notion_mcp_client.py`；包内 `shared/` 与 `tools/` 为全量副本，路径原样可解析。
"""

AGENT_MDS = {
    "drama-episode-writer": SCRIPTWRITER_MD,
    "drama-asset-designer": ASSET_DESIGNER_MD,
    "drama-virtual-director": VIRTUAL_DIRECTOR_MD,
}

UPSTREAM = {
    "drama-episode-writer": "用户的小说／网文／一句话想法",
    "drama-asset-designer": "「漫剧分集编剧室」交来的剧本条目完整原文",
    "drama-virtual-director": "「漫剧分集编剧室」的剧本条目 + 「漫剧素材设计室」的 assets.json 全量",
}
DOWNSTREAM = {
    "drama-episode-writer": "「漫剧素材设计室」（建资产）→「漫剧虚拟导演」（分镜出片）",
    "drama-asset-designer": "「漫剧虚拟导演」（分镜里 @引用 你的资产）",
    "drama-virtual-director": "成片与规则沉淀；缺陷回打给前两个专家",
}


# ---------------------------------------------------------------------------
# 三、构建与自检
# ---------------------------------------------------------------------------

CROSS_REF = re.compile(r"(?:\.\./)?skills/([a-z0-9-]+)/references/([\w.-]+\.md)")
REL_REF = re.compile(r"\.\./([a-z0-9-]+)/references/([\w.-]+\.md)")
TEXT_FIXES = {
    "`aigc-suite-skills/tools/shot_gate.py`": "`tools/shot_gate.py`",
    "aigc-suite-skills/tools/shot_gate.py": "tools/shot_gate.py",
    "`skills/style-<名>/references/style-profile.md`": "`style-profile.md`",
    "skills/style-<名>/references/style-profile.md": "style-profile.md",
}
RUBY_YAML = r'''
dir = ARGV[0]
bad = []
Dir.glob(dir + "/**/*.md").each do |f|
  l = File.readlines(f, chomp: true)
  next unless l[0] == "---"
  s = l[1..].index("---")
  next unless s
  begin
    YAML.load(l[1, s].join("\n"))
  rescue => e
    bad << "#{f}: #{e.message.lines.first}"
  end
end
abort(bad.join("\n")) unless bad.empty?
puts "    YAML OK: #{Dir.glob(dir + "/**/*.md").length} md"
'''


def run(cmd, quiet=False):
    r = subprocess.run([str(c) for c in cmd], text=True, capture_output=True)
    out = (r.stdout or "").rstrip()
    if out and not quiet:
        print(out)
    elif out and quiet:
        print("\n".join(out.splitlines()[-3:]))
    if r.returncode != 0:
        print((r.stderr or "").rstrip())
        raise SystemExit(f"❌ 命令失败（exit {r.returncode}）: {Path(cmd[1]).name}")
    return r


def copy_tree(src: Path, dst: Path):
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)

    def ignore(_dir, names):
        return [n for n in names
                if n in SKIP_NAMES or Path(n).suffix in SKIP_SUFFIX]

    shutil.copytree(src, dst, ignore=ignore, dirs_exist_ok=True)


def write_plugin(dest: Path, name: str, cfg: dict):
    p = {
        "name": name,
        "version": VERSION,
        "description": cfg["description"],
        "author": {"name": AUTHOR, "email": "user@local"},
        "agents": [f"./agents/{name}.md"],
        "skills": [f"./skills/{s}" for s in cfg["skills"]],
        "expertType": "agent",
        "agentName": name,
        "displayName": cfg["displayName"],
        "profession": cfg["profession"],
        "displayDescription": cfg["displayDescription"],
        "avatar": "avatars/expert.png",
        "categoryId": CATEGORY_ID,
        "defaultInitPrompt": cfg["defaultInitPrompt"],
        "plugin": name,
        "tags": cfg["tags"],
        "quickPrompts": cfg["quickPrompts"],
    }
    (dest / ".codebuddy-plugin/plugin.json").write_text(
        json.dumps(p, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_readme(dest: Path, name: str, cfg: dict):
    skills = "\n".join(f"- `{s}`" for s in cfg["skills"])
    prompts = "\n".join(f"- {q['zh']}" for q in cfg["quickPrompts"])
    domain = {
        "drama-episode-writer": "剧本",
        "drama-asset-designer": "素材",
        "drama-virtual-director": "分镜与出片",
    }[name]
    text = f"""# {cfg['displayName']['zh']}（{cfg['profession']['zh']}）

独立上架的 **Agent 型专家**（`expertType: agent`），由 Team 型专家团「漫剧制片厂」拆分而来，
只负责「{domain}」这一环。

> {cfg['displayDescription']['zh']}

## 边界与交接

- 上游：{UPSTREAM[name]}
- 下游：{DOWNSTREAM[name]}
- 三个专家是**独立会话**，跨专家传递必须粘贴完整产出原文（零压缩铁律），禁止摘要转述。
- 本专家不调度团队、不越界做上游或下游的活；缺什么就写进《交接卡》让用户带回对应专家。

## 挂载技能（{len(cfg['skills'])} 个）

{skills}

包内 `shared/`（LOCKED 数据契约、硬闸、词典）与 `tools/`（花钱门、品牌扫、提示词自检、五道硬闸等）
是**全量副本**，路径原样可解析；跨 skill 的 references 引用已按闭包补齐，但只有本域技能带 SKILL.md。

## 试试这样问我

{prompts}

## 硬闸速记

先检后烧；素材在分镜之前；剧本/资产/分镜逐字对账；品牌三层禁；任何扣积分动作先 quote → 用户明确批准 → run；
成片必过五项核验，一次翻车 = 一条新规。完整规则见 `shared/hard-gates.md` 与 `shared/output-formats.md`。

## 上架与安装

- 上架包：`dist/expert-packages/{name}.zip`（开放平台 → 发布管理 → 专家 → 创建）。
- 卡片头像：`avatars/expert.png`（512×512 PNG，≤500KB，可自行替换，保持文件名）。
- 本地已注册到 `{CONFIG_DIR}/plugins/marketplaces/my-experts/.codebuddy-plugin/marketplace.json`。
- 重新生成：`python3 tools/build_individual_experts.py`（构建时从仓库一次性取材；包发布后独立演进）。
"""
    (dest / "README.md").write_text(text, encoding="utf-8")


def fix_texts(dest: Path):
    for f in dest.rglob("*"):
        if not f.is_file() or f.suffix not in (".md", ".txt"):
            continue
        try:
            t = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        new = t
        for a, b in TEXT_FIXES.items():
            new = new.replace(a, b)
        if new != t:
            f.write_text(new, encoding="utf-8")


def close_refs(dest: Path):
    """迭代补齐跨 skill 的 references 引用，直到闭包稳定。

    补进来的文件自身还会再引用别的 skill 文档（例如 video-consistency.md 引用
    character-prompts.md），所以单趟不够；只补被引用的 .md，不补 SKILL.md。
    """
    added_total, missing = 0, set()
    for _ in range(8):
        targets = set()
        for f in dest.rglob("*"):
            if not f.is_file() or f.suffix not in (".md", ".txt", ".py", ".json"):
                continue
            try:
                t = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for rx in (CROSS_REF, REL_REF):
                for m in rx.finditer(t):
                    targets.add((m.group(1), m.group(2)))
        added = 0
        for skill, fname in sorted(targets):
            target = dest / "skills" / skill / "references" / fname
            if target.exists():
                continue
            src = SRC_SKILLS / skill / "references" / fname
            if src.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, target)
                added += 1
            else:
                missing.add(f"skills/{skill}/references/{fname}")
        added_total += added
        if added == 0:
            break
    return added_total, sorted(missing)


def strict_yaml(dest: Path):
    run(["ruby", "-ryaml", "-e", RUBY_YAML, str(dest)])


def check_refs(dest: Path):
    missing = []
    for f in dest.rglob("*"):
        if not f.is_file() or f.suffix != ".md":
            continue
        t = f.read_text(encoding="utf-8", errors="ignore")
        for rx in (CROSS_REF, REL_REF):
            for m in rx.finditer(t):
                p = dest / "skills" / m.group(1) / "references" / m.group(2)
                if not p.exists():
                    missing.append(f"{f.relative_to(dest)} -> skills/{m.group(1)}/references/{m.group(2)}")
    return sorted(set(missing))


def build_one(name: str):
    cfg = BASE_PLUGIN[name]
    dest = PLUGINS_DIR / name
    marker = dest / ".split-expert"
    print(f"\n{'=' * 72}\n▶ {name}  |  {cfg['displayName']['zh']}  |  {len(cfg['skills'])} skills\n{'=' * 72}")

    # 1) init（只在首次创建时）
    if dest.exists() and not marker.exists():
        raise SystemExit(f"❌ 目录已存在且不是本脚本生成，拒绝覆盖：{dest}")
    if not dest.exists():
        run(["python3", EM / "init_expert.py", name, "--type", "agent",
             "--path", PLUGINS_DIR], quiet=True)
        marker.write_text("generated by build_individual_experts.py\n", encoding="utf-8")

    # 2) 内容
    (dest / ".codebuddy-plugin").mkdir(exist_ok=True)
    write_plugin(dest, name, cfg)
    (dest / "agents").mkdir(exist_ok=True)
    for stale in (dest / "agents").glob("*.md"):
        if stale.name != f"{name}.md":
            stale.unlink()
    (dest / "agents" / f"{name}.md").write_text(AGENT_MDS[name], encoding="utf-8")
    write_readme(dest, name, cfg)

    # 3) 本域 skills + 全量 shared/tools + 全链图
    skills_dst = dest / "skills"
    if skills_dst.exists():
        shutil.rmtree(skills_dst)
    skills_dst.mkdir()
    for s in cfg["skills"]:
        shutil.copytree(SRC_SKILLS / s, skills_dst / s,
                        ignore=lambda _d, names: [n for n in names
                                                  if n in SKIP_NAMES or Path(n).suffix in SKIP_SUFFIX])
    copy_tree(SRC_SHARED, dest / "shared")
    copy_tree(SRC_TOOLS, dest / "tools")
    docs = dest / "docs"
    docs.mkdir(exist_ok=True)
    shutil.copy2(ROOT / "docs/flow-map.md", docs / "flow-map.md")

    fix_texts(dest)
    added, missing_src = close_refs(dest)
    print(f"  资源：{len(cfg['skills'])} skills / 15 shared / tools 全量 / 引用闭包补 {added} 个")
    if missing_src:
        print(f"  ⚠️ 源仓库也缺的引用（仅为说明性路径）：{missing_src}")

    # 4) 头像（沿用原团队同画风 512×512）
    avatars = dest / "avatars"
    avatars.mkdir(exist_ok=True)
    src_avatar = SRC_TEAM / "avatars" / cfg["avatar_src"]
    if not src_avatar.exists():
        raise SystemExit(f"❌ 原专家团头像不存在：{src_avatar}")
    for old in avatars.glob("*"):
        if old.is_file() and old.name != "expert.png":
            old.unlink()
    shutil.copy2(src_avatar, avatars / "expert.png")

    # 5) 本地严格解析（平台解析规则 ≠ validate_expert.py）
    strict_yaml(dest)
    miss = check_refs(dest)
    if miss:
        raise SystemExit("❌ 包内引用断链：\n  " + "\n  ".join(miss))

    # 6) 标准流程：validate → register → package（每个专家串行完整走完）
    run(["python3", EM / "validate_expert.py", dest])
    run(["python3", EM / "register_expert.py", dest], quiet=True)
    OUT.mkdir(parents=True, exist_ok=True)
    run(["python3", EM / "package_expert.py", dest, OUT], quiet=True)

    verify_zip(OUT / f"{name}.zip", name, cfg)


def verify_zip(zp: Path, name: str, cfg: dict):
    """从 zip 内再验一遍：本地通过 ≠ 平台解析通过。"""
    size = zp.stat().st_size
    assert size < 20 * 1024 * 1024, f"{name}.zip 超 20MB"
    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(zp) as z:
            z.extractall(td)
        root = Path(td) / name
        pj = json.loads((root / ".codebuddy-plugin/plugin.json").read_text(encoding="utf-8"))
        for k in ("displayName", "profession", "displayDescription", "defaultInitPrompt"):
            assert pj[k]["en"] and pj[k]["zh"], f"{name}: {k} 双语不全"
        assert len(pj["tags"]) == 3 and len(pj["quickPrompts"]) == 3
        assert pj["defaultInitPrompt"]["zh"] == pj["quickPrompts"][0]["zh"]
        assert pj["expertType"] == "agent" and pj["agentName"] == name
        assert pj["categoryId"] == CATEGORY_ID
        for i, q in enumerate(pj["quickPrompts"]):
            assert q["en"] and q["zh"], f"quickPrompts[{i}] 双语不全"
        for t in pj["tags"]:
            assert t["en"] and t["zh"]
        for rel in pj["agents"] + pj["skills"]:
            assert (root / rel[2:]).exists(), f"zip 内缺 {rel}"
        av = root / pj["avatar"]
        assert av.exists() and av.stat().st_size <= 500 * 1024
        assert "[TODO" not in (root / "agents" / f"{name}.md").read_text(encoding="utf-8")
        strict_yaml(root)
        miss = check_refs(root)
        if miss:
            raise SystemExit(f"❌ zip 内引用断链：\n  " + "\n  ".join(miss))
    print(f"  ✅ zip 自检通过：{zp.name}  {size / 1024:.0f} KB  "
          f"| agent / 3 tags / 3 prompts / 双语 / YAML / 引用闭包")


def main():
    for d in (SRC_SKILLS, SRC_SHARED, SRC_TOOLS, SRC_TEAM, EM, PLUGINS_DIR):
        if not d.exists():
            raise SystemExit(f"❌ 依赖目录不存在：{d}")
    retire_old_ids()
    for name in ORDER:
        build_one(name)
    print(f"\n🎉 三个独立专家已注册并打包到：{OUT}")
    print("   原专家团 aigc-drama-studio 保持不动；上架时只传这三个 zip。")


if __name__ == "__main__":
    main()
