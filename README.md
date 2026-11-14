# aigc-suite-skills

漫剧（AI 短剧）创作技能套件：**从小说 / 想法到成片**的 18 个 Claude Code skill，覆盖剧本、素材（人物 / 场景 / 道具）、分镜、出视频执行、出片质检、成片回流。

三条主轴：**场景转场连贯 · 剧情分镜 · 人物建模质量**。

> 🆓 **已上架 WorkBuddy 专家团「漫剧制片厂」（免费）**——多角色协作团队（11 agents + 18 skills）在 WorkBuddy 开放平台「专家」货架可直接安装使用。专家团是平台侧独立交付物，与本仓库独立演进（打包与维护见 [docs/WorkBuddy专家团与Skill包上传指南.md](docs/WorkBuddy专家团与Skill包上传指南.md)）。

## 流水线

```
小说 ─→ novel-to-drama ─┐
                        ├─→ 剧本条目 ─→ 素材层 ─→ 分镜层 ─→ 出片（执行顺序：剧本→素材→分镜，2026-10-30 用户重排）
想法 ─→ idea-to-drama  ─┘      │            │          │
                    character-studio ─→ 人物资产 ──┤ storyboard-director ─→ 分镜块
                    scene-studio ────→ 场景资产 ──┤  （@引用全指向已建资产）
                    prop-studio ─────→ 道具资产 ──┤  prompt_compiler ─→ 出图/视频指令
                    lora_registry（视觉元数据）──┘  （LoRA/触发词/权重自动编译）
        style-*（风格段，一部剧锁 1 种）
                    clip-review（成片核验与回流：五项核验→缺陷归因→规则回流，一次翻车=一条新规）────────────────────────────────────────┤
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
| **人物** | 基础形象设定卡 = **三视图 + 头部特写 + 眼部特写**（7–8 面板，纯白/影棚底，标准A站姿） | **表情板**以设定卡为基础**单独出指令**（i2i 挂设定卡，6–8 格绑定识别点）；**装扮变体卡** = 人物图换装出卡，**时期×装扮双轴**随剧情演进成图鉴（优点标配） | 服装饰品（头戴/耳饰/颈饰）**随人物图**画上身，不单独出服装图/饰品图 |
| **道具** | **关键性准入**：只有承载剧情/线索/身份/情绪/特写记忆点的道具才出卡；一张**主视图为主**（**不需三视图**，复杂道具按需加辅助视图） | 状态变体走 i2i（`道具名-状态`，一状态一素材） | 普通物件不出卡，出视频时文字描述带过；固定装饰画进场景 |
| **场景** | 空镜 + 光影锁定 | 镜头变体（同场景多机位） | 不放人（有人场景不能用于出视频） |

设定卡是出视频时**角色参考图唯一入口**；所有露脸角色/场景/关键道具必须挂资产节点（素材关联硬闸）。

## 校验体系：合规闸，不是创作闸

> **最高原则（2026-11-05 用户令）**：一切检查、校验是**合规**，不是限制模型、限制发挥、限制创作。每条检查的准入标准只有一个——「不拦会有什么合规/资损后果」。字数无上限、题材/风格/叙事/镜头语言完全自由。

| 闸 | 工具 | 拦什么 |
|----|------|--------|
| 提示词合规闸（7 项机检） | `tools/prompt_selfcheck.py` | 平台违禁词、裸英文运镜、多镜缺时间码、refs>9、重复块（拼装手误）、每镜 <250 字信息量保底、**时间轴不对时**（分镜时间覆盖≠生成时长±0.5s——超出内容会被模型压缩/砍掉，成片 ffprobe 实测） |
| 出图/出视频五道硬闸 | `tools/pre_gen_gate.py` | 分镜细节保底、素材关联（不关联=浪费积分）、剧情核验、场景纯净（只用空镜）、Notion 先行 |
| 花钱门 | `tools/credit_gate.py` | 扣积分生成必须先报价、用户批准才跑，一枪一停 |
| 广告闸 | `tools/brand_scan.py` | 品牌/商标/包装词（道具一律素色化） |

## 测试

```bash
python3 -m pytest tests/ -q   # 36 项单测（合规闸/品牌扫/花钱门/skill lint）
sh tests/skill-smoke/run.sh   # skill → 指令 全指令验证：两套不同剧本 × 五类指令共 7 份，逐份过合规闸（不烧积分）
```

skill-smoke 验证的是不同剧本能产出不同指令，以及这些指令通过合规与格式检查；它不证明模型生成后的画面质量。素材测试按「skill → 指令 → 单张实际生成 → 逐项验收」记录首次结果；同一冻结版本独立重复后，才能估计首张通过概率。苗疆七格人物卡的测试口径与失败账本见 tests/material-live/，该目录按 .gitignore 留在本机。

## 安装

```bash
# Claude Code（symlink，git pull 即更新）
for s in ~/aigc-suite-skills/skills/*; do ln -sfn "$s" ~/.claude/skills/$(basename $s); done
ln -sfn ~/aigc-suite-skills/shared ~/.claude/skills/aigc-suite-shared
```

Cursor / Codex / DSH 插件安装见 [docs/install.md](docs/install.md)；不想手动装就直接用 WorkBuddy 专家团「漫剧制片厂」（免费）。

## 使用

对话中说「小说改编」「出分镜」「人物出图」「出片检查」等即自动触发对应 skill；也可点名「用 idea-to-drama 原创一部漫剧」。

规则与词典在 `shared/`（硬闸/契约/风格库/运镜词典/后端方言/经验回流），机器闸门在 `tools/`（花钱门/品牌扫/提示词自检/五道硬闸 pre_gen_gate），全链流程图见 [docs/flow-map.md](docs/flow-map.md)。

## 用途声明

- `tools/fanqie_ocr.py` 等抽取工具仅用于**个人创作素材的本地抽取**（本地渲染 + 系统 OCR，不做对抗、不分发原文），请遵守来源平台服务条款；本仓库不提供任何绕过付费/反爬的对抗手段。
- 示例与文档中的人名/道具/剧名均为**脱敏占位**（2026-11-01），真实剧内数据不在本仓库；`tools/lora_registry.json` 为占位示例，真实注册表存项目侧。
