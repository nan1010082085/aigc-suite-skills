# aigc-suite-skills

漫剧（AI 短剧）创作技能套件：**从小说 / 想法到成片**的 18 个 skill，覆盖剧本、素材（人物 / 场景 / 道具）、分镜、出视频执行、出片质检与成片回流。

三条主轴：**场景转场连贯 · 剧情分镜 · 人物建模质量**。

> 🆓 WorkBuddy 开放平台已上架专家团「漫剧制片厂」与 3 个独立专家（免费）。它们是平台侧独立交付物，与本仓库各自演进；zip 替换 / 填版本 / 提交审核 / 公开发布由账号本人在平台操作，打包维护见本机 `docs/WorkBuddy专家团与Skill包上传指南.md`（不上公开仓）。

## 架构口径

| 层 | 是什么 | 不是什么 |
|----|--------|----------|
| **Skills** | 创作方法论（剧本、七格设定卡、分镜、出片指令） | 某一厂商 CLI / 短剧模板的说明书 |
| **Gates** | 合规红线 + 机检硬停 + 花钱门（报价→用户批本批账单→跑） | 绑死 Notion / 绑死 dreamina 的工具仪式 |
| **Backends** | `shared/backends.md` 可插拔出口 | skill 本体；换后端只改方言，不改方法论 |

- **Skill 直载（强制）**：命中任务 → Read `skills/<name>/SKILL.md` → 再读其点名的 references；禁止用对话记忆 / claude-mem 摘要 / `lessons` / 旧测薄稿顶替（契约 `shared/skill-load.md`）。
- **真相源 = 项目本地文件**（剧本 / `assets.json` / registry / 锁版 prompt / 生成记录）。Notion 等外部表仅为可选适配（`tools/notion_mcp_client.py`），不是硬闸。
- **出片唯一停机条件 = 机检退出码**：`tools/prompt_selfcheck.py --mode video` exit ≠ 0 禁止报价 / 生成；不得用「文档看过了」代替（红线 `shared/red-lines.md`）。

## 流水线

```
小说 ─→ novel-to-drama ─┐
                        ├─→ 剧本条目 ─→ 素材层 ─→ 分镜层 ─→ 质检 ─→ 出片 ─→ 成片回流
想法 ─→ idea-to-drama  ─┘      │            │          │
                    character-studio ─→ 人物资产 ──┤ storyboard-director ─→ 分镜锁版
                    scene-studio ────→ 场景资产 ──┤  （@引用全指向已建资产）
                    prop-studio ─────→ 道具资产 ──┤  prompt_compiler ─→ 出图/视频指令
                    lora_registry（视觉元数据）──┘
        style-*（风格段，一部剧锁 1 种）
        shot-qa（红线机检硬停）→ video-producer → clip-review（五项核验 + 规则回流）
```

## Skills（18 个）

| 链路 | Skill |
|------|-------|
| 剧本 | `novel-to-drama` 小说改编 ｜ `idea-to-drama` 想法原创 |
| 资产 | `character-studio` 人物 ｜ `scene-studio` 场景 ｜ `prop-studio` 道具（分工见下节） |
| 分镜 | `storyboard-director` 虚拟导演 + 提示词工程（后端可插拔） |
| 执行 | `video-producer` 出视频（单镜隔离 / 试产锁参 / 容错收口 / 时间轴对时） |
| 质检 | `shot-qa` 机检硬停 + 三闸预检（先机检再花钱；见 `shared/red-lines.md`） |
| 回流 | `clip-review` 成片核验与规则回流（一次翻车 = 一条新规） |
| 风格 | `style-cg-refined`（主）/ `style-3d-anime` / `style-anime` / `style-comic` / `style-pixar` / `style-cyberpunk` / `style-fantasy` / `style-infinite-flow` / `style-photoreal`（9 种，一部剧锁 1 种全剧不换） |

## 素材三分工

| 素材 | 卡体 | 独立指令 / 变体 | 不做什么 |
|------|------|----------------|----------|
| **人物** | 基础形象设定卡 = **三视图 + 头部特写 + 眼部特写**（身份锚，16:9 七格，按 `character-prompts.md` §1.1 完整骨架） | **一张表情九宫格**（§1.3，图生图**必须挂已锁设定卡**，裁切单张 EXP 入库）+ 装扮 / 角度 / pose 按需（皆挂卡）；编号见 `shared/id-and-registry.md` | 服装饰品随人物图；禁语义文件名当身份；禁不挂卡的独立文生脸；禁平台三格人台冒充设定卡 |
| **道具** | **关键性准入**：只有承载剧情 / 线索 / 身份 / 情绪 / 特写记忆点的道具才出卡；一张**主视图为主** | 状态变体走图生图（一状态一素材） | 普通物件不出卡；固定装饰画进场景 |
| **场景** | 空镜 + 光影锁定 | 镜头变体（同场景多机位） | 不放人（有人场景不能用于出视频） |

设定卡 / REF 锁身份；出片按镜挂 **REF（或 OUT）+ 当前 EXP + LOC**（素材关联硬闸）。剧本须附视觉化标注（`skills/novel-to-drama/references/visual-annotation-template.md`）。

## 校验体系：合规闸，不是创作闸

> **最高原则**：一切检查、校验是**合规**，不是限制模型、限制发挥、限制创作。字数无上限、题材 / 风格 / 叙事 / 镜头语言完全自由。

| 闸 | 工具 | 拦什么 |
|----|------|--------|
| 出视频锁版机检（硬停） | `tools/prompt_selfcheck.py` | ≥**1000** 中文字 + 六类写作锚（调度 / 机位 / 运镜 / 动作 / 声音 / 对话）、违禁词、时间轴对时；**exit ≠ 0 禁止报价 / 跑**（`shared/red-lines.md`） |
| 矩阵预检 | `tools/pre_gen_gate.py` | 分镜细节、素材关联、剧情核验、场景纯净、**G5 本地项目源**（Notion 非硬闸） |
| 花钱 | `tools/credit_gate.py` | 报价 → **本批账单**用户批准（批准人 + 上限）→ 跑；未批禁止扣费 |
| 广告 | `tools/brand_scan.py` | 品牌 / 商标 / 包装词 |
| 镜级与验真 | `tools/shot_gate.py` / `tools/trust_audit.py` | 逐镜闸、只认提交后新产物 |

## 测试

```bash
python3 -m pytest tests/ -q   # 单测（合规闸 / 品牌扫 / 花钱门 / skill lint）
sh tests/skill-smoke/run.sh   # skill → 指令 全指令验证（不烧积分）
```

`tests/` 与本地 `docs/`（计划 / 上传记录 / 调研归档）**均不上 GitHub**，按 `.gitignore` 留在本机。

## 安装

```bash
git clone git@github.com:nan1010082085/aigc-suite-skills.git ~/aigc-suite-skills

# Claude Code（symlink，git pull 即更新）
for s in ~/aigc-suite-skills/skills/*; do ln -sfn "$s" ~/.claude/skills/$(basename $s); done
ln -sfn ~/aigc-suite-skills/shared ~/.claude/skills/aigc-suite-shared
```

- **Cursor**：把 `skills/` 拷入项目规则目录，`shared/` + `tools/` 放进 vendor 引用路径，在 `AGENTS.md` 标明按各 `SKILL.md` 执行、出图 / 出片过花钱门。
- **Codex**：`cp -r` 整仓到 `vendor/aigc-suite-skills`，在 `AGENTS.md` 按任务路由到对应 `SKILL.md`。
- **整套离线包**：`dist/aigc-suite-skills.zip`（由 `tools/` 打包脚本重建，非上架物）。
- **WorkBuddy**：直接用专家团「漫剧制片厂」或 3 个独立专家（剧本 / 素材 / 虚拟导演）。

## WorkBuddy 交付物（平台侧独立演进）

| 产物 | 版本 | 说明 |
|------|------|------|
| 专家团 `aigc-drama-studio` | 1.1.7 | 11 角色协作，zip 在 `dist/aigc-drama-studio.zip` |
| 独立专家 `drama-episode-writer` / `drama-asset-designer` / `drama-virtual-director` | 1.0.6 | 三个单角色专家，zip 在 `dist/expert-packages/` |

包体由 `tools/build_individual_experts.py` 从仓库一次性取材构建，构建后与仓库独立演进，不随 `git push` 自动变化。4 个包均已注册进本机 `~/.workbuddy/plugins/marketplaces/my-experts/`，并从最终 zip 内逐项复验（平台字段 / 双语 / YAML / 头像 / 引用闭包 / 体积）。

## 用途声明

- `tools/fanqie_ocr.py` 等抽取工具仅用于**个人创作素材的本地抽取**（本地渲染 + 系统 OCR，不做对抗、不分发原文），请遵守来源平台服务条款；本仓库不提供任何绕过付费 / 反爬的对抗手段。
- 示例与文档中的人名 / 道具 / 剧名均为**脱敏占位**；真实剧内数据不在本仓库；`tools/lora_registry.json` 为占位示例，真实注册表存项目侧。
