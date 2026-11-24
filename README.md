# aigc-suite-skills

漫剧（AI 短剧）创作技能套件：**从小说 / 想法到成片**的 18 个 Claude Code skill，覆盖剧本、素材（人物 / 场景 / 道具）、分镜、出视频执行、出片质检、成片回流。

三条主轴：**场景转场连贯 · 剧情分镜 · 人物建模质量**。

> 🆓 **已上架 WorkBuddy 专家团「漫剧制片厂」（免费）**——多角色协作团队在 WorkBuddy 开放平台「专家」货架可直接安装。专家团是平台侧独立交付物，与本仓库独立演进；平台替换 zip / 填版本 / 发布由账号本人操作。

## 架构口径（2026-11-24）

| 层 | 是什么 | 不是什么 |
|----|--------|----------|
| **Skills** | 创作方法论（剧本、七格设定卡、分镜、出片指令） | 某一厂商 CLI / 短剧模板的说明书 |
| **Gates** | 合规检查 + 花钱提示（报价→用户批本批账单→跑） | 绑死 Notion / 绑死 dreamina 的工具仪式 |
| **Backends** | `shared/backends.md` 可插拔出口 | skill 本体；换后端只改方言，不改方法论 |

**真相源 = 项目本地文件**（剧本 / `assets.json` / registry / 锁版 prompt / 生成记录）。Notion 等外部表仅为可选适配。

## 流水线

```
小说 ─→ novel-to-drama ─┐
                        ├─→ 剧本条目 ─→ 素材层 ─→ 分镜层 ─→ 出片（执行顺序：剧本→素材→分镜）
想法 ─→ idea-to-drama  ─┘      │            │          │
                    character-studio ─→ 人物资产 ──┤ storyboard-director ─→ 分镜块
                    scene-studio ────→ 场景资产 ──┤  （@引用全指向已建资产）
                    prop-studio ─────→ 道具资产 ──┤  prompt_compiler ─→ 出图/视频指令
                    lora_registry（视觉元数据）──┘
        style-*（风格段，一部剧锁 1 种）
                    clip-review（成片核验与回流）─────────────────────────────┤
                                                                                ▼
                                                              shot-qa（三道闸）─→ video-producer ─→ 成片
```

## Skills（18 个）

| 链路 | Skill |
|------|-------|
| 剧本 | `novel-to-drama` 小说改编 ｜ `idea-to-drama` 想法原创 |
| 资产 | `character-studio` 人物 ｜ `scene-studio` 场景 ｜ `prop-studio` 道具（分工见下节） |
| 分镜 | `storyboard-director` 虚拟导演 + 提示词工程（后端可插拔） |
| 执行 | `video-producer` 出视频（单镜隔离/试产锁参/容错收口/时间轴对时） |
| 质检 | `shot-qa` 出片三道闸 + 五道硬闸预检（先检查再花钱） |
| 回流 | `clip-review` 成片核验与规则回流（一次翻车=一条新规） |
| 风格 | `style-cg-refined`（主）/ `style-3d-anime` / `style-anime` / `style-comic` / `style-pixar` / `style-cyberpunk` / `style-fantasy` / `style-infinite-flow` / `style-photoreal`（9 种，一部剧锁 1 种全剧不换） |

## 素材三分工（2026-11-06 定版）

| 素材 | 卡体 | 独立指令 / 变体 | 不做什么 |
|------|------|----------------|----------|
| **人物** | 基础形象设定卡 = **三视图 + 头部特写 + 眼部特写**（身份锚，16:9 七格） | **单张表情 EXP**（6–8，出片按镜挂一张；宫格仅审阅）+ 角度/pose/光影按需；**装扮 OUT** 独立三视图+表情子集；编号见 `shared/id-and-registry.md` | 服装饰品随人物图；禁语义文件名当身份；禁平台三格人台冒充设定卡 |
| **道具** | **关键性准入**：只有承载剧情/线索/身份/情绪/特写记忆点的道具才出卡；一张**主视图为主** | 状态变体走图生图（一状态一素材） | 普通物件不出卡；固定装饰画进场景 |
| **场景** | 空镜 + 光影锁定 | 镜头变体（同场景多机位） | 不放人（有人场景不能用于出视频） |

设定卡/REF 锁身份；出片按镜挂 **REF（或 OUT）+ 当前 EXP + LOC**（素材关联硬闸）。剧本须附视觉化标注（`skills/novel-to-drama/references/visual-annotation-template.md`）。

## 校验体系：合规闸，不是创作闸

> **最高原则（2026-11-05 用户令）**：一切检查、校验是**合规**，不是限制模型、限制发挥、限制创作。字数无上限、题材/风格/叙事/镜头语言完全自由。

| 闸 | 工具 | 拦什么 |
|----|------|--------|
| 提示词合规闸（7 项机检） | `tools/prompt_selfcheck.py` | 平台违禁词、裸英文运镜、多镜缺时间码、refs>9、重复块、每镜 <250 字保底、时间轴不对时 |
| 出图/出视频五道硬闸 | `tools/pre_gen_gate.py` | 分镜细节保底、素材关联、剧情核验、场景纯净（空镜）、**本地项目源** |
| 花钱门 | `tools/credit_gate.py` | 扣积分前报价提示、**本批账单**用户批准才跑（不绑死某一工具），一枪一停 |
| 广告闸 | `tools/brand_scan.py` | 品牌/商标/包装词（道具一律素色化） |

## 测试

```bash
python3 -m pytest tests/ -q   # 单测（合规闸/品牌扫/花钱门/skill lint）
sh tests/skill-smoke/run.sh   # skill → 指令 全指令验证（不烧积分）
```

`tests/` 与本地 `docs/`（计划/上传记录/调研归档）**均不上 GitHub**，按 `.gitignore` 留在本机。

## 安装

```bash
git clone git@github.com:nan1010082085/aigc-suite-skills.git ~/aigc-suite-skills

# Claude Code（symlink，git pull 即更新）
for s in ~/aigc-suite-skills/skills/*; do ln -sfn "$s" ~/.claude/skills/$(basename $s); done
ln -sfn ~/aigc-suite-skills/shared ~/.claude/skills/aigc-suite-shared
```

**Cursor**：把 `skills/` 拷入项目规则目录，把 `shared/` + `tools/` 放进 vendor 引用路径，在 `AGENTS.md` 标明按各 `SKILL.md` 执行、出图/出片过花钱门。

**Codex**：`cp -r` 整仓到 `vendor/aigc-suite-skills`，在 `AGENTS.md` 按任务路由到对应 `SKILL.md`。

不想手动装可直接用 WorkBuddy 专家团「漫剧制片厂」（免费）。

## 使用

对话中说「小说改编」「出分镜」「人物出图」「出片检查」等即自动触发对应 skill；也可点名「用 idea-to-drama 原创一部漫剧」。

规则与词典在 `shared/`，机器闸门在 `tools/`。本地流水线说明与上传操作手册在本机 `docs/`（不上仓）。

## 用途声明

- `tools/fanqie_ocr.py` 等抽取工具仅用于**个人创作素材的本地抽取**（本地渲染 + 系统 OCR，不做对抗、不分发原文），请遵守来源平台服务条款；本仓库不提供任何绕过付费/反爬的对抗手段。
- 示例与文档中的人名/道具/剧名均为**脱敏占位**；真实剧内数据不在本仓库；`tools/lora_registry.json` 为占位示例，真实注册表存项目侧。
