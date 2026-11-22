# 表情单张 EXP · 真出验收规程

> 配合 `character-prompts.md` §1.3 与 `shared/id-and-registry.md`。  
> 成功标准：≥1 主角 6–8 张单张 EXP 过同脸+情绪差；示范镜 refs = 身份 REF + 当前 EXP + LOC。

## 一、发号

| 序号 | emotion | 建议 ID |
|------|---------|---------|
| 1 | 平静 | CHAR-{nnn}-EXP-001 |
| 2 | 微笑 | CHAR-{nnn}-EXP-002 |
| 3 | 大笑 | CHAR-{nnn}-EXP-003 |
| 4 | 愤怒 | CHAR-{nnn}-EXP-004 |
| 5 | 哭泣 | CHAR-{nnn}-EXP-005 |
| 6 | 惊讶 | CHAR-{nnn}-EXP-006 |
| 7 | 不屑 | CHAR-{nnn}-EXP-007 |
| 8 | 低沉 | CHAR-{nnn}-EXP-008 |

## 二、出图前

1. 主体三视图 / 设定卡已 `locked`（REF）
2. 花钱门报价 → 用户批准（`tools/credit_gate.py`）
3. 图生图挂 REF；一情绪一请求；count=1

## 三、验收清单（每张）

- [ ] 画幅与参数符合当期 CLI
- [ ] 与 REF 同脸（发际/眼型/痣/下颌）
- [ ] 情绪标签可读；嘴型显式符合该情绪
- [ ] 单人格、无宫格泄漏、无文字入画
- [ ] 已写入 registry：`type=expression`, `shot_use=video_ref_ok`, `status=locked`
- [ ] 文件路径与 ID 对应（非「最终版」语义名当键）

## 四、示范挂镜（验收文档必写）

```
shot_id: SC-DEMO-SH-001
refs: [CHAR-xxx-REF-001, CHAR-xxx-EXP-004, LOC-xxx]
ref_policy: 只参考五官发型服装与当前愤怒表情；不参考姿势与背景排版
```

禁止示范镜挂全套 8 张 EXP。

## 五、账本

真出结果记入项目 `tests/material-live/` 或剧目验收页：日期、模型、ID、通过/废片原因。未过花钱门不得宣称「已真出通过」。
