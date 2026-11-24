---
name: shot-qa
description: 出片前硬停检查——prompt_selfcheck≥1000字+机位运镜锚必须exit0才许报价；零压缩对账；花钱门用户批本批账单；禁止文档自检代替机检。
---

# shot-qa（出片前硬停）

## 红线（先读·违反即停｜2026-11-24）

见 `shared/red-lines.md`。本 skill 只做一件事：**机检未过 = 不许花钱**。

```bash
python3 tools/prompt_selfcheck.py --mode video --duration <秒> <锁版>
# exit ≠ 0 → 停止。禁止 quote / run。
```

不得用「看过了」「差不多够了」绕过退出码。

## 何时使用

- 出图/出视频扣费前
- 用户问能不能出片 / 要检查报告

## 流程（顺序不可换）

1. **机检硬停**：`prompt_selfcheck`（①≥1000 中文字、⑧机位运镜锚、违禁词、对时…）+ 需要时 `pre_gen_gate` / `shot_gate` / `brand_scan`
2. **对账**：生成调用文本 ↔ 本地锁版 SHA 一致（零压缩）
3. **报价**（仅上一步全过）→ **用户批本批账单** → **run** → **验真**（只认提交后新产物）
4. 输出检查报告（字段见 `shared/output-formats.md` §4）

FAIL 打回：分镜→`storyboard-director`；素材→character/scene/prop；剧本→剧本 skill。

## 细则（需要时再读）

- `references/three-gates.md` — 硬停操作细则（账单/对账/挂载；**不能代替**机检退出码）
- `shared/hard-gates.md` — 总纲与出片五律
- `tools/credit_gate.py` / `brand_scan.py` / `shot_gate.py` / `pre_gen_gate.py`

## 产出

LOCKED 检查报告；未过机检不得声称「可以出片」。
