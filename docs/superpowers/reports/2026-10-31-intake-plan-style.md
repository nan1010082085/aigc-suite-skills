# 施工单：风格侧三档入库（style-* 九技能）

- 日期：2026-10-31
- 施工员：intake-style（入库施工·风格侧）
- 喂料：`docs/superpowers/reports/2026-10-31-batch5-style-word-efficacy.md`（15 条标源硬要求，下称「batch5」）
- 目标文件：`skills/style-{3d-anime, anime, cg-refined, comic, cyberpunk, fantasy, infinite-flow, photoreal, pixar}/**`（SKILL.md + references/style-profile.md 各一）
- 流程：**先写施工单（本文件），再按单施工**；施工后在本文件追加「施工日志（逐条）」

## 三档入库口径（用户已批「三档全入库」）

| 档位 | 入库方式 | 文件内标注格式 |
|------|---------|---------------|
| 官方级 | 直接入 | `【官方·出处】` |
| 社区实证级 | 带源入 | `【社区实证·出处】`（新闻实证并入此档，标 `【新闻实证·出处】`） |
| 经验值 | 标【经验·内部】 | 有外部经验源：`【社区经验·出处】`；无出处旧词条：`【经验·内部】`；纯推断：`【推测】`；查无实证：`【查不到】` |

说明：batch5 对 Anifusion 五件套/翻车词的定性是「社区经验（工具方实测）」而非「社区实证」，按铁律③不得升格标注——本单按报告原标注入库（经验级·带源），不写成社区实证。

## 铁律（施工约束）

1. 每条必带来源标注（上表格式）
2. U 级用户令与用户供样例不动（见「不动清单」）
3. 禁编造 batch5 报告外内容
4. 被校正条目留注记（格式：`（2026-10-31 校订：原写「…」→ 依 batch5 §x 改为「…」）`）
5. 逐条日志（本文件末尾「施工日志」）

## 不动清单（明确不施工）

| # | 对象 | 理由 |
|---|------|------|
| N-1 | style-cg-refined 用户 2026-10-27 参考案例、风格定位「设计可假光材质必须真」 | U 级用户令（2026-10-27 主风格钦定） |
| N-2 | style-cyberpunk「朋克家族扩充（2026-10-30 用户方案）」段 | 用户方案原文 |
| N-3 | 各 SKILL.md「禁知名 IP/角色名」硬闸 | U 级硬闸 |
| N-4 | batch5 §2.2「原神风」Genshin Impact 英文锚词 | 与 N-3 冲突（引 IP 名），不入库；如需入库待用户裁定 |
| N-5 | 各 skill 双语示例正文、风格锁模板正文（仅加注记不改写） | 已验收格式/供样例 |
| N-6 | `shared/` 目录（含 backends.md / prompt-formula.md） | 目标范围外；其中 prompt-formula.md 画质词行与本批结论一致，仅记录不改 |
| N-7 | 「即梦网页/App UI 是否有负面框」 | batch5 空白 #1——只标【未定·需一次 UI 实测】，禁写成事实 |

## 条目总表（38 条）

档位统计：官方级 7 / 社区实证级 26 / 经验·内部 5。

### A. style-anime —— 质量词体系修正（核心落点）

| ID | 档位 | 目标文件:位置 | 动作 | 施工内容 | 来源标注 |
|----|------|--------------|------|---------|---------|
| A-01 | 官方级 | style-anime/SKILL.md §流程3 | 修订+注记 | 「Booru 动漫底模 masterpiece 族放最前」→ 位置分底模：Animagine XL 4.0 官方要求质量词**放句尾**（前置会让 artist/风格词失效）；NAI 官方质量词开关也是句尾追加；NAI V3 词序前置强；Pony score 梯子放句首。留校订注记 | 【官方·CagliostroLab】【官方·NAI docs】 |
| A-02 | 官方级 | style-anime/SKILL.md §硬闸「画质词按后端分流」 | 修订 | masterpiece 降级：NAI 体系里是 Aesthetic Tag、仅 V4.5+ 生效；逐词对照 very aesthetic 最强 / amazing quality 显著 / best quality 几乎无效；「强有效」表述删除。Pony 梯子补全 `score_9, score_8_up, score_7_up` + V7 弱化 score 词（改用 score_8/score_7_up）+ `source_/rating_` 仅训练过的模型生效 | 【官方·NAI docs】【社区实证·note.com / artificialguy / Civitai】 |
| A-03 | 社区实证级 | style-anime/SKILL.md description + §硬闸「禁写实词混入」 | 修订+注记 | 「半写实恐怖谷」断言降级为「漂向写实/半写实，易出半写实不协调感」 | 【社区实证·Reddit PSA + Civitai Semi-Realistic Blend XL】 |
| A-04 | 官方级 | style-anime/references/style-profile.md §负面词与画质词策略·画质词分平台 | 重写+注记 | 整条重写为分底模矩阵：①Booru 训练族（NAI/Animagine/Pony）字面训练信号有效；②SDXL base/Flux 弱或反作用（masterpiece 拉向绘画感）；③MJ 完全忽略内联质量词（用 --style raw/--stylize/--quality）；④位置分底模（同 A-01）；⑤masterpiece 降级（同 A-02）；⑥≤3 个（>3–4 稀释注意力、属性泄漏）；⑦8k/4k 只偏置 caption 不改分辨率禁挂；⑧分词 NovelAI 空格/老 Animagine 下划线。留校订注记「原写 masterpiece 强有效且放最前」 | 【官方·NAI docs / CagliostroLab】【社区实证·Promgrammer / note.com】 |
| A-05 | 社区实证级 | style-anime/references/style-profile.md §负面词与画质词策略 | 新增条 | 负面侧质量词（low quality, worst quality, blurry, jpeg artifacts, extra fingers, watermark, text）常比正面质量词更有效，SD 侧优先给负面框 | 【社区实证·Promgrammer】 |
| A-06 | 社区实证级 | style-anime/references/style-profile.md §翻车点表·Pony 行 | 修订 | 补 V7 变化（score 词弱化 → score_8/score_7_up）+ source_/rating_ 仅训练过的模型生效 | 【社区实证·artificialguy / Civitai】 |
| A-07 | 社区实证级 | style-anime/references/style-profile.md §禁写实词条 + §翻车点表「混写实词」行 | 修订+注记 | 「混入=半写实恐怖谷」→「混入→漂向写实/半写实（半写实是真实中间吸引域），易出半写实不协调感」 | 【社区实证·Reddit PSA + Civitai】 |
| A-08 | 官方级 | style-anime/references/style-profile.md §负面词通道 | 修订 | 【即梦无负面框·推测】→「（官方：火山 API 无 negative_prompt 参数 2026-10）」；网页/App UI 层标【未定·需一次 UI 实测】；MJ `--no` 补官方定性：nudge 非绝对过滤、正文写 "no X" 无效、点名某物罕见反引入、逗号分隔置尾 | 【官方·volcengine】【官方·MJ docs（403，镜像交叉）】 |

### B. style-3d-anime —— 重点补料（现 23 条全无出处）

| ID | 档位 | 目标文件:位置 | 动作 | 施工内容 | 来源标注 |
|----|------|--------------|------|---------|---------|
| B-01 | 经验·内部（带源） | style-3d-anime/references/style-profile.md 新节 | 新增 | cel-shading 锁质感五件套：`cel-shaded`、`two-tone shadow blocks`、`ink line outline`、`flat color fields`、明确光向（`top-left key light`）+ `rim light`，附英文词表与用法（锁 3D 渲染转赛璐璐观感：硬轮廓/2–3 档色块阴影/高饱和平涂/极少渐变） | 【社区经验·Anifusion（工具方实测）】 |
| B-02 | 经验·内部（带源） | 同上节 | 新增 | 明文翻车词：`soft-glow`、`painterly` 修饰词——"they fight the look"，与 cel 质感直接对冲，禁入本风格段 | 【社区经验·Anifusion】 |
| B-03 | 社区实证级 | 同上节 | 新增 | halftone（西漫）与 screentone（日漫）是两种印刷传统，禁混写（halftone+manga 混写尤其糟），commit 其一 | 【社区实证·artpromptsgenerator】 |
| B-04 | 社区实证级 | style-3d-anime/references/style-profile.md 风格锁模板「次表面散射」行 + 高效组合 SSS 行 | 标注 | SSS 标「跨模型借用」：SD 系写实侧有效（含推近+柔背光副作用）【社区实证】；Flux 单词弱、需 SSS LoRA【社区实证·旁证】；**Seedream/即梦/MJ、SDXL 动漫侧无任何 A/B 实证（空白）**【查不到】 | 【社区实证·Reddit r/StableDiffusion + Civitai SSS LoRA】【查不到】 |
| B-05 | 经验·内部 | style-3d-anime/references/style-profile.md 高效组合「材质」「皮肤/毛发」行 | 标注 | 织物纹理/皮革质感/金属反光归 intricate_details 族，过用产生 busy 的「AI 感」纹理【社区实证·Promgrammer】；「发丝根根分明」无对照实证，标经验写法 | 【社区实证·Promgrammer】【经验·内部】【查不到】 |
| B-06 | 社区实证级 | style-3d-anime/references/style-profile.md §边界词表 | 修订+注记 | 「写实词混入→日漫脸被写实化，恐怖谷」→「→漂向写实/半写实，易出半写实不协调感」（留校订注记）；「赛璐璐混入→3D 压平成 2D」后果列【推测】（机理自洽无直接 A/B） | 【社区实证·Reddit PSA + Civitai】【推测】 |
| B-07 | 经验·内部 | style-3d-anime/references/style-profile.md §翻车点表「脸部日漫锚词前置」行 | 注记 | 「前置」仅 NAI 类底模有据；Animagine XL 4.0 官方主张质量词句尾（顺序敏感模型前置一般更强但会打崩 artist/风格词）；即梦/Seedream 上前置效果无实证 | 【官方·CagliostroLab】【查不到】 |
| B-08 | 社区实证级 | style-3d-anime/references/style-profile.md §翻车点表 | 新增行 | 风格词在自然语言底模锁不住时，社区答案是 LoRA（SD 侧 3DMM LoRA trigger `3DMM`；Flux 侧 Cel Shading Style LoRA） | 【社区实证·Civitai + stable-diffusion-art】 |
| B-09 | 经验·内部 | style-3d-anime/SKILL.md §硬闸前两条 | 标注 | 「禁写实真人词混入」补「易出半写实不协调感」；「禁 2D 平涂词混入→压平成 2D」标【推测】 | 【社区实证·Reddit PSA】【推测】 |

### C. style-comic —— 词库带源补强

| ID | 档位 | 目标文件:位置 | 动作 | 施工内容 | 来源标注 |
|----|------|--------------|------|---------|---------|
| C-01 | 社区实证级 | style-comic/references/style-profile.md | 扩写 | 美漫三件套带源补强：`bold ink outlines` + `flat cel color` + `halftone/Ben-Day dots`；补「时代词」维度（golden-age halftone / 90s grim-dark / modern flat digital / ligne claire）；动态镜头（low angle / Dutch tilt）+ speed lines/action lines 比形容词更能卖能量感 | 【社区实证·artpromptsgenerator】 |
| C-02 | 社区实证级 | style-comic/references/style-profile.md | 新增+注记 | halftone（西漫）/screentone（日漫）禁混写，commit 其一；现模板「halftone effect + manga aesthetic」属混写，留注记提示出图时择一 | 【社区实证·artpromptsgenerator】 |
| C-03 | 社区实证级 | style-comic/references/style-profile.md §负面词 | 标注 | 负面词 `3D, realistic` 无专门实证【查不到】；MJ `--no`=nudge 非绝对、正文 "no X" 无效【官方】；MJ comic book style 是 Midlibrary 实测大类（525 styles / 249 SREF codes） | 【官方·MJ docs+镜像】【社区实证·Midlibrary】【查不到】 |
| C-04 | 社区实证级 | style-comic/SKILL.md | 修订 | stub 补一行：指向带源词库（三件套+时代词）与 halftone/screentone 禁混写提示 | 【社区实证·artpromptsgenerator】 |

### D. style-fantasy

| ID | 档位 | 目标文件:位置 | 动作 | 施工内容 | 来源标注 |
|----|------|--------------|------|---------|---------|
| D-01 | 社区实证级（新闻） | style-fantasy/references/style-profile.md（原 Greg Rutkowski 位） | 注记 | P0 已删画师名；原位补注记：画师名增强=SD1.5 时代过时写法，SD 2.0 起移除在世艺术家风格模仿，禁作通用增强词（社区靠 LoRA 复活该风格） | 【新闻实证·decrypt / BBC】 |
| D-02 | 社区实证级 | style-fantasy/references/style-profile.md 词库行 | 标注 | 词库主体（epic lighting / intricate armor / fantasy concept art / oil painting style / dark fantasy）在 MJ/SD fantasy prompt 库通用；intricate details 过用 busy【社区实证·Promgrammer】 | 【社区经验·promptspace / therightgpt】【社区实证·Promgrammer】 |
| D-03 | 社区实证级 | style-fantasy/SKILL.md | 修订 | stub 补一行画师名禁令注记（同 D-01 口径） | 【新闻实证·decrypt / BBC】 |

### E. style-infinite-flow —— 补实证词库

| ID | 档位 | 目标文件:位置 | 动作 | 施工内容 | 来源标注 |
|----|------|--------------|------|---------|---------|
| E-01 | 社区实证级 | style-infinite-flow/references/style-profile.md | 新增 | M.C. Escher = 不可能空间风格锚（`Escher-inspired spatial paradox`，训练数据标注率高） | 【社区实证·flowpixai】 |
| E-02 | 社区实证级 | 同上 | 新增 | 五类循环空间词组：Möbius strip corridor / Penrose staircase / infinite reflections（镜像递归）/ fractal-like nested spaces / fragments from different time periods | 【社区实证·flowpixai】 |
| E-03 | 社区实证级 | 同上 | 新增 | glitch 词表：RGB channel shift, datamosh, scanlines, pixel sorting, databending, corrupted signal, compression artifact；Sci-Fi HUD / system UI overlay 词条 | 【社区实证·designstylebook】【社区经验·completeaitraining】 |
| E-04 | 社区实证级 | 同上 | 新增 | 一人多身（同一角色多版本同框 + glowing temporal threads）；时空间隙（a crack in reality / temporal energy）；异化时钟 | 【社区实证·flowpixai】 |
| E-05 | 社区实证级 | 同上 | 新增 | 多副本统一靠「贯穿性视觉锚点」而非统一画风；副本风格多样性词例（pastel gothic horror / cyberpunk xianxia / wasteland amusement park） | 【社区实证·flowpixai】 |
| E-06 | 社区实证级 | 同上 | 新增 | 无限流≠赛博朋克：前者是多世界切换机制，视觉重点在**过渡空间**（门/电梯/走廊/屏幕） | 【社区实证·flowpixai】 |
| E-07 | 社区实证级 | 同上 §负面词 | 标注 | 现有词（dimensional rift / portal / space distortion / floating data codes / system UI overlay）方向对、原无出处——对照补标；负面词行补 MJ `--no` nudge 事实 | 【社区实证·flowpixai】【官方·MJ docs+镜像】 |

### F. 负面词平台事实（其余 3 处【推测】升级）

| ID | 档位 | 目标文件:位置 | 动作 | 施工内容 | 来源标注 |
|----|------|--------------|------|---------|---------|
| F-01 | 官方级 | style-cyberpunk/references/style-profile.md §负面词通道 | 修订 | 【即梦无负面框·推测】→「（官方：火山 API 无 negative_prompt 参数 2026-10）」+ UI 层【未定·需一次 UI 实测】+ MJ `--no` nudge 定性 | 【官方·volcengine】【官方·MJ docs+镜像】 |
| F-02 | 官方级 | style-photoreal/references/style-profile.md §负面词通道 | 修订 | 同 F-01 | 同 F-01 |
| F-03 | 官方级 | style-pixar/references/style-profile.md §负面词通道 | 修订 | 同 F-01 | 同 F-01 |

### G. 其余 skill 来源标注补齐

| ID | 档位 | 目标文件:位置 | 动作 | 施工内容 | 来源标注 |
|----|------|--------------|------|---------|---------|
| G-01 | 社区实证级 | style-photoreal/references/style-profile.md + SKILL.md | 标注 | 「masterpiece 在 SDXL 拉向绘画」「MJ 忽略内联质量词」「负面质量词常比正面管用」补源标注（原引研究 §3 的结论与 batch5 一致） | 【社区实证·Promgrammer】 |
| G-02 | 社区实证级 | style-pixar/references/style-profile.md + SKILL.md | 标注 | SSS 行标「跨模型借用」口径（同 B-04：SD 写实侧有效、Flux 弱、Seedream/即梦/MJ 无实证空白）；「masterpiece 拉向画廊绘画」补源 | 【社区实证·Reddit】【社区实证·Promgrammer】【查不到】 |
| G-03 | 社区实证级 | style-cg-refined/references/style-profile.md §翻车点表 | 标注 | 「8k/ultra-detailed 堆砌弱偏置且稀释注意力」补源；新增注记：intricate details / super detail 族过用产生 busy 的 AI 感纹理 | 【社区实证·Promgrammer】 |
| G-04 | 社区实证级 | style-cyberpunk/references/style-profile.md + SKILL.md | 标注 | 「8k/RAW/masterpiece 在 Flux/GPT/即梦/MJ 是噪声」补源 | 【社区实证·Promgrammer】 |

## 施工顺序

1. A 组（style-anime 核心修正）→ 2. B 组（style-3d-anime 补料）→ 3. C/D/E 组（三个 stub 词库）→ 4. F 组（负面词平台事实）→ 5. G 组（标注补齐）→ 6. 回填施工日志。

---

## 施工日志（逐条）

施工时间：2026-10-31。全部 38 条执行完毕，逐条结果如下（✔=已入库；文件路径均相对 `skills/`）：

| ID | 结果 | 落点摘要 |
|----|------|---------|
| A-01 | ✔ | style-anime/SKILL.md §流程3「放最前」→「位置分底模」（Animagine 4.0 句尾/NAI 开关句尾/NAI V3 前置/Pony 句首）+ 校订注记 |
| A-02 | ✔ | style-anime/SKILL.md §硬闸：masterpiece 降级（Aesthetic Tag V4.5+；very aesthetic 最强/amazing quality 显著/best quality 几乎无效）+ score_9/8_up/7_up、V7 弱化、source_/rating_ 限定 + 校订注记 |
| A-03 | ✔ | style-anime/SKILL.md description + §硬闸：「半写实恐怖谷」→「漂向写实/半写实，易出半写实不协调感」+ 校订注记 |
| A-04 | ✔ | style-anime/profile「画质词分平台」整条重写为 8 点分底模矩阵（适用域/masterpiece 降级/位置/≤3/Pony/8k 禁/分词）+ 校订注记 |
| A-05 | ✔ | style-anime/profile 新增「负面侧质量词更有效」条 |
| A-06 | ✔ | style-anime/profile 翻车点 Pony 行补 V7 + source_/rating_ |
| A-07 | ✔ | style-anime/profile「禁写实词条」+ 翻车点行降级「恐怖谷」+ 校订注记 |
| A-08 | ✔ | style-anime/profile 负面词通道：【即梦无负面框·推测】→ 官方 API 事实 + UI【未定·需一次 UI 实测】+ MJ --no nudge 定性 + 校订注记 |
| B-01 | ✔ | style-3d-anime/profile 新节「cel-shading 锁质感词库」：五件套（cel-shaded/two-tone shadow blocks/ink line outline/flat color fields/光向+rim light）【社区经验·Anifusion】 |
| B-02 | ✔ | 同节明文翻车词 soft-glow/painterly（"they fight the look"） |
| B-03 | ✔ | 同节 halftone（西漫）/screentone（日漫）禁混写、commit 其一 |
| B-04 | ✔ | style-3d-anime/profile 词效标注 + 模板词效标注：SSS=跨模型借用（SD 写实侧有效/Flux 弱需 LoRA/Seedream·即梦·MJ·SDXL 动漫侧空白【查不到】） |
| B-05 | ✔ | 词效标注：intricate 族过用 busy【社区实证】；「发丝根根分明」【经验·内部】【查不到】 |
| B-06 | ✔ | 边界词表：「恐怖谷」降级 + 校订注记；「赛璐璐压平」列【推测】；新增 soft-glow/painterly、halftone/screentone 混写两行 |
| B-07 | ✔ | 翻车点「脸部日漫锚词前置」注记：前置仅 NAI 类有据、Animagine 官方句尾、即梦/Seedream【查不到】 |
| B-08 | ✔ | 翻车点表新增行：词锁不住→LoRA（3DMM / Cel Shading Style）【社区实证】 |
| B-09 | ✔ | style-3d-anime/SKILL.md 硬闸：「恐怖谷」降级、「压平」标【推测】、新增禁翻车词条 |
| C-01 | ✔ | style-comic/profile 扩写：美漫三件套 + 时代词四类 + 动态镜头【社区实证·artpromptsgenerator】+ Midlibrary |
| C-02 | ✔ | style-comic/profile 禁混写节：现模板「halftone+manga aesthetic」混写留注记、出图 commit 其一 |
| C-03 | ✔ | style-comic/profile 负面词注记：`3D, realistic`【查不到】+ MJ --no nudge【官方】+ 即梦 API 事实 |
| C-04 | ✔ | style-comic/SKILL.md stub 补三件套+时代词+禁混写一行 |
| D-01 | ✔ | style-fantasy/profile 原 Rutkowski 位注记：画师名增强=SD1.5 过时写法【新闻实证·decrypt/BBC】 |
| D-02 | ✔ | style-fantasy/profile 词库主体标源 + intricate details 过用 busy 注记 |
| D-03 | ✔ | style-fantasy/SKILL.md stub 补画师名禁令一行 |
| E-01 | ✔ | style-infinite-flow/profile 新增 M.C. Escher 不可能空间锚 |
| E-02 | ✔ | 五类循环空间词组表（莫比乌斯/彭罗斯/镜像递归/嵌套走廊/时空碎片） |
| E-03 | ✔ | glitch 词表 7 词 + Sci-Fi HUD/system UI overlay |
| E-04 | ✔ | 一人多身（glowing temporal threads）+ 时空间隙 + 异化时钟 |
| E-05 | ✔ | 多副本「贯穿性视觉锚点」手法 + 副本风格多样性词例 |
| E-06 | ✔ | 无限流≠赛博朋克、视觉重点在过渡空间（门/电梯/走廊/屏幕） |
| E-07 | ✔ | 既有词「方向对但原无出处」对照注记 + 负面词通道注记（MJ --no + 即梦 API） |
| F-01 | ✔ | style-cyberpunk/profile【即梦无负面框·推测】→ 官方 API 事实 + UI 未定 + MJ --no 定性 + 校订注记 |
| F-02 | ✔ | style-photoreal/profile 同上 |
| F-03 | ✔ | style-pixar/profile 同上 |
| G-01 | ✔ | style-photoreal profile+SKILL.md：masterpiece/SDXL 拉向绘画、MJ 忽略内联质量词、负面质量词更有效补源【社区实证·Promgrammer】 |
| G-02 | ✔ | style-pixar profile+SKILL.md：SSS 跨模型借用标注（同 B-04 口径）+ masterpiece 拉向画廊绘画补源 |
| G-03 | ✔ | style-cg-refined/profile 翻车点表：8k/ultra-detailed 弱偏置补源 + intricate details 过用 busy 补注 |
| G-04 | ✔ | style-cyberpunk profile+SKILL.md：「8k/RAW/masterpiece 是噪声」补源 |

### 施工备注

1. **Anifusion 五件套/翻车词档位说明**：team-lead 口述为「社区实证」，batch5 报告原标注为【社区经验/工具方实测】——按铁律③以报告为准入库，文件内标【社区经验·Anifusion】（经验级·带源），未升格为社区实证。
2. **pixar 负面词表中的「恐怖谷」词条未改**（style-pixar/profile 负面框词表与翻车点行）：那是负面框词条/翻车点名用法，非「写实词混入→恐怖谷」因果断言（该断言已按 A-03/A-07/B-06 全部降级）；该行原本已标（无出处）。
3. **N-4（原神锚词）未入库**：与「禁知名 IP/角色名」U 级硬闸冲突，待用户裁定。
4. `shared/` 未动（范围外）；`shared/prompt-formula.md` 画质词行与本批结论方向一致，无需修订。
5. 验证命令复核：`放最前`、`即梦无负面框·推测`、`恐怖谷` 在 skills/style-* 下的残留仅存在于校订注记文本中，正文断言已全部替换。
