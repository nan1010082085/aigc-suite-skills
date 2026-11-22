# 极端角度 REF + 关键 POSE · 验收规程（P1）

> 前置：主体 `CHAR-*-REF-*`（三视图）已 locked。指令骨架见 `character-prompts.md` §1.3b / §1.3c。

## 角度（每主角三张级）

| meta.view | 建议 ID 后缀 | 验收 |
|-----------|--------------|------|
| high_30 | REF-0xx | 俯约 30°；同脸；单人格 |
| low | REF-0xx | 仰拍；同脸；单人格 |
| profile_90 | REF-0xx | 纯侧 90°；同脸；单人格 |

静帧可挂：`shot_use` 可标 `still_ok`；出片仍遵守单镜预算（角度 REF 与身份 REF 二选一为主锚，勿叠两张结构 REF）。

## POSE（仅剧本高频）

从视觉化标注表/剧本动作统计出现 ≥2 次的动作再做。候选：走侧面、走背影、坐起、伸手、对峙站位。

验收：同脸同装；动作可读；单人格；registry `type=pose`。

## 账本

真出记 material-live；未过花钱门不得称通过。
