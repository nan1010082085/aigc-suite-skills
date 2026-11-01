# aigc-suite-skills

漫剧（AI 短剧）创作技能套件：**从小说 / 想法到成片**的 14 个 Claude Code skill，覆盖剧本、分镜、人物 / 场景 / 道具出图、出视频执行、出片质检。

三条主轴：**场景转场连贯 · 剧情分镜 · 人物建模质量**。

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

## Skills

| 链路 | Skill |
|------|-------|
| 剧本 | `novel-to-drama` 小说改编 ｜ `idea-to-drama` 想法原创 |
| 资产 | `character-studio` 人物（基础形象设定卡）｜ `scene-studio` 场景（空镜+光影锁定+镜头变体）｜ `prop-studio` 道具（分类判定+状态变体防穿帮） |
| 分镜 | `storyboard-director` 虚拟导演 + 提示词工程（后端可插拔） |
| 执行 | `video-producer` 出视频（单镜隔离/试产锁参/容错收口） |
| 质检 | `shot-qa` 出片三道闸 + 五道硬闸预检（先检查再花钱） |
| 风格 | `style-cg-refined`（主）/ `style-3d-anime` / `style-anime` / `style-pixar` / `style-cyberpunk` / `style-photoreal` |

## 安装

```bash
# Claude Code（symlink，git pull 即更新）
for s in ~/aigc-suite-skills/skills/*; do ln -sfn "$s" ~/.claude/skills/$(basename $s); done
ln -sfn ~/aigc-suite-skills/shared ~/.claude/skills/aigc-suite-shared
```

Cursor / Codex / DSH 插件安装见 [docs/install.md](docs/install.md)。

## 使用

对话中说「小说改编」「出分镜」「人物出图」「出片检查」等即自动触发对应 skill；也可点名「用 idea-to-drama 原创一部漫剧」。

规则与词典在 `shared/`（硬闸/契约/内核参考/运镜词典/后端方言），机器闸门在 `tools/`（花钱门/品牌扫/提示词自检/五道硬闸 pre_gen_gate），全链流程图见 [docs/flow-map.md](docs/flow-map.md)。

## 用途声明

- `tools/fanqie_ocr.py` 等抽取工具仅用于**个人创作素材的本地抽取**（本地渲染 + 系统 OCR，不做对抗、不分发原文），请遵守来源平台服务条款；本仓库不提供任何绕过付费/反爬的对抗手段。
- 示例与文档中的人名/道具/剧名均为**脱敏占位**（2026-11-01），真实剧内数据不在本仓库；`tools/lora_registry.json` 为占位示例，真实注册表存项目侧。
