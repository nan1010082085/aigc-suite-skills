# 批次 5 调研报告：风格词效实证（Booru 质量词 / cel-shading / 边界词 / 材质词 / 三风格词库 / 负面词平台事实）

- 日期：2026-10-31
- 调研员：research-b5（风格词效实证）
- 方法：中英双语检索约 17 组（EN 11 / CN 6），深度抓取 12 页以上；每条结论标来源 URL 与性质（**官方** / **社区实证** / **推测** / **查不到**）
- 校准对象（只读，未修改）：`skills/style-anime`、`skills/style-3d-anime`、`skills/style-comic`、`skills/style-fantasy`、`skills/style-infinite-flow`

来源性质标注：【官方】=平台/模型方文档；【社区实证】=带对照/实测的社区内容；【社区经验】=社区普遍说法无严格对照；【推测】=本报告推断；【查不到】=检索无果，明说。

---

## ① Booru 质量词/风格词效对照（校准 style-anime）

### 1.1 NovelAI 官方体系：masterpiece 不是「质量词」，是「美学词」，且 V4.5+ 才有

【官方】NovelAI 现行文档把特殊标签分四类，`masterpiece` 归 **Aesthetic Tags** 且注明 **"masterpiece (V4.5 or higher only)"**：

- Quality Tags：`best quality / amazing quality / great quality / normal quality / bad quality / worst quality`
- Aesthetic Tags：`masterpiece`（V4.5+）、`top aesthetic`（V4+）、`very aesthetic`、`aesthetic displeasing`、`very displeasing`
- Complexity Tags（V5）：`low/medium/high/ultra complexity`；Year Tags：`year XXXX`；Dataset Tags：`fur dataset` 等
- 词序（V3 及以下）：**越靠前权重越强**；推荐顺序 `1boy/1girl, characters, series, 其余`
- 来源：https://docs.novelai.net/en/image/tags/ 【官方】

### 1.2 NAI 质量词开关的官方行为是「追加到提示词末尾」，且逐词实测差异巨大

【社区实证】note.com 的 NAI 对照实验（同 seed 只换质量词）：

- NAI Anime V3 打开 Quality Tags 时官方追加的是 **`best quality, amazing quality, very aesthetic, absurdres`，加在提示词末尾**（不是句首）
- 逐词 2 倍加权对照：**`very aesthetic` 效果最强**（细节/构图/色调全动）；`amazing quality` 效果显著（会改画风）；**`best quality` 几乎无变化**；`absurdres` 几乎无变化、主观感觉质量反而降
- 质量词整体作用：发丝/眼睛/背景细节增加、色调变淡、阴影更利；**极端加权会强烈「AI 生成感」**——可反向故意不加来保留个性
- 来源：https://note.com/nai_researchnote/n/nbf34d1edf269 【社区实证】

### 1.3 「只在动漫底模生效」方向正确，但强弱要分模型写清

【社区实证】Promgrammer《Quality Tags — A Deep Dive》（固定 seed 对照 + 模型矩阵）：

- Booru 训练族（NovelAI/Animagine/Pony）：质量词是字面训练信号，有效
- **SDXL base / Flux：弱、甚至反作用**——`masterpiece` 会把画面拉向绘画感、远离摄影感；写实目标应改用相机词（85mm lens, Kodak Portra 400）
- **Midjourney：完全忽略内联质量词**，用 `--style raw / --stylize / --quality`
- 固定 seed 实测（Illustrious v3.0）：**成熟强底模上，质量词组造成的画面位移小于随机 token**（噪声地板以下）；弱底模/老底模/低步数时才更有效
- **>3–4 个质量词开始稀释注意力、可能属性泄漏**；`8k/4k` 只偏置训练 caption、不改分辨率
- **负面侧质量词（low quality, worst quality, blurry）常比正面质量词更有效**
- 分词：NovelAI 用空格、老 Animagine 用下划线，随底模而定
- 来源：https://www.promgrammer.com/en/guides/quality-tags-deep-dive 【社区实证】；模型差异另见 https://insiderllm.com/guides/best-anime-stylized-checkpoints-local-image-generation/ 【社区经验】

### 1.4 「放最前」是分模型命题，style-anime 现文写死了，需修正

- NAI V3 词序：越靠前越强（官方）；但 **NAI 官方质量词开关追加在末尾**（1.2）
- **Animagine XL 4.0 官方指南（模型训练方 CagliostroLab）明确要求质量词放句尾**：`masterpiece, high score, great score, absurdres` 放前面会让 artist tags 失效、概念/画风出错——训练时质量词从未放在句首
- Pony：score 梯子 `score_9, score_8_up, score_7_up` 放句首；**Pony V7 弱化 score 词，改用 `score_8`/`score_7_up`**；`source_*`/`rating_*` 只在训练过的模型生效
- 来源：https://cagliostrolab.net/posts/optimizing-animagine-xl-40-in-depth-guideline-and-update 【官方（模型方）】；https://artificialguy.com/blog/pony-illustrious-prompt-syntax/ 、https://civitai.com/articles/4248/what-is-score9-and-how-to-use-it-in-pony-diffusion 【社区实证】

### 1.5 对 style-anime 现有断言的逐条裁定

| 现文断言（style-anime） | 裁定 |
|---|---|
| 「Booru 质量词只在动漫底模生效」 | **基本成立**，补细则：SDXL/Flux 弱或反作用、MJ 忽略【社区实证】 |
| 「masterpiece/best_quality 强有效且 ≤3 个」 | **半对**：≤3 个对（>3 稀释）；「强有效」过头——强底模边际效应可小于随机 token，且 NAI 体系里真正强的是 `very aesthetic`/`amazing quality`【社区实证】 |
| 「放最前」 | **分模型**：NAI V3 前置强；Animagine 4.0 官方要求放句尾；NAI 官方开关追加句尾【官方】 |
| 「Pony 系改用 score_9, score_8_up」 | **成立**，补 V7 变化：score 词弱化，用 score_8/score_7_up【社区实证】 |
| 「NovelAI 空格、老 Animagine 下划线」 | **成立**【社区实证】 |
| 「禁统一挂 8k/RAW」 | **成立**：8k 只偏置 caption；写实侧用相机词【社区实证】 |

---

## ② cel-shading / 3D 日漫 CG 风格词效（校准 style-3d-anime）

### 2.1 cel-shading 锁质感词与翻车词（社区实证）

【社区经验/工具方实测】Anifusion cel-shading 风格页（含示例 prompt 全文）：

- **锁质感词**：`cel-shaded`、`two-tone shading / two-tone shadow blocks`、`ink line outline`（1-pixel matte ink contours）、`flat color fields`、`rim light only`、明确光向（`top-left key light`）、`halftone screentone`
- **翻车词（明说要避开）**：**soft-glow、painterly 修饰词**——「they fight the look」，与 cel 质感直接对冲
- cel-shading 定义：3D 渲染主体转平涂手绘赛璐璐观感——硬轮廓、2–3 档色块阴影、高饱和平涂、极少渐变
- 来源：https://anifusion.ai/style/cel-shading-anime-style-generator/ 【社区经验（工具方）】

【社区实证】西漫 halftone/Ben-Day dots 与日漫 screentone 是**两种印刷传统，混用会 muddy**，应 commit 其一（halftone+manga 混写尤其糟）——来源：https://artpromptsgenerator.org/ai-comic-book-art-prompts/ 【社区实证】

### 2.2 「3D 日漫 CG」（原神型）社区锚词

- 社区实际用法以「原神风」为锚：`in the style of Genshin Impact's 3D rendering anime-style art`（Leonardo 社区 prompt）；neta.art、CGTrader 均以 Genshin style 为独立风格类目
- SD 侧给动漫图加 3D 感历史上靠 **3DMM LoRA**（trigger: `3DMM`），说明纯词在部分底模上不够、要 LoRA 辅助
- Flux 侧 cel-shading 也有专用 LoRA（Civitai "Cel Shading Style (CGI Anime)"），同样旁证：**自然语言底模上风格词锁不住时，社区答案是 LoRA**
- 来源：https://civitai.com/models/909778/cel-shading-style-cgi-anime 【社区实证】、https://stable-diffusion-art.com/anime-models-and-prompts/ 【社区经验】、https://neta.art/use-cases/en/ai-genshin-impact-art-generator 【社区经验】

### 2.3 对 style-3d-anime 模板（现全无出处）的逐块裁定

| 模板成分 | 裁定 |
|---|---|
| 「精致3D日漫CG渲染/3D立体建模」 | 方向成立（= Genshin-style 3D rendering anime-style 的中文写法），可补英文锚词【社区经验】 |
| 「次表面散射皮肤质感」 | 见 ④：写实侧有实证、3D 动漫侧无直接 A/B，属「合理借用」【推测】 |
| 「发丝根根分明」 | 无对照实证，属经验写法【查不到】 |
| 「织物纹理/皮革质感/金属反光清晰」 | 归入 intricate_details 族（见 ④），过用会 busy【社区实证】 |
| 边界词「赛璐璐/粗描边/色块平涂 混入→3D 质感被压平成 2D」 | 机理自洽（flat color fields 正是 cel 定义词，2.1），但无直接 A/B，标【推测】 |
| 边界词「写实词混入→日漫脸被写实化，恐怖谷」 | 方向有据（见 ③），「恐怖谷」具体后果无直接实证【社区经验】 |
| 翻车对策「脸部日漫锚词前置」 | 与 1.4 冲突风险：Animagine 官方主张质量词句尾、顺序敏感模型前置一般更强——「前置」仅在 NAI 类底模有据，即梦/Seedream 无实证【查不到】 |

---

## ③ 写实/动漫边界词实证（校准 style-3d-anime 边界词表）

- 【社区实证】Reddit r/StableDiffusion PSA：**动漫底模可以被提示词拉到完全 photoreal**（给了两类方法）——反向证实写实词混入动漫提示词确实会把渲染拉向写实，风格漂移是真实存在的单向吸引：https://www.redditmedia.com/r/StableDiffusion/comments/1hedclp/psa_make_your_anime_checkpoint_outputs_completely/ 【社区实证】
- 【社区实证】Civitai「Semi-Realistic Blend XL」：同一底模可产 2.5D anime 与 semi-realistic——**「半写实」是真实存在的中间吸引域**，写实词混入动漫词的落点常是半写实而非直接照片：https://civitai.com/models/1477356/semi-realistic-blend-xl 【社区实证】
- 【社区实证】Promgrammer：SDXL 上 `masterpiece` 反向拉向绘画；photorealism 靠相机词族（focal length/film stock）而非质量词——**写实词族与动漫词族在 SDXL 语义空间里确实互拉**：https://www.promgrammer.com/en/guides/quality-tags-deep-dive 【社区实证】
- 【社区经验】恐怖谷修复多在写实侧（natural skin texture, visible pores, catchlights, subtle asymmetry）：https://www.sozee.ai/resources/fix-uncanny-valley-ai-faces/ 【社区经验】
- **裁定**：「写实词混入动漫提示词→漂向写实/半写实」**成立**【社区实证】；「→恐怖谷」是可能后果而非必然，宜降级为「易出半写实不协调感」【社区经验】；即梦/Seedream 上的混入后果**查不到对照实证**【查不到】。

---

## ④ SSS/次表面散射等材质词效

- 【社区实证】Reddit r/StableDiffusion：写实皮肤 prompt 里 **"subsurface scattering" surprisingly effective**——会轻微推近、加柔和背光、皮肤显著变自然（SD1.5/XL 时代多人复现过该说法）：https://www.redditmedia.com/r/StableDiffusion/comments/1bonciw/prompt_for_realistic_skin/ 【社区实证】
- 【社区实证】同站 filler-keywords 讨论：SSS 词与 **3D 渲染语料关联强于 photorealistic**——用在 3D 风格段比用在写实段更「名正言顺」：https://www.reddit.com/r/StableDiffusion/comments/1bu2b1b/how_important_are_the_ridiculous_filler_prompt/ 【社区实证】
- 【厂商博客·低权重】Hailuo/BytePlus 指南：SSS 建议配组织学词（translucent epidermis, dermal light transport）与逆光构图约束，称比 "glowing skin" 稳：https://blog.hailuoai.video/knowledge/subsurface-scattering-ai-skin-realism-master-guide 【社区经验（厂商营销文）】
- 【社区实证】Flux 上 "subsurface scattering" 单词锁不住时社区做法是 SSS LoRA（Civitai "subsurface scattering skin" Flux.1 LoRA）——**Flux 词效有限的旁证**：https://civitai.com/models/739544/subsurface-scattering-skin 【社区实证】
- 材质词族（intricate details / super detail）：填满表面细节，**过用产生 busy 的「AI 感」纹理**：https://www.promgrammer.com/en/guides/quality-tags-deep-dive 【社区实证】
- **裁定**：SSS 在 SD 系写实侧有效【社区实证】；Flux 弱【社区实证·旁证】；**Seedream/即梦、MJ、SDXL 动漫侧的 SSS 词效查不到任何 A/B 实证**【查不到】——style-3d-anime 模板「次表面散射皮肤质感」在即梦/Seedream 上属未验证借用。

---

## ⑤ comic / fantasy / infinite-flow 三风格词库来源

### 5.1 style-comic（美漫）——词库与社区词库对得上，可补三件套理论

- 【社区实证】美漫风格三件套 = **bold ink outlines + flat cel color + halftone/Ben-Day dots**，再加动态镜头（low/Dutch tilt）与**时代词**（golden-age halftone / 90s grim-dark / modern flat digital / ligne claire），时代不同画面完全不同：https://artpromptsgenerator.org/ai-comic-book-art-prompts/ 【社区实证】
- 速度线/动作线（speed lines / action lines）+ 动态角度比形容词更能卖「能量感」【社区实证·同上】
- MJ 侧 comic book style 是 Midlibrary 实测大类（525 styles / 249 SREF codes）：https://midlibrary.io/styles/comic-book-style 【社区实证】
- **裁定**：skill 现有词（speed lines、halftone dots、bold black outlines、vibrant flat colors）均能对上社区词库【社区实证】；缺「时代词」维度；负面词 `3D, realistic` 无专门实证（MJ `--no` 只是 nudge，见 ⑥）【查不到】。

### 5.2 style-fantasy（西幻）——「Greg Rutkowski 画师风增强」是过时写法

- 【新闻实证】Greg Rutkowski 名字曾是 SD 最热 artist prompt（40 万+次），**SD 2.0 起 Stability 移除在世艺术家风格模仿**；社区用 LoRA/微调「复活」该风格：https://decrypt.co/150575/greg-rutkowski-removed-from-stable-diffusion-but-brought-back-by-ai-artists 、https://www.bbc.com/news/uk-wales-66099850 【新闻/官方立场】
- **裁定**：「Greg Rutkowski（画师风增强）」仅对 SD1.5 系老底模有效；SD2+/SDXL/Flux/MJ 上无效或被策略屏蔽，**skill 不应作为通用增强词**，应标年代与底模限制。fantasy 词库主体（epic lighting, intricate armor, fantasy concept art, oil painting style, dark fantasy）在 MJ/SD fantasy prompt 库通用：https://www.promptspace.in/fantasy-art-prompts 、https://therightgpt.com/ai-prompts/image-prompts/midjourney/fantasy-art 【社区经验】。

### 5.3 style-infinite-flow（无限流）——有可用的实证词库，现 skill 只覆盖了一半

- 【社区实证】无限流视觉的五类循环空间模型，每类有可直接抄的英文提示词：莫比乌斯走廊（Möbius strip corridor / Escher-inspired spatial paradox）、彭罗斯阶梯（Penrose staircase）、镜像递归房间（infinite reflections）、嵌套走廊（fractal-like nested spaces）、时空碎片拼贴（fragments from different time periods）
- **M.C. Escher 是「不可能空间」的风格锚**（训练数据标注率高，AI 理解 "Escher-inspired" = 非欧空间）——现 skill 缺这个锚
- 一人多身（同一角色多版本同框 + glowing temporal threads）、时空间隙（a crack in reality / temporal energy）、异化时钟
- 副本风格多样性：pastel gothic horror（恐怖童谣）、cyberpunk xianxia（赛博道观）、wasteland amusement park（废土游乐场）；**统一多副本靠「贯穿性视觉锚点」而非统一画风**
- 无限流≠赛博朋克：前者是「多世界切换机制」，视觉重点在**过渡空间**（门/电梯/走廊/屏幕）
- 来源：https://www.flowpixai.com/ai-art/ai-infinite-loop-painting.html 【社区实证】
- 【社区实证】glitch art 词表（可补 system UI/诡异氛围段）：RGB channel shift, datamosh, scanlines, pixel sorting, databending, corrupted signal, compression artifact：https://www.designstylebook.com/prompts/glitch-art 【社区实证】；Sci-Fi HUD/system UI overlay 有成熟 prompt 库词条：https://completeaitraining.com/prompts/design-a-sci-fi-hud-interface/ 【社区经验】
- **裁定**：现 skill 的 dimensional rift / portal / space distortion / floating data codes / system UI overlay 方向对但无出处；应补 Escher 锚、五类循环空间词组、glitch 词表、「贯穿性锚点」手法。

---

## ⑥ 负面词通道分流（4 处【推测】的裁决）

### 6.1 Midjourney `--no`（官方）

- 官方文档页存在（docs.midjourney.com《No》，直接抓取被 403，经检索摘要+两处参数镜像站交叉确认）：`--no <item>, <item>` 逗号分隔、置于提示词尾
- 行为定性：**是 nudge 不是绝对过滤**；正向强提示可覆盖；**罕见情况下点名某物反而引入该物**；在 prompt 里写 "no plants" 无效，必须用 `--no`；多词必须逗号分隔
- 来源：https://docs.midjourney.com/hc/en-us/articles/32173351982093-No 【官方】（403，经 https://www.numonic.ai/integrations/midjourney-parameters/no 、https://www.dreamdrive.ai/learn/midjourney/midjourney-negative-prompts/ 【社区实证·镜像】交叉确认）

### 6.2 SD 系 negative prompt（官方/社区）

- A1111/ComfyUI 真负面通道，负面质量词常比正面有效（1.3）；动漫侧常用负面 embedding（EasyNegative、bad artist-neg）：https://stable-diffusion-art.com/anime-models-and-prompts/ 【社区实证】
- Pony score 词放负面收益有限（score_4/5 下限）：https://civitai.com/articles/4248/ 【社区实证】

### 6.3 即梦/Seedream「无负面框」——**API 层坐实，UI 层存疑**

- **【官方实证】火山引擎图片生成 API（Seedream 5.0 pro/flash/lite、4.5、4.0 全系）请求参数逐项核对：prompt、image、layer_decomposition、size、optimize_prompt_options、output_format、background、response_format、sequential_image_generation(+options)、stream、tools、watermark、model——没有 negative_prompt / 负向提示词 / 反向提示词参数。** 来源：https://www.volcengine.com/docs/82379/1541523 【官方】（全文 4 万字符逐段核对）
- 本地 dreamina-canvas CLI（管线实际入口）二进制与技能文档中亦无 negative 相关字段【本地实证】
- **【UI 层存疑】**第三方说法分裂：
  - 称「有」：塔猴 2026 教程称文生图「可以添加负面提示词，如模糊、畸形手」（https://www.tahou.com/article/217656615786854405 【社区经验】）；头条/抖音创作者称「负向提示词」栏存在（https://www.toutiao.com/article/7585072904665055779/ 【社区经验】）
  - 疑似幻觉：php.cn/17golang/ufcn 等内容农场文章描述「高级设置→反向提示词框」时混入即梦根本不暴露的 CFG 值/采样器/模型 v2v3 话术，**整批文章疑似 LLM 生成的互相抄袭的 SEO 垃圾，不可作证据**
  - 也有创作者教程把「负面词加在提示词末尾」当反向约束用——这是正向通道写法，不是负面框
- **裁定**：4 处【推测】「即梦无负面框」——**在 API/画布管线（我们出图出片的实际通道）升级为【官方实证：无负面参数】**；在网页/App UI 上【无法证实也无法证伪】，需一次实机截图定案，报告阶段不得写成事实。结论：负面词一律走正向改写（「干净、无文字、无水印」式描述）依然成立且更稳。

---

## ⑦ 可直接写入 skill 的硬要求（全部标源）

1. **Booru 质量词只在 Booru 训练动漫底模（NAI/Animagine/Pony 系）有强信号；SDXL base/Flux 弱或反向拉向绘画；Midjourney 完全忽略内联质量词（用 --style raw / --stylize / --quality）**【社区实证·Promgrammer】
2. **质量词 ≤3 个**：超过 3–4 个稀释注意力、可能属性泄漏；8k/4k 不改分辨率只偏置 caption，禁挂【社区实证·Promgrammer】
3. **质量词位置分底模**：NAI V3 越靠前越强（官方开关却追加句尾）；**Animagine XL 4.0 官方要求质量词放句尾**（前置会让 artist/风格词失效）；Pony score 梯子放句首【官方·NAI docs + CagliostroLab】
4. **NAI 现行体系里 `masterpiece` 是 Aesthetic Tag、仅 V4.5+ 生效**；V3 时代真正强的是 `very aesthetic`、`amazing quality`，`best quality`/`absurdres` 边际效应很小【官方·NAI docs + 社区实证·note.com】
5. **Pony 用 `score_9, score_8_up, score_7_up`；V7 弱化 score 词改用 score_8/score_7_up；source_/rating_ 仅训练过的模型生效**【社区实证·artificialguy/Civitai】
6. **负面侧质量词（low quality, worst quality, blurry, jpeg artifacts, extra fingers, watermark, text）常比正面质量词更有效**，SD 侧优先给负面框【社区实证·Promgrammer】
7. **cel-shading 锁质感五件套**：cel-shaded、two-tone shadow blocks、ink line outline、flat color fields、明确光向 + rim light；**禁 soft-glow / painterly 修饰词**（明文翻车词）【社区经验·Anifusion】
8. **halftone（西漫）与 screentone（日漫）是两个传统，禁混写**，commit 其一【社区实证·artpromptsgenerator】
9. **美漫三件套**：bold ink outlines + flat cel color + halftone/Ben-Day dots，加时代词（golden-age / 90s grim-dark / modern flat digital / manga）与动态镜头【社区实证·artpromptsgenerator】
10. **写实词混入动漫提示词会把画面拉向写实/半写实**（半写实是真实中间态）；「恐怖谷」降级为「易出半写实不协调感」【社区实证·Reddit PSA + Civitai】
11. **SSS 词在 SD 系写实侧有效**（含推近+柔背光副作用），与 3D 语料强关联；Flux 需 LoRA 补；**Seedream/MJ/即梦上未验证**【社区实证·Reddit】
12. **Greg Rutkowski 类在世艺术家名**：SD 2.0+ 已移除模仿能力，仅老 SD1.5 底模有效，skill 中禁作通用增强词【新闻实证·decrypt/BBC】
13. **无限流锚**：M.C. Escher = 不可能空间风格锚；五类循环空间词组（莫比乌斯/彭罗斯/镜像递归/嵌套走廊/时空碎片）；glitch 词表（RGB channel shift, datamosh, scanlines, pixel sorting, databending）；多副本统一靠「贯穿性视觉锚点」；视觉重点在过渡空间【社区实证·flowpixai + designstylebook】
14. **MJ `--no` 是 nudge 非绝对**：逗号分隔、写在正文的 "no X" 无效、点名可能反引入；替代手段是重新描述画面【官方+社区镜像·MJ docs/Numonic】
15. **即梦/Seedream API 无负面参数（官方 API 文档核对）→ 负面意图一律正向改写**；UI 是否有负面框未定，禁写成事实【官方·volcengine + 本报告核对】

---

## ⑧ 空白清单（查不到，明说）

| # | 空白 | 影响 |
|---|------|------|
| 1 | 即梦网页/App UI 是否有负面提示词框——第三方说法分裂且含明显 LLM 幻觉文，需实机截图一次定案 | 4 处【推测】的 UI 半边无法落锤 |
| 2 | Seedream/即梦上任何风格词（SSS、cel-shading 词、质量词）的 A/B 对照实证全缺 | style-3d-anime/anime 在即梦侧全是「跨模型借用」 |
| 3 | SSS 在 MJ、SDXL 动漫侧的词效无 A/B | style-3d-anime 模板核心词未验证 |
| 4 | 「赛璐璐/平涂混入→3D 压平成 2D」无直接对照 | 边界词表后果列为推测 |
| 5 | 「发丝根根分明」「织物纹理/皮革质感/金属反光」等中文材质词在国产模型的词效无任何实证 | 材质词库整段经验性 |
| 6 | style-comic 负面词 `3D, realistic` 的实测效果 | 负面词表待验 |
| 7 | Pony V7 / Illustrious 新版质量词行为的官方一手文档（现靠社区博客） | score 词策略时效风险 |
| 8 | Midjourney 官方文档正文无法直接抓取（403），靠镜像交叉 | MJ 结论二手化 |

---

## 附：本次主要来源清单

| 来源 | 性质 | 用于 |
|------|------|------|
| https://docs.novelai.net/en/image/tags/ | 官方 | ① |
| https://note.com/nai_researchnote/n/nbf34d1edf269 | 社区实证 | ① |
| https://www.promgrammer.com/en/guides/quality-tags-deep-dive | 社区实证 | ①③④ |
| https://cagliostrolab.net/posts/optimizing-animagine-xl-40-in-depth-guideline-and-update | 官方（模型方） | ① |
| https://civitai.com/articles/4248/what-is-score9-and-how-to-use-it-in-pony-diffusion / https://artificialguy.com/blog/pony-illustrious-prompt-syntax/ | 社区实证 | ① |
| https://anifusion.ai/style/cel-shading-anime-style-generator/ | 社区经验（工具方） | ② |
| https://artpromptsgenerator.org/ai-comic-book-art-prompts/ | 社区实证 | ②⑤ |
| https://civitai.com/models/909778/cel-shading-style-cgi-anime / https://civitai.com/models/739544/subsurface-scattering-skin | 社区实证 | ②④ |
| https://www.redditmedia.com/r/StableDiffusion/comments/1hedclp/psa_make_your_anime_checkpoint_outputs_completely/ | 社区实证 | ③ |
| https://civitai.com/models/1477356/semi-realistic-blend-xl | 社区实证 | ③ |
| https://www.redditmedia.com/r/StableDiffusion/comments/1bonciw/prompt_for_realistic_skin/ | 社区实证 | ④ |
| https://decrypt.co/150575/... / https://www.bbc.com/news/uk-wales-66099850 | 新闻 | ⑤ |
| https://www.flowpixai.com/ai-art/ai-infinite-loop-painting.html | 社区实证 | ⑤ |
| https://www.designstylebook.com/prompts/glitch-art | 社区实证 | ⑤ |
| https://docs.midjourney.com/hc/en-us/articles/32173351982093-No + Numonic/Dreamdrive 镜像 | 官方+镜像 | ⑥ |
| https://www.volcengine.com/docs/82379/1541523 | 官方 | ⑥ |
| https://www.tahou.com/article/217656615786854405 | 社区经验 | ⑥（存疑） |
