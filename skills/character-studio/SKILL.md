---
name: character-studio
description: 漫剧/短剧人物出图 skill——按剧本建人物资产：基础形象设定卡（三视图+头部特写+眼部特写合一身份锚，随剧本阶段演进）为全剧角色参考图唯一入口，表情板/道具卡独立出指令、服装饰品随人物图；装扮变体人物卡、面部身份卡为可替换模块；一致性两层控制保证跨镜同脸同人，出图前置调研后按公式组装即梦/Seedance 等后端的人物生图指令，产出与分镜素材映射对账的人物资产注册。
---

# character-studio（人物出图 · 基础形象设定卡锚点制）

把剧本人物变成**跨镜同人**的图片资产：**基础形象设定卡**锁身份（三视图+头部特写+眼部特写合一），再按出片条件补维——**单张表情 EXP（P0）**、极端角度 REF、POSE、光影 LIT、换装 OUT（见 `references/character-prompts.md` §1.3–1.3e）。编号与挂镜预算见 `shared/id-and-registry.md`。三视图是身份证，不是出片全能锚。

## 何时使用

- 剧本条目产出后，要出人物图、三视图、装扮变体人物卡、表情板、立绘
- 分镜块 `素材映射[]` 点名了人物资产需要建/补/重制
- 用户提到：人物出图 / 三视图 / 表情单张 / 表情表 / 俯仰侧脸 / pose / 服装设定 / 立绘 / 角色一致性

## 流程

1. **读剧本建人物清单 + 出场顺序表 + 发 CHAR ID**：外貌锚点一字不差；主要角色登记表情库 6–8（平静/微笑/大笑/愤怒/哭泣/惊讶/不屑/低沉）；按 `character-asset-system.md` §一 + `shared/id-and-registry.md` 发号
2. **出图前置调研（禁止跳过）**：`shared/pre-gen-research.md` 四步；风格路由按目标脸与材质，国风只定服饰词
3. **基础形象设定卡（身份锚）**：§1.1 三视图+头特写+眼特写；锁定后写入 `CHAR-xxx-REF-*` + visual_id
4. **P0 表情单张 EXP**：§1.3 一情绪一图，真出验收后 `locked`；宫格仅审阅。再按需 §1.2 装扮 / §1.3b 角度 / §1.3c pose
5. **面部身份卡 / 色卡**：§1.4
6. **交付与对账**：assets.json（LOCKED）+ registry（ID）；`素材映射[]` 写 ID；露脸角色全挂

## 硬闸与自检

- **一致性两层控制**（`shared/prompt-formula.md` §二）：人物基准层锁身份 → 场景融合层锁光影——两层缺一必漂。本套主路径=设定卡指令自足 + 按镜挂 REF/EXP + 崩坏重抽；**不依赖训 LoRA**（LoRA 仅其他后端可选，见 `production-priority.md` Skill 边界）。社区/论文天花板讨论见 `character-asset-system.md` §五，不作本 skill 交付承诺
- **文生图/图生图分工**：主体文生图文字控构图；服装/表情/立绘图生图挂主体 + 构图硬锁句（防参考图排版被锚走）
- **广告闸**：手持物/服装商品「素色无品牌+禁包装特写」，出图前后过 `tools/brand_scan.py`
- **花钱门**：扣积分的出图走 `tools/credit_gate.py`（报价→用户批→跑）
- **调用参数**：以**项目声明的生成后端**实时 model list/schema 为准（见 `shared/backends.md`）；提示词优先保留格位和角色锚点，删除重复形容词。图片尺寸、水印和长度按该后端方言，不把别家 API 参数硬套进来；某一后端的 CLI 细则见 `references/character-prompts.md` §2（适配附录，非 skill 本体）。
- **出图验收清单**（`references/character-prompts.md` §4）逐张过：五官锚点/机位正交/服装逐件/手部完整/无品牌/表情差异
- 设定卡模板/排版硬锁/要点：`references/character-prompts.md` §1.1（唯一出处）
- 一枪一停、重制不夹带、验真只认新产物（`shared/hard-gates.md`）
- 违禁词/裸英文过 `tools/prompt_selfcheck.py`（后端方言长度按 `shared/backends.md`）

## 产出与格式

- **assets.json characters[]/outfits[]**：字段名逐字 `shared/output-formats.md` §3 LOCKED 契约（`name/visual_id/three_view/face_card/expressions[]/outfits:[{名, three_view, 配饰}]`）
- **人物生图指令**：五段式组装（`shared/prompt-formula.md` §四），代码块交付，按目标后端方言
- **对账表**：角色 × 出镜镜头 × 挂载节点，交 `shot-qa` 素材校验
