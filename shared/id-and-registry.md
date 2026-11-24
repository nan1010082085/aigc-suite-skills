# 编号 · Registry · 结构化指针 · 溯源

> 2026-11-21 定稿（Skills 打磨计划）。全 skill 新产出强制；存量渐进迁移。  
> **SC = 集（Episode），LOC = 场景（Location）**——禁止把 SC 当成场景。

## 一、原则

1. **ID 无意义但唯一**：编号永不改；显示名/情绪/机位说明只住 registry。
2. **禁人肉语义文件名当身份**：`张三_三视图_正面_最终版.png` 可作人读别名，权威身份仍是 ID。
3. **引用用结构化指针**：禁「参考张三的三视图正面」字符串匹配。
4. **画布 node / 提示词「参考图 N」**：仅提交瞬时映射，禁止当跨步骤身份。
5. **LOCKED 字段名**仍以 `output-formats.md` 为准；本文件是 **ID 寻址层**，与 `name`/`visual_id`/`素材映射[]` 并存——`素材映射[]` 与 refs 必须写 ID（可附 display_name 注释，机器只认 ID）。

## 二、ID 形态

| ID | 含义 |
|----|------|
| `CHAR-001` | 角色实体 |
| `CHAR-001-REF-001` | 结构参考（三视图格/角度等，type 在 registry） |
| `CHAR-001-EXP-001` | **单张**表情（出片按镜挂） |
| `CHAR-001-POSE-001` | 动作姿态参考 |
| `CHAR-001-OUT-001` | 服装套 |
| `CHAR-001-LIT-001` | 光影条件变体（按需） |
| `SC-003` | 第 3 **集** |
| `SC-003-SH-002` | 第 3 集第 2 **镜** |
| `LOC-002` | 场景空间 |
| `PROP-005` | 道具 |
| `SCRIPT-v2.3` | 剧本版本 |
| `SC-003-SH-002-gen-001` | 该镜生成物第 1 代（返工只升 gen） |

编号规则：前缀大写 + 连字符 + 零填充三位序号；子资源在父 ID 后追加 `-TYPE-nnn`。

## 三、Registry 记录字段（每条资产必填）

```json
{
  "id": "CHAR-001-EXP-002",
  "type": "expression",
  "display_name": "张三_愤怒",
  "parent_id": "CHAR-001",
  "file": "assets/CHAR-001/EXP-002.png",
  "version": 1,
  "status": "locked",
  "meta": {
    "emotion": "愤怒",
    "shot_use": "video_ref_ok"
  }
}
```

| 字段 | 说明 |
|------|------|
| `id` | 永不改 |
| `type` | `character` / `ref` / `expression` / `pose` / `outfit` / `lighting` / `location` / `prop` / `episode` / `shot` / `script` / `generation` |
| `display_name` | 人读名；可改 |
| `parent_id` | 归属（EXP/REF 的 parent 为 CHAR） |
| `file` | 当前文件路径或 URI；换图只改这里 |
| `version` | 文件代数；换图 +1 |
| `status` | `draft` / `locked` / `retired` |
| `meta` | 类型专有（情绪、角度、光影 key 等） |

示例整表见 `asset-registry.example.json`。

## 四、结构化指针（分镜 / 出片）

```json
{
  "shot_id": "SC-003-SH-002",
  "refs": ["CHAR-001-REF-001", "CHAR-001-EXP-002", "LOC-002"],
  "ref_policy": "只参考五官发型服装与当前表情；不参考姿势与背景排版"
}
```

禁：`素材映射: ["张三三视图正面"]`。  
要：`素材映射` / `refs` 写 ID 列表。

## 五、单镜挂载预算（防多参考杀构图）

默认每镜最多：

1. 身份结构：`CHAR-*-REF-*` **或** 该镜服装 `CHAR-*-OUT-*` 对应 REF **1 张**
2. 当前情绪：`CHAR-*-EXP-*` **至多 1 张**
3. 场景：`LOC-*` 空镜 **1 张**
4. 关键道具：`PROP-*` 按需，总 refs 遵守后端上限（常见 ≤9）

禁止：一镜挂全套 EXP / 全角度 REF。  
九宫格表情板用于**生产与审阅**；出片 refs **不得**挂整表，只挂裁切后的单张 EXP（见 `character-studio/references/character-prompts.md` §1.3）。

## 六、溯源链

```
SC-003-SH-002-gen-001
  ← shot_id: SC-003-SH-002
    ← episode_id: SC-003
      ← script_id: SCRIPT-v2.3
        + refs: [...]
```

生成物文件名推荐：`{shot_id}-gen-{nnn}.ext`；或旁路 sidecar JSON 同名 `.meta.json` 写全链。返工只新建 `gen-00n+1`，不改 SH/SC/SCRIPT。

## 七、与旧命名对照（迁移）

| 旧习惯 | 新做法 |
|--------|--------|
| `张三_三视图_正面_最终版.png` | `CHAR-001-REF-001` + registry.display_name |
| `第3集_生气_中景_02.png` | `SC-003-SH-002-gen-002` |
| 分镜写「参考张三正面」 | `refs: ["CHAR-001-REF-001"]` |
| `visual_id` / `node_xxx` | 保留为画布瞬时句柄；跨文档仍用 CHAR/REF/EXP ID |
