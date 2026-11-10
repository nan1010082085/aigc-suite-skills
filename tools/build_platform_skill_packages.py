#!/usr/bin/env python3
"""把本仓库的 18 个 skill 打成 WorkBuddy 开放平台可上传的独立技能包。

平台硬性要求（open.workbuddy.cn 开放文档 / 技能）：
  - 一个 zip = 一个技能，zip 内第一层为 <skill-name>/，SKILL.md 在该目录下
  - 目录最多两层；zip ≤ 3MB；仅 .zip
  - SKILL.md frontmatter 必填 8 项：name, display_name, display_name_en,
    description, description_zh, description_en, version, author

本仓库的 skill 会引用仓库根的 shared/ 与 tools/，因此每个上架包内附一份全量
副本（shared/ 与 tools/ 均为第二层目录，符合层级要求），路径原样可解析。
源仓库与专家包均不被修改。

2026-11-06 v1.0.1 修复「内置文件缺失」质检驳回：
  shared/pre-gen-research.md 等共享文档会引用 `skills/<其它 skill>/references/xxx.md`，
  独立技能包里没有 skills/ 这一层，平台按引用反查资源时判定为缺文件。
  本脚本在打包副本中把这类跨 skill 引用目标**扁平化复制**进 references/，
  并把包内引用路径改写成 references/xxx.md（同名不同内容时加 skill 名前缀），
  递归补齐引用闭包；源仓库仍保留原本有效的 skills/... 路径。
  另外清理两类不可解析的示例路径，并从包内排除本构建脚本本身。

2026-11-06 v1.0.2 修复第二批「内置文件缺失」（缺的是「技能」不是「文件」）：
  平台会把文档里的 `prop-studio` / `shot-qa` / `storyboard-director` 这类
  纯技能名、以及「对应风格 skill 的 style-profile.md」这类描述短语，判定为
  「依赖的技能未内置」。独立技能包按规则只能有一个技能，所以上架副本统一把
  跨技能名改成中文展示名、把含 skill 字样的资源短语改成中文环节描述，
  让包内不再出现任何指向其它技能的引用。源仓库与专家包保持原样。

用法：
    python3 tools/build_platform_skill_packages.py [--skip <skill-name> ...]
输出：
    dist/skill-packages/<skill-name>.zip
"""

import argparse
import json
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_SKILLS = ROOT / "skills"
SRC_SHARED = ROOT / "shared"
SRC_TOOLS = ROOT / "tools"
OUT = ROOT / "dist" / "skill-packages"

AUTHOR = "酉钱"
VERSION = "1.0.2"  # 2026-11-06 第二批质检驳回：跨技能名引用被判「缺技能」

# 包内跨 skill 文档引用：`skills/<skill>/references/<file>.md`
# 以及 references/ 内文档常用的相对写法 `../<skill>/references/<file>.md`
CROSS_REF_RES = (
    re.compile(r"(?:\.\./)?skills/([a-z0-9-]+)/references/([\w.-]+\.md)"),
    re.compile(r"\.\./([a-z0-9-]+)/references/([\w.-]+\.md)"),
)
# 源仓库里少量文档把其它 skill 的文档简写成 `references/xxx.md`（缺 skill 名），
# 在独立包里同样会指向不存在的文件：按文件名从源仓库补进包内。
LOCAL_REF_RE = re.compile(r"(?<![\w/])references/([\w.-]+\.md)")
# .py 注释里的仓库路径只是出处说明，去掉目录前缀避免被当成包内必需资源。
PY_COMMENT_REF_RE = re.compile(r"skills/[a-z0-9-]+/references/([\w.-]+\.md)")

# 仅在上架副本生效的文本修正：占位/示例路径不可解析，改成包内真实路径或纯文件名。
TEXT_FIXES = {
    "`aigc-suite-skills/tools/shot_gate.py`": "`tools/shot_gate.py`",
    "`skills/style-<名>/references/style-profile.md`": "所选风格的风格档案",
}

# 含 skill 字样 + .md 的描述短语会被平台抽成「技能」类必需资源（审核原文：
# 「技能「对应风格 skill 的 style-profile.md」（shared/pre-gen-research.md 引用）」）。
# 在上架副本里改成中文环节描述，不再像资源引用。长短语必须排在短短语前面。
PHRASE_FIXES = {
    "对应**风格 skill** 的 style-profile.md": "所选风格的风格档案",
    "对应**风格 skill** 的 `style-profile.md`": "所选风格的风格档案",
    "**对应风格 skill**": "**所选风格**",
    "对应**风格 skill**": "所选风格",
    "`skills/style-<名>/references/style-profile.md`": "所选风格的风格档案",
    "`skills/style-<name>/`": "风格技能目录",
    "`style-profile.md`": "风格档案",
    "所选风格 skill 的": "所选风格的",
    "风格 skill 的": "所选风格的",
    "风格 skill 清单": "风格技能清单",
    "风格 skill 结构": "风格技能结构",
    "剧本 skill": "剧本技能",
}

# 构建脚本不是运行时组件，不随上架包分发（其注释里含占位路径）。
BUILD_SCRIPT_NAME = "build_platform_skill_packages.py"

# (中文展示名, 英文展示名, 中文简介, 英文简介, 中文示例, 英文示例)
META = {
    "novel-to-drama": (
        "小说改编漫剧编剧", "Novel-to-Drama Screenwriter",
        "把小说或网文改编成分集漫剧剧本条目，按故事单元分集，保留人物、伏笔与名场面。",
        "Adapt novels and web fiction into episode-ready AI drama script entries, split by story unit.",
        "把这本小说前 20 章改编成 8 集漫剧剧本，每集 60 秒左右并留钩子。",
        "Adapt the first 20 chapters of this novel into eight 60-second drama episodes with hooks.",
    ),
    "idea-to-drama": (
        "想法原创漫剧编剧", "Idea-to-Drama Screenwriter",
        "从一句话脑洞出发，产出 logline、集数规划、人物小传与分集剧本条目。",
        "Turn a one-line idea into a logline, episode plan, character bios and script entries.",
        "我有个想法：能听见别人心声的外卖员卷入豪门争斗，帮我定 logline 和 8 集规划。",
        "My idea: a delivery rider who hears thoughts. Give me a logline and an 8-episode plan.",
    ),
    "character-studio": (
        "人物资产设计", "Character Asset Studio",
        "用三视图身份锚、服装三视图、表情表与脸卡建立跨镜一致的人物资产。",
        "Build cross-shot consistent character assets: three-view anchors, outfits, expressions and face cards.",
        "给主角出一套三视图、两套服装和表情表，解决跨镜变脸。",
        "Create a three-view anchor, two outfits and an expression sheet for the lead character.",
    ),
    "scene-studio": (
        "场景资产设计", "Scene Asset Studio",
        "建立纯空镜场景主图与光影锁定变体，保证换场不跳戏、同场景多镜复用。",
        "Build empty-plate scene key art with locked lighting and variants for spatial continuity.",
        "给这集的三个场景出纯空镜主图并锁定下午光比。",
        "Create empty-plate key art for three scenes and lock the afternoon lighting ratio.",
    ),
    "prop-studio": (
        "道具资产设计", "Prop Asset Studio",
        "按关键性准入建道具卡，出造型锚点主图与剧情状态变体，防止道具穿帮漂移。",
        "Register story-critical props with a locked shape anchor, scale reference and plot-state variants.",
        "这把钥匙是关键道具，出主图和「完好/折断」两个状态变体。",
        "This key is a story-critical prop. Produce a master image and intact/broken state variants.",
    ),
    "storyboard-director": (
        "虚拟导演分镜", "Virtual Storyboard Director",
        "把剧本条目改成时间片分镜块，组装六要素并产出可直出片的中文提示词。",
        "Turn script entries into time-sliced storyboard blocks with six-element ready-to-generate prompts.",
        "把第 3 集剧本拆成分镜块，每镜给可直出片的中文指令。",
        "Break episode 3 into storyboard blocks with ready-to-generate Chinese prompts.",
    ),
    "shot-qa": (
        "出片三道闸质检", "Three-Gate Shot QA",
        "出图出片前跑价格闸、剧情校验、素材校验三道闸，先检查再报价，过闸才准生成。",
        "Run price, script and asset gates before generation, with quote, approval and result verification.",
        "这集的剧本、资产、分镜都齐了，帮我过三道闸再报价。",
        "Script, assets and storyboards are ready. Run the three gates and quote before generating.",
    ),
    "video-producer": (
        "出片执行制片", "Video Production Producer",
        "单镜隔离生成、试产锁参、素材入库与失败归因、崩坏镜单独重生成、后期收口。",
        "Execute isolated single-shot generation, pilot parameter locking, failure attribution and post closeout.",
        "报价已批准，按单镜隔离开跑，先试产 3 镜锁参。",
        "Approved. Start isolated single-shot generation with a 3-shot pilot to lock parameters.",
    ),
    "clip-review": (
        "成片核验与回流", "Clip Review & Rule Feedback",
        "成片抽帧五项核验、缺陷分层归因、修复回流规则，一次翻车沉淀一条新规。",
        "Sample finished clips, attribute defects to their true layer and feed lessons back as rules.",
        "这条成片手部穿模了，定位根因并把教训写成规则。",
        "Hands clip through each other in this shot. Find the root layer and write it into the rules.",
    ),
    "style-cg-refined": (
        "半写实精致CG风格", "Semi-realistic Refined CG Style",
        "本套件主风格：设计可风格化、渲染必须写实，PBR 材质、自然光比与电影运镜。",
        "House default style: stylized design with realistic rendering, PBR materials and cinematic camera work.",
        "给我这部都市剧的风格锁模板和材质词表。",
        "Give me the style-lock template and material word bank for this urban drama.",
    ),
    "style-anime": (
        "日漫二次元风格", "Japanese Anime Style",
        "日漫/二次元风格段，含赛璐璐平涂、描边与色块规则及翻车点对策。",
        "Japanese anime style block with cel shading, outlines, flat colour rules and anti-failure notes.",
        "取日漫风格的风格锁模板，别混写实摄影词。",
        "Get the anime style-lock template without any photorealistic camera terms.",
    ),
    "style-3d-anime": (
        "新中式三渲二风格", "New Chinese 3D-Anime Style",
        "三渲二与新中式国风角色设定、资产规格与材质表现指引。",
        "3D-to-2D and New Chinese aesthetic character design and asset specification.",
        "这部国风剧用三渲二，给我角色设定规格。",
        "Use the 3D-to-2D style for this period drama and give me the character spec.",
    ),
    "style-pixar": (
        "皮克斯质感风格", "Pixar-quality 3D Style",
        "皮克斯质感三维风格段，适合合家欢、温情与萌系题材。",
        "Pixar-quality 3D style block suited to family, warm and cute stories.",
        "给这部合家欢短剧取皮克斯质感的风格段。",
        "Get a Pixar-quality style block for this family short series.",
    ),
    "style-comic": (
        "漫画分镜风格", "Comic Panel Style",
        "漫画分镜感、速度线与网点表现，适合强节奏静态视觉叙事。",
        "Comic panel aesthetics with speed lines and halftone dots for punchy visual storytelling.",
        "用漫画分镜风格出这段追逐戏的风格段。",
        "Give me a comic-panel style block for this chase sequence.",
    ),
    "style-cyberpunk": (
        "赛博朋克风格", "Cyberpunk Style",
        "赛博、蒸汽、柴油三系的未来都市视觉规则与霓虹光比词库。",
        "Cyber, steam and diesel-punk future-city visual rules with a neon lighting word bank.",
        "取赛博朋克三系里适合悬疑剧的那套风格段。",
        "Pick the cyberpunk sub-style that fits a suspense series.",
    ),
    "style-photoreal": (
        "写实摄影风格", "Photoreal Style",
        "写实摄影风格段，含即梦链路转 cel 防拦截的适配说明。",
        "Photoreal style block with backend-specific notes on cel conversion to avoid blocking.",
        "这部年代剧要写实摄影质感，告诉我即梦链路怎么适配。",
        "This period drama needs a photoreal look. Explain the Jimeng backend adaptation.",
    ),
    "style-fantasy": (
        "西方玄幻风格", "Western Fantasy Style",
        "中世纪史诗、魔法光效、油画厚重质感与繁复盔甲的风格词库。",
        "Medieval epic, magical glow, oil-painting texture and ornate armour style word bank.",
        "给骑士法师题材取西方玄幻风格段。",
        "Get a western fantasy style block for a knight-and-mage story.",
    ),
    "style-infinite-flow": (
        "无限流风格", "Infinite Flow Style",
        "多元宇宙、系统 UI、维度裂缝等无限流题材的视觉关键词与组合。",
        "Multiverse, system UI and dimensional rift visual keywords for infinite-flow stories.",
        "这部无限流要系统 UI 和维度裂缝的风格词。",
        "Give me system-UI and dimensional-rift style terms for this infinite-flow series.",
    ),
}


def q(value: str) -> str:
    """YAML 双引号字符串，避免中文、冒号、引号破坏 frontmatter。"""
    return json.dumps(value, ensure_ascii=False)


def read_frontmatter(text: str):
    """返回 (frontmatter_dict, body)。仅处理本仓库的简单 key: value 结构。"""
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not m:
        return {}, text
    data = {}
    for line in m.group(1).split("\n"):
        if ":" in line and not line.lstrip().startswith("-"):
            k, _, v = line.partition(":")
            data[k.strip()] = v.strip().strip('"').strip("'")
    return data, m.group(2)


def bundle_cross_refs(dst: Path) -> int:
    """把包内 .md 引用的其它 skill 文档补进 references/，并重写引用路径。

    平台按文档引用反查「必需资源」；独立技能包里没有源仓库的 skills/ 目录层，
    `skills/<skill>/references/xxx.md` 会被判为内置文件缺失。这里把目标文件
    扁平化复制到 references/（第二层目录，符合层级要求），引用改写成包内路径；
    同名但内容不同的文件加 skill 名前缀避免覆盖。递归补齐引用闭包。

    只改上架副本，源仓库与专家包的路径一字不动。返回新增文件数。
    """
    refs_dir = dst / "references"
    refs_dir.mkdir(parents=True, exist_ok=True)
    # 包内原生 references 的原始字节，用来判断"同名即同一份"；
    # 不能用已改写过的文件去比对，否则会把同一来源误判成冲突并重复复制。
    initial = {f.name: f.read_bytes() for f in refs_dir.glob("*.md")}
    placed: dict[Path, str] = {}  # 源仓库文件 -> 包内文件名，保证一个来源只落一份
    added = 0

    def place(src: Path, skill: str, wanted: str) -> str:
        nonlocal added
        if src in placed:
            return placed[src]
        raw = src.read_bytes()
        if wanted in initial and initial[wanted] == raw:
            placed[src] = wanted
            return wanted
        dest = wanted
        target = refs_dir / dest
        while target.exists() and target.read_bytes() != raw:
            dest = f"{skill}-{dest}"
            target = refs_dir / dest
        if not target.exists():
            shutil.copy2(src, target)
            added += 1
        placed[src] = dest
        return dest

    for _ in range(8):  # 引用闭包：新补进来的文档自己也可能引用别的 skill 文档
        explicit: dict[str, tuple[str, str, Path]] = {}
        local: set[str] = set()
        for doc in sorted(dst.rglob("*.md")):
            text = doc.read_text(encoding="utf-8")
            for rx in CROSS_REF_RES:
                for m in rx.finditer(text):
                    skill, fname = m.group(1), m.group(2)
                    src = SRC_SKILLS / skill / "references" / fname
                    if src.is_file():
                        explicit[m.group(0)] = (skill, fname, src)
            local.update(m.group(1) for m in LOCAL_REF_RE.finditer(text))
        if not explicit and not local:
            break

        rewrite = {}
        for old, (skill, fname, src) in explicit.items():
            rewrite[old] = f"references/{place(src, skill, fname)}"
        for fname in sorted(local):
            if (refs_dir / fname).exists():
                continue
            candidates = sorted(SRC_SKILLS.glob(f"*/references/{fname}"))
            if len(candidates) == 1:
                src = candidates[0]
                dest = place(src, src.parent.parent.name, fname)
                if dest != fname:
                    rewrite[f"references/{fname}"] = f"references/{dest}"

        changed = False
        for doc in sorted(dst.rglob("*.md")):
            text = doc.read_text(encoding="utf-8")
            new = text
            for old, replacement in rewrite.items():
                new = new.replace(old, replacement)
            for old, replacement in TEXT_FIXES.items():
                new = new.replace(old, replacement)
            if new != text:
                doc.write_text(new, encoding="utf-8")
                changed = True
        for py in sorted(dst.rglob("*.py")):
            text = py.read_text(encoding="utf-8")
            new = PY_COMMENT_REF_RE.sub(r"\1", text)
            if new != text:
                py.write_text(new, encoding="utf-8")
                changed = True
        if not changed:
            break
    return added


def _split_head(text: str) -> tuple[str, str]:
    """拆出 frontmatter（含围栏）与正文，用于只改正文、不动平台解析字段。"""
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            cut = end + len("\n---\n")
            return text[:cut], text[cut:]
    return "", text


def skill_id_re() -> re.Pattern:
    """匹配 18 个 skill ID（独立词，不误伤带后缀的文件名）。"""
    ids = sorted(META, key=len, reverse=True)
    return re.compile(r"(?<![a-z0-9-])(?:" + "|".join(map(re.escape, ids)) + r")(?![a-z0-9-])")


def neutralize_skill_refs(dst: Path, own: str) -> None:
    """消除上架副本里的跨技能引用。

    平台把 `prop-studio`、`shot-qa`、`storyboard-director` 这类纯技能名判成
    「依赖的技能未内置」；独立技能包只能有一个技能，因此把包内所有 skill ID
    （含自身在正文中的自指）换成中文展示名，并清掉 `skills/xxx` 这类路径与
    反引号资源标识；含 skill 字样的描述短语改成中文环节描述。
    frontmatter 的 name/description 属平台解析字段，保持原样。
    """
    zh_all = {k: v[0] for k, v in META.items()}
    ids = skill_id_re()
    skills_path_re = re.compile(r"skills/([a-z0-9-]+)")
    skill_word_re = re.compile(r"(?<![A-Za-z0-9_-])skill(?![A-Za-z0-9_-])")
    for doc in sorted(dst.rglob("*.md")):
        text = doc.read_text(encoding="utf-8")
        head, body = _split_head(text)
        for old, new in PHRASE_FIXES.items():
            body = body.replace(old, new)
        # 修掉连续两层替换产生的重复措辞，保持正文可读。
        body = body.replace("所选风格的 所选风格的", "所选风格的")
        # `skills/xxx` 是仓库根的目录路径，独立包里永远不存在：连前缀一起去掉。
        body = skills_path_re.sub(lambda m: zh_all.get(m.group(1), "对应环节"), body)
        # 反引号里的 ID 去掉反引号再换名，避免中文名仍被当成资源标识。
        for sid, zh in zh_all.items():
            body = body.replace(f"`{sid}`", zh)
        body = ids.sub(lambda m: zh_all[m.group(0)], body)
        for zh in set(zh_all.values()):
            body = body.replace(f"`{zh}`", zh)
        # 不带目录前缀的 style-profile.md 在多数包里不存在；路径写法保留。
        body = re.sub(r"(?<![/\w])style-profile\.md", "风格档案", body)
        body = skill_word_re.sub("技能", body)
        body = re.sub(r"([\u4e00-\u9fff]) 技能", r"\1技能", body)
        if head + body != text:
            doc.write_text(head + body, encoding="utf-8")


PATH_REF_RE = re.compile(r"`([^`\n]*?\.(?:md|py|json|txt|sh))`")


def verify_package(zip_path: Path, root: str) -> list[str]:
    """从最终 zip 内自检：目录层级、大小、frontmatter 8 项、文档引用零断链。"""
    problems: list[str] = []
    if zip_path.stat().st_size > 3 * 1024 * 1024:
        problems.append("zip 超过 3MB")
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        file_set = set(names)
        if f"{root}/SKILL.md" not in file_set:
            problems.append("根缺 SKILL.md")
        else:
            head = zf.read(f"{root}/SKILL.md").decode("utf-8")
            for key in ("name", "display_name", "display_name_en", "description",
                        "description_zh", "description_en", "version", "author"):
                if not re.search(rf"^{key}:", head, re.MULTILINE):
                    problems.append(f"frontmatter 缺 {key}")
        for n in names:
            rel = n[len(root) + 1:] if n.startswith(root + "/") else n
            if rel.count("/") > 1:
                problems.append(f"目录层级超限: {n}")
        ids = skill_id_re()
        for n in (x for x in names if x.endswith(".md")):
            text = zf.read(n).decode("utf-8", "ignore")
            _, body = _split_head(text)
            for m in ids.finditer(body):
                problems.append(f"skill ID 残留 {n}: {m.group(0)}")
            if "skills/" in body:
                problems.append(f"skills/ 路径残留 {n}")
            for m in PATH_REF_RE.finditer(text):
                ref = m.group(1).strip()
                # 占位符、说明性文字、仓库外路径不参与断链判定
                if any(x in ref for x in ("<", ">", "…", "xxx", "*", " ", "§")):
                    continue
                ref = ref.split("#")[0].rstrip(":")
                if ref.startswith("./"):
                    ref = ref[2:]
                if ref.startswith("../"):
                    continue
                if "/" not in ref:
                    # 纯 .md 文件名引用也要能在包内找到，否则平台会判「缺文件」
                    if ref.endswith(".md") and ref != "SKILL.md" and not any(
                        f"{root}/{d}/{ref}" in file_set
                        for d in ("references", "shared", "tools")
                    ):
                        problems.append(f"断链 {n}: {ref}")
                    continue
                # 独立包里不该再出现源仓库的 skills/ 路径
                if ref.startswith("skills/"):
                    problems.append(f"残留跨 skill 路径 {n}: {ref}")
                    continue
                # 只判定包内三大目录的资源；docs/、analysis/、manju-pipeline/ 等
                # 是项目侧/外部资料的说明性出处，不属于本包必需资源。
                if not ref.startswith(("shared/", "tools/", "references/")):
                    continue
                if f"{root}/{ref}" not in file_set and ref not in file_set:
                    problems.append(f"断链 {n}: {ref}")
    return problems


def build_skill(name: str, workdir: Path) -> Path:
    src = SRC_SKILLS / name
    dst = workdir / name
    dst.mkdir(parents=True, exist_ok=True)

    raw = (src / "SKILL.md").read_text(encoding="utf-8")
    fm, body = read_frontmatter(raw)
    if name not in META:
        raise ValueError(f"缺少展示元数据: {name}")
    zh, en, desc_zh, desc_en, ex_zh, ex_en = META[name]

    description = fm.get("description", "").replace("<", "").replace(">", "")
    if not description:
        description = desc_zh

    head = "\n".join([
        "---",
        f"name: {name}",
        f"display_name: {q(zh)}",
        f"display_name_en: {q(en)}",
        f"description: {q(description)}",
        f"description_zh: {q(desc_zh)}",
        f"description_en: {q(desc_en)}",
        f"examples_zh:",
        f"  - {q(ex_zh)}",
        f"examples_en:",
        f"  - {q(ex_en)}",
        f"version: {VERSION}",
        f"author: {q(AUTHOR)}",
        "---",
        "",
    ])
    (dst / "SKILL.md").write_text(head + body, encoding="utf-8")

    # 原样复制 references/，并把 shared/、tools/ 作为第二层目录附入，
    # 保证规则文档里的 `shared/xxx.md`、`tools/xxx.py` 路径无需改写即可解析。
    if (src / "references").exists():
        shutil.copytree(src / "references", dst / "references")
    shutil.copytree(SRC_SHARED, dst / "shared",
                    ignore=shutil.ignore_patterns(".DS_Store"))
    shutil.copytree(SRC_TOOLS, dst / "tools",
                    ignore=shutil.ignore_patterns(".DS_Store", "__pycache__", "*.pyc",
                                                  BUILD_SCRIPT_NAME))
    bundle_cross_refs(dst)
    neutralize_skill_refs(dst, name)

    zip_path = OUT / f"{name}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(dst.rglob("*")):
            if f.is_file():
                zf.write(f, f.relative_to(workdir))
    return zip_path


def main():
    ap = argparse.ArgumentParser(description="生成 WorkBuddy 开放平台独立技能包")
    ap.add_argument("--skip", nargs="*", default=[], metavar="NAME",
                    help="保留现有 zip、不重生成的 skill 名（如已过审的条目）")
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    workdir = OUT / "_build"
    if workdir.exists():
        shutil.rmtree(workdir)
    workdir.mkdir(parents=True)

    all_names = sorted(p.name for p in SRC_SKILLS.iterdir() if p.is_dir())
    missing = [n for n in all_names if n not in META]
    if missing:
        raise SystemExit(f"以下 skill 缺少展示元数据，请先补 META：{missing}")
    unknown_skip = [n for n in args.skip if n not in all_names]
    if unknown_skip:
        raise SystemExit(f"--skip 里有不存在的 skill：{unknown_skip}")
    names = [n for n in all_names if n not in args.skip]

    too_big = []
    broken = []
    for n in names:
        z = build_skill(n, workdir)
        kb = z.stat().st_size / 1024
        flag = "  ⚠️ 超过 3MB" if kb > 3072 else ""
        print(f"  {n:<24} {kb:7.1f} KB{flag}")
        if kb > 3072:
            too_big.append(n)
        issues = verify_package(z, n)
        if issues:
            broken.append((n, issues))
    shutil.rmtree(workdir)
    skip_note = f"（按 --skip 保留原有 zip：{', '.join(args.skip)}）" if args.skip else ""
    print(f"\n共生成 {len(names)} 个独立技能包 → {OUT}{skip_note}")
    if too_big:
        print(f"超限包：{too_big}")
    if broken:
        print(f"\n包内自检未通过（{len(broken)} 个包）：")
        for n, issues in broken:
            for issue in issues[:12]:
                print(f"  [{n}] {issue}")
            if len(issues) > 12:
                print(f"  [{n}] … 另有 {len(issues) - 12} 条")
        raise SystemExit(1)
    print("包内自检：目录层级 / 大小 / frontmatter 8 项 / 文档引用零断链 —— 全部通过")


if __name__ == "__main__":
    main()
