# AIGC 人物/场景提示词优化研究报告

- 日期：2026-10-27
- 范围：Midjourney / Stable Diffusion / Flux / 即梦(Dreamina/Seedream) / Nano Banana / GPT-Image
- 方法：中英文检索 22 组（20 组有效），深度抓取 11 个页面（含 BFL/Google Cloud/OpenAI 官方文档）；结论标注来源，未查证处标【推测】

---

## ① 人物一致性技巧（按平台分列）

### 通用方法论

1. **三视图/Character Sheet 是人物一致性的地基**（来源：Arcloop《人物三视图完整指南》、CSDN《用 GPT-Image-2 生成人物特写+三视图》、imagesv2.ai《Ai 角色设定表提示词》）
   - 三视图 = 正面 + 标准侧面 + 背面，**同一中性站姿、同一画面尺度、同一相机高度、同一光照**，脚底同基线，纯浅灰背景。常出斜侧角度的角色补一张 3/4 视图做四视图。
   - **先定"看不见的部分"**再生成：后领、衣长、接缝、包带、道具挂点——没有这些就没有判断对错的依据。
   - 推荐顺序：**先面部特写三视图锁五官 → 再全身三视图锁服装体型 → 超分 → 关键道具单独锚定**（CSDN《26_AI角色一致性难题，用"三视图"一招破解》）。
   - 不对称细节（发夹/伤疤/挎包）按**角色自身左右**记录，允许自然遮挡，禁止为露出而换边（Arcloop）。
   - 验收清单：脚底基线/头身比/肩高腰线、侧面"额头-鼻尖-嘴唇-下巴-后脑"同属一个头、服装从正面合理延续到背面、不对称物不换边。
   - 三视图模板要点（OpenNana 专业角色三视图提示词、知乎《Ai漫剧-人物三视图提示词》）："composition references the reference image, left = front/side/back full-body three views, right = multi-angle facial close-ups + clothing texture details"，并显式写"不要动作姿势、强透视、其他人物、文字、不同服装版本"。
   - 重要认知：**三视图是"设计记录"不是"免死金牌"**——视频/图生图仍会变脸，需配合参考图 + 短镜头逐角度验证（Arcloop）。

2. **五官锚点写法**：把识别特征写成短名词锚点并在每张提示词里**原样重复**——脸型、发型轮廓、发色、眼睛颜色、标志性配饰及其位置；表情和光照是变量，不写进固定设定（Arcloop；FLUX 官方漫格示例同理：每格重复"brown skin tone, short fade haircut, black-framed glasses…"）。Nano Banana 2 社区指南建议**每镜 5-7 个核心特征锚点**（selfielab blog）。

### Midjourney

- **--cref（V6 引入，V7 增强）**：`场景描述 --cref [参考图URL]`，保脸/发/体型；**--cw 0-100 控制强度**：cw 100 全量复刻（创意受限）、**cw 75-85 推荐起点**、cw 50 只留神似、cw 0 只带风格（PromptMake《Midjourney --cref Guide》）。
- **--cref + --sref 组合**：`--cref [角色URL] --cw 80 --sref [风格URL] --sw 80`——人物锁身份 + 风格锁调性/光影/渲染（PromptMake；creatide.ai《SREF vs CREF》）。
- **参考图要求**：正面、中性表情、好光照、干净背景、无墨镜口罩、单人——参考图质量直接决定 cref 上限（PromptMake）。
- **--cref 局限**：写实参考最稳，卡通/高度风格化参考易漂；极端角度（正→背）掉一致性；**不复制服装**（只带人物特征）；跨大风格（写实→动漫）掉保真（PromptMake）。
- **--seed 的真实作用**：Midjourney 官方文档把 seed 归在"**Not for Saving Styles**"下——seed 复现的是构图/风格倾向，**不能锁脸跨场景**（Midjourney 官方 Seeds 文档；cropupai《Seeds & Consistency: Limits Without --cref》）。seed 适合做提示词 A/B 测试（同 seed 对比改词效果）。
- V7 还有 Omni Reference（--oref/--ow）可同时带人物+物体（aiarty、cropupai）。

### Stable Diffusion / Flux（本地/ComfyUI 生态）

- **工具分工**（media.io《ComfyUI Consistent Characters》）：**IP-Adapter**=快速参考式外观迁移（大姿势变化时失稳）；**PuLID**=面部身份注入不污染模型、保留风格自由（runcomfy《PuLID Flux II》）；**InstantID**=ControlNet 路线的高保真人脸保持（arXiv 2401.07519）；**PhotoMaker**=多张参考堆叠 ID embedding；**角色 LoRA**=长期反复出场角色的终极方案（成本最高）；**ControlNet（OpenPose/Reference Only）**=只管姿势和构图（CSDN《如何让SD在不同场景保持人物形象一致性》）。
- 横评结论（aiofm《PuLID vs InstantID vs IP-Adapter FaceID 2026》、iimagined.ai）：身份保真 PuLID/InstantID > PhotoMaker > 普通 IP-Adapter；风格自由度反之；出镜人物多/长期连载→训 LoRA，一次性任务→PuLID/InstantID。
- Flux 生态新进展：FLUX.2 多参考图（selfielab《Flux 2 Multi-Ref》）、Flux Kontext + PuLID 组合（runcomfy）、ComfyUI-PuLID-Flux2（GitHub/iFayens）。

### 即梦 / Seedream

- **参考图语义**（Seedream 4.0/4.5 官方提示词指南·头条、zhang-jian《Seedream 4.0 使用指南》）：Seedream 是统一的"生成+编辑"模型，支持**多图参考融合**；写法必须**给每张参考图编号并声明职责**："图一作为人物主体参考，保留人物五官和发型；图二作为服装参考；图三作为场景参考"——笼统写"参考这些图"必翻车。
- **提示词五段式**（zhang-jian）：任务 / 对象 / 参考 / **保留** / 约束。"保留"是核心：`保留人物的脸型、五官比例、发型、表情和服装主体结构，只改变绘画风格`；编辑时补"只修改……，其他内容保持不变"。
- **php.cn《即梦ai角色参考图使用技巧》五步法**（摘要，原文抓取为空）：①上传高清正面参考图锁定特征 ②语义锚定提示词：复述确定特征再扩展变量 ③三张图分别锚定结构/装备/配色 ④首尾帧加参考图校准动态 ⑤局部重绘修断裂点。
- 即梦 3.0 的**智能垫图/智能参考**是官方的人物一致性入口（搜狐《即梦图片3.0智能垫图》）；进阶用**局部重绘**修五官偏移（输入"对称的五官""自然的手部姿势"）（头条《即梦ai如何保持漫画人物一致性》）。
- **纯提示词路线**（头条《如何通过提示词解决即梦AI的人物一致性》）：结构化复述全部外观锚点 + 固定角色描述，适合不愿传参考图的场景，但上限低于参考图路线【推测：两条路线可叠加】。
- 即梦提示词是**结构化六要素**而非关键词堆砌：主体/风格/光线色调/构图视角/材质细节/画质（CSDN《即梦ai提示词实战：结构化写法与模板》）。

### Nano Banana（Gemini 图像）

- **官方公式**（Google Cloud《Ultimate prompting guide for Nano Banana》）：**[参考图] + [关系指令] + [新场景]**，例："Using the attached napkin sketch as the structure and the fabric sample as the texture, transform this into a 3D armchair render. Place it in a sun-drenched minimalist living room."
- 一个 prompt 最多**混用 14 张参考图**（Google Cloud 官方规格）；社区实践是 8 张参考系统（selfielab《Nano Banana Pro Character Consistency》）。
- 一致性技巧：**foundation image（锚点图）+ 5-7 特征锚点 + seed 引用**（techyheaven、selfielab、nanobananatool）；编辑时**显式写"要保留什么"**："Remove the man from the photo" 之外要说清哪些部分完全不动（Google Cloud）。

### GPT-Image

- 自然语言直述，无参数系统；一致性靠**多图指令逻辑**：给模型下结构化命令如"Dress this person"并附 6 张单品参考图，模型会分开理解每件再合成（nanobananalib《GPT Image 1.5 multi-image consistency》）。
- 官方 cookbok《gpt-image-1.5 Prompting Guide》强调：**约束清晰化、编辑边界显式化（Change only / Keep unchanged）、多图指令逻辑**；但"Change only"**不保证**模型只改该处，必须与原图对照核查（gptimage2.hk 实测同结论）。
- 常用句式（贝果科技《ChatGPT 生图提示词与改图指令》）："保留人物，只换背景/服装"类句式 + "只修改 X 区域，人物五官、发型、衣服和背景保持不变"。

### 「换场景人不变」的分层控制法（跨平台综合）

1. **身份层**：参考图/cref/PuLID 锁脸+发型+体型（权重高，别让文字去争）
2. **服装层**：文字显式写全（cref 不保服装！），或单独一张服装参考图
3. **场景层**：场景描述或场景参考图，人物描述只留锚点
4. **光影层**：写明光源方向/色温/时段，且与场景一致（见②）
5. **禁改层**：`Keep unchanged: face identity, hairstyle, costume colors`（GPT/即梦/Flux 系用正向句；SD 用负面词）

---

## ② 场景一致性技巧

1. **场景参考图 + 版式锚定**：
   - **九宫格/俯视图/全景图方案**：用俯视图或九宫格把空间布局钉死，再用 skill/提示词约束每次生成都对齐该布局——B站《保持场景一致性!100%成功的方案》《AI视频场景一致性完整工作流：俯视图、九宫格、全景图》称这是当前最稳的场景复用方案。
   - 多视角场景：先建基础场景图 → 再以它为参考生成多视角（什么值得买《如何用AI生成场景一致性超高的多视角图》，Midjourney + NanoBanana2 组合）。
2. **同场景多镜复用**：
   - 每镜重复同一段**场景锚点描述**（家具布局、门的方位、窗的位置、道具摆设）——与人物锚点同理（FLUX 官方漫画格示例：每格重复同一 Setting 描述）。
   - **空间连续性道具要单独交代**：连续开门镜头的门向、持物手，人物三视图管不了这些（Arcloop）。
   - Qwen Multiangle 等多角度一致性模型可一键同主体多视角（知乎《Qwen Multiangle》）【推测：效果需实测】。
3. **光影统一（lighting match）写法**：
   - 核心公式（CSDN《光影重构底层逻辑》）：**光源位置 + 光源类型 + 光色/色温 + 时段**四件套写全，如"窗光从画面左侧进入，柔和漫射光，暖色 3200K，傍晚"。AI 分不清左右光、图生图会光影混乱——用"提示词预控 + 工具二次重构（Tapnow 可视化打光、Nano Banana Pro 光影二次建模）"双向控光。
   - 统一多镜光影的机械做法：**把光影四件套做成固定段落，逐镜复制**，只改动作与景别（B站《AI多角度一致性出图流程和光影切换提示词指令》）。
   - 换场景保光影的模板（Nano Banana 官方"图生图编辑"思路）："保留原图的光照方向和色调，仅替换背景为 X"。
4. **场景参考图用法**：参考图声明职责——"图一提供原始场景和构图，保持背景、光照和镜头角度不变"（zhang-jian）；场景必挂参考图比纯文字稳（与本项目"素材关联"硬闸方向一致）。

---

## ③ 指令公式与要素优化

### 提示词公式（各模型最佳实践）

| 模型 | 公式/结构 | 顺序权重 | 语法 |
|------|----------|---------|------|
| Midjourney | 描述性短语 + 参数 | **越靠前权重越高**，重要元素放最前 | 逗号分隔短语，`--ar --v --style raw --stylize --chaos` 放尾部（imagetoprompt） |
| Stable Diffusion | 质量标签→风格→主体→描述→场景→镜头 | 前面 token 权重高；`(词:1.2)` 加权、`[词]` 降权、BREAK 分段 | 标签堆；SD1.5 ≤75 CLIP token，SDXL 可长（dreamdrive、promptmake） |
| Flux | **Subject + Action + Style + Context**，自然语言整句 | 词序重要，主语/关键动作在前 | 30-80 词最佳；支持 JSON 结构化 prompt；引号包文字、hex 色号（BFL 官方 prompting_guide_flux2） |
| Nano Banana | [Subject]+[Action]+[Location]+[Composition]+[Style]；参考图模式 [Refs]+[Relationship]+[New scenario] | 强动词开头 | 自然语言叙述式，"关键词列表不够用"（Google Cloud 官方） |
| GPT-Image | 完整自然语句 + 多图指令 | 需求前置 | 自然语言；文字内容用引号（OpenAI image-prompting、imagetoprompt） |
| 即梦/Seedream | 任务/对象/参考/保留/约束 五段 | 结构化分段 > 堆词 | **中文自然语言即可**，越结构化越稳（zhang-jian、CSDN） |

要素顺序通则（Medium《The Prompt Formula That Works Across Midjourney, GPT…》）：主体 > 动作/构图 > 风格 > 光影 > 画质词；**画质词只是收尾小料，救不了空洞的提示词**。

### 景别与构图中英对照表

| 中文 | English | 用途 |
|------|---------|------|
| 大远景/极远景 | extreme wide shot (EWS) | 宏大环境、孤寂感 |
| 远景 | wide shot / long shot | 人小景大，交代环境 |
| 全景 | full shot (FS) | 全身入画，脚底到头顶 |
| 中景 | medium shot (MS) | 膝盖以上，叙事主力 |
| 中近景 | medium close-up (MCU) | 胸口以上，对话戏 |
| 近景 | close-up (CU) | 肩部以上，情绪 |
| 特写/大特写 | extreme close-up (ECU) | 眼睛/局部细节 |
| 仰拍/低角度 | low angle shot | 威压、英雄感 |
| 俯拍/高角度 | high angle shot | 渺小、被审视 |
| 鸟瞰 | aerial view / bird's-eye view | 地图感、全局 |
| 荷兰角 | Dutch angle | 不安、失衡 |
| 过肩 | over-the-shoulder (OTS) | 对话关系 |
| 主观镜头 | POV shot | 代入感 |
| 浅景深/背景虚化 | shallow depth of field, f/1.8, bokeh | 突出主体 |
| 三分法构图 | rule of thirds | 通用构图 |
| 中心构图 | center-framed | 对称/仪式感 |

（来源：Yolo Lab《电影景别》、Floniks《镜头景别全解析》、小黄技术栈《常用镜头与分镜提示词速查表》、shot.gpsx.io《镜头语言速查系统》、CSDN《Midjourney进阶：景别详解》、jsnoteclub《SD 镜头拍摄 Prompt 中英文汇总》）

### 负面词通道表（2026 各平台差异）

| 平台 | 负面通道 | 语法 | 注意 |
|------|---------|------|------|
| Midjourney | `--no` 软负面（≈-0.5 权重） | `prompt --no fruit, text` | 列表**3-5 个词**为宜，长串碎片化注意力；散文写"without X"会被当"有 X"读；`--no modern clothing` 会被逐词误读触发审核（PromptMake《Negative Prompts in 2026》） |
| Stable Diffusion / SDXL | 独立负面框，**真实有效** | `(extra fingers:1.3)` 可加权 | SDXL 用 5-15 个精准词，别搬 40 行 SD1.5 老墙；负面质量词常比正面质量词更管用（Promgrammer、PromptMake） |
| Flux / Flux 2 | **不支持负面词** | 无（diffusers 的 negative_prompt 在默认 guidance 下被忽略） | 必须**正向改写**："no crowds"→"empty plaza, solitary figure"；"no blur"→"sharp focus"（BFL 官方、findimageprompt） |
| GPT-Image / DALL·E | 无参数 | 排除写进散文："clean white backdrop, product only, no props, no text overlays" | 排除从句前置效果更稳（PromptMake） |
| Nano Banana / Gemini | 无参数 | **正向措辞**官方建议："empty street" 代替 "no cars"（Google Cloud 官方） | — |
| 即梦/Seedream | 无独立负面框【推测】 | "保留/不要" 句式：不要改成白天、不要磨皮 | zhang-jian 的"约束"段承担负面职能 |

负面词三个正当用途（PromptMake）：**媒介锁**（挡卡通/挡照片）、**物体清除**（人/车/水印）、**已实测的顽固缺陷**。抽象词（ugly、bad composition）远不如具体名词（watermark、frame、crowd）。互相打架的同义词（blurry + out of focus + soft focus 同写）纯浪费。

### 画质/风格词：真有用 vs 废话

（核心来源：Promgrammer《Quality Tags — A Deep Dive》，含固定 seed 对比实测）

- **8k/4k/highres**：不改变输出分辨率（分辨率由采样参数决定），只是把结果偏向训练集中"高分辨率"标注的图——**纹理更锐、微细节更多**，是弱偏置。Midjourney 里 HD/8K/4K **不提升物理分辨率**，只影响视觉风格与细节倾向（groprompt；Reddit r/midjourney 认为其本质是图文匹配统计）。
- **masterpiece/best_quality**：**仅对 Booru 系动漫模型（NovelAI/Animagine/Pony）强有效**（训练 caption 里真有这些词）；SDXL 上会把图拉向"画廊绘画"，**写实目标反而是减分**；Flux 上近乎无效（自然语言模型）；**Midjourney 直接忽略内联质量词**，用 `--style raw --stylize --quality`。
- 实测（Promgrammer，Illustrious v3 固定 seed）：`worst quality` 放正面都不怎么掉档；**质量词堆到 3-4 个以上开始稀释注意力、甚至属性泄漏**（质量特征渗进主体描述）。
- **真有用的替代**：写实目标用**相机词汇**（85mm f/1.4、Kodak Portra 400、golden hour）代替 masterpiece；细节需求用具体材质词（navy tweed、etched silver leaf）代替 super_detail。
- 通用负面质量行（各 SD 系）：`low quality, worst quality, blurry, jpeg artifacts, deformed, extra fingers, watermark, text`。
- 结论：**"8k/RAW 有用吗"——答：分模型**。动漫 Booru 模型：masterpiece 族有效但别堆；SDXL 写实：换相机词；Flux/GPT/即梦：纯噪声；MJ：忽略，用参数。这与"统一加 8k 画质词"的省事做法冲突（见⑦）。

### 中文 vs 英文提示词

- 默认 CLIP（ViT-L-14）：**英文理解最深，中文有损耗**；SD/MJ 走英文词元最稳（搜狐《英文提示词vs中文提示词》）。
- **例外：即梦/Seedream 系对中文理解是第一梯队**（知乎《Seedream 4.0 教程：比 Nano Banana 更懂中文》），中文结构化提示词完全够用。
- Flux 2 支持多语言，且**用内容母语提示更"地道"**（BFL 官方：法语场景用法语提示，本地建筑/氛围更准）。
- 实操建议：SD/MJ/Niji 用英文；即梦/Seedream 用中文；Flux 两者皆可，涉文化细节用母语。

### Flux 特性备忘（BFL 官方）

- 自然语言 + T5 编码器：吃长句、能摆位（"text appears above the door"）、**关键词汤浪费其能力**。
- **文字渲染**：引号包文字 + 指定位置 + 字体风格（"bold industrial lettering"）+ 字号 + 颜色可用 **hex 码**（"#FF5733"）；要最佳排版用 FLUX.2 [flex]。
- JSON 结构化 prompt 与自然语言等效理解，适合生产流水线（scene/subjects/style/color_palette/lighting/camera 字段）。
- 漫画连续格的官方一致性法：**每格完整重复角色描述**（不厌其烦）。
- 写实必杀：写具体机型镜头胶片（"Shot on Hasselblad X2D, 80mm, f/2.8"），比 "professional photo" 强得多。

---

## ④ 五种风格的提示词组合与翻车点

### 1) 3D 卡通渲染 / cel-shading（本项目主风格：3D 都市动漫·卡通渲染）

- **高效组合**：`3D render, cel-shaded / flat shading, sharp shadow cutoffs, bold ink outlines, solid color blocks, vibrant palette, stylized proportions`（AtomWords cel-shading 定义：模仿手绘赛璐璐的 3D 渲染——硬阴影截断、色块平涂、粗描边）。都市时尚感加：`urban fashion outfit, city street background, trendy color grading`。
- PromptHero/stablediffusionweb 有大量 cel_shading 标签范例可抄结构。
- **翻车点**：
  - 写实词混入（`85mm photoreal, skin pores, DSLR`）会冲掉动画感（gptimage2.hk 实测避坑）；
  - 只写 "3D cartoon" 不写**描边/阴影截断/材质**，模型回退到通用 3D 卡通贴纸；
  - SD 上 cel-shading 效果**高度依赖 checkpoint**，通用底模出的是"3D 渲染"不是"赛璐璐"（Reddit r/StableDiffusion 讨论）【推测：需配动漫/卡通专用底模或 LoRA】；
  - Midjourney 里别指望 "cel shaded" 一个词定风格——MJ 吃长描述，写清渲染方式+描边+光影（Reddit r/midjourney）。
- 官方风锁模板（gptimage2.hk Style lock 改编）：`3D animated feature look; slightly large head, soft cheeks, readable silhouette; big expressive eyes, crisp iris highlights; soft subsurface skin, stylized hair clumps; cinematic three-point light, soft key + warm rim; clean anti-aliasing, no photoreal pores, no uncanny CGI.`

### 2) 日漫 / 二次元

- **组合**：`anime illustration, vibrant colors, cel shaded, clean line art`；吉卜力味加 `Studio Ghibli style, pastoral, soft watercolor backgrounds`（smartaiedits）；Niji 模式（`--niji`）自带二次元优化。
- SD 侧走动漫 checkpoint + Danbooru 标签体系：`1girl, solo, [发型发色], [服装], [表情], [场景], masterpiece, best quality`（注意：NovelAI 用空格分词，老 Animagine 用下划线，查模型文档——Promgrammer）。
- **翻车点**：手部/多余肢体（配负面 `extra fingers, bad anatomy` 或手部 LoRA）；文字乱码；混写实词导致"半写实恐怖谷"；Pony 系要用 `score_9, score_8_up` 评分体系而不是 masterpiece（Promgrammer）。

### 3) 皮克斯质感

- **组合**（可灵官方教程·抖音、gptimage2.hk）：核心是**四件套 = 圆润比例 + 夸张表情 + SSS 材质 + 电影级布光**：`3D Pixar-style animated feature look, slightly large head, soft cheeks, big expressive eyes, crisp iris highlights, soft subsurface scattering skin, smooth stylized hair clumps, cinematic three-point lighting, soft key + warm rim, gentle ambient occlusion, animated film still`。
- 明确表情词（curious/joyful）比只写 cute 有效（gptimage2.hk 对照表）。
- **翻车点**：
  - 只写 `Pixar style, cute` → 通用贴纸脸；
  - 一次改表情+服装+场景 → 脸一起漂（坚持**一图一变量**）；
  - 写实关键词冲掉动画感；
  - 写实电商产品图别用皮克斯风，会"卡通化"产品；
  - **版权**：风格描述≠复制受保护角色，禁写知名角色名（gptimage2.hk 避坑）。
- MJ 快捷通道：`--sref 3687830488 --v 7` 直接开 3D 卡通风格门（aimindwork 博客）【推测：风格码效果随版本波动】。

### 4) 赛博朋克

- **组合**（NavXD 提示词库分类、原创力《赛博朋克AI提示词》）：`cyberpunk, neon-lit megacity, rain-slick streets, holographic advertisements, glowing neon signs, high-tech low-life, teal and magenta color palette, volumetric fog, night, cinematic`。子类：霓虹城市全景 / 暗黑赛博 / 复古赛博 / 轻科幻。
- **翻车点**：
  - 霓虹乱入所有风格（写皮克斯/田园时误加 neon 就毁了——gptimage2.hk 风格污染警告）；
  - 只堆 neon 不写**光源布局**，光影混乱（配合②的光影四件套）；
  - 中文霓虹招牌文字易乱码——Flux/即梦 引号内写明文字内容；
  - 赛博+人物特写容易满屏光污染盖住人脸，需显式 `face clearly lit, rim light on face`。

### 5) 写实摄影

- **组合**（BFL 官方 + imagetoprompt）：`photorealistic portrait of [主体], shot on Canon EOS R5, 85mm f/1.4, shallow depth of field, golden hour window light, natural skin texture, slight film grain, Kodak Portra 400 colors`。**机型+镜头+光圈+胶片/调色**四件套是核心，不是 quality soup。
- 80s 复古：`film grain, warm color cast, soft focus`；2000s 卡片机：`early digital camera, flash photography, candid`（BFL 风格参考表）。
- **翻车点**：
  - `masterpiece` 在 SDXL 上把写实拉向绘画（Promgrammer）；
  - `8k, ultra-detailed, RAW photo` 堆叠无益，甚至"AI 味"（discover.oreateai《The Failure of Quality Soup》）；
  - 手部崩坏、皮肤塑料感（负面加 `plastic skin` 或写 `detailed skin texture`）；
  - MJ 默认"过于精美"——要粗糙纪实感加 `--style raw` + documentary photography（imagetoprompt）。

---

## ⑤ 人物 + 场景融合模板

### 模板 A：参考图融合（Nano Banana / 即梦 / GPT-Image 通用）

```
[参考图：图一=人物（角色锚点/三视图裁图），图二=新场景（可选），图三=风格（可选）]
任务：将图一人物放入 [新场景描述]，生成 [景别]。
人物保留：脸型、五官比例、发型、[发色]、[标志性配饰+位置]、[服装] 完全不变。
场景与光影：[光源位置+类型+色温+时段]，人物受光方向与场景一致，落地投影自然。
约束：人物符合场景透视与比例；只改变场景与姿势，不改变人物外观；画面无文字无水印。
```

（要素来源：zhang-jian 五段式 + Google Cloud [Refs]+[Relationship]+[New scenario] + gptimage2.hk Change only/Keep unchanged）

### 模板 B：Midjourney 分层

```
[人物锚点短语 x5-7，原样沿用] standing in [新场景+光影]，[景别]，[风格]
--cref [角色URL] --cw 80 --sref [风格URL] --sw 80 --ar [比例] --style raw
```

服装变化时在正文直接写新服装（cref 不保服装）；同系列逐镜只改场景/动作/景别。

### 模板 C：FLUX 文本流（无参考图时）

```
Style: [风格句]. Character: [完整人物描述——每镜逐字重复同一段]. Setting: [场景+光影].
Composition: [景别+机位]. Mood: [色调情绪].
```

（BFL 官方漫画格范式；80+ 词长镜允许，但主语和关键动作放最前）

### 模板 D：多镜连续（同场景同人物，系列锁定）

```
[人物锚点段——逐字复制] + [场景锚点段——逐字复制] + 本镜动作：[仅本镜变化]
景别：[本镜景别]；光影：[固定光影四件套——逐字复制]
Keep unchanged: face identity, hairstyle, costume, scene layout, lighting direction.
```

配套流程（综合 Arcloop/gptimage2.hk）：锚点立绘先行 → 一图一变量 → 逐张与锚点并排核对（头身比/眼距/发际线/配饰侧）→ 局部重绘修偏差 → 记录每镜所用参考图版本。

---

## ⑥ 来源清单

### 深度抓取（11）

| 来源 | 状态 |
|------|------|
| Google Cloud Blog《The ultimate Nano Banana prompting guide》 | 成功 |
| Black Forest Labs docs《Prompting Guide - FLUX.2 [pro] & [max]》 | 成功 |
| Promgrammer《Quality Tags — A Deep Dive》 | 成功 |
| Arcloop《人物三视图完整指南：AI 短剧和 AI 漫剧角色一致性》 | 成功 |
| ImageToPrompt《Stable Diffusion vs Midjourney vs DALL-E 3 vs Flux：提示词差异全面解析》 | 成功 |
| PromptMake《Midjourney --cref Guide (2026)》 | 成功 |
| PromptMake《Negative Prompts in 2026 Across Models》 | 成功 |
| zhang-jian.com《Seedream 4.0 使用指南：文生图、图像编辑与多图参考融合》 | 成功 |
| gptimage2.hk《用 GPT Image 2 制作 3D 皮克斯风格角色》 | 成功 |
| OpenAI developers《Image prompting》 | 部分（正文为导航目录，正文段未取得；另据 search 摘要引用 cookbok gpt-image-1.5 指南要点） |
| php.cn《即梦ai角色参考图使用技巧》 | 失败（返回空内容；仅用搜索摘要） |

### 检索引用（站名/标题）

- 三视图/角色表：imagesv2.ai《Ai 角色设定表提示词：三视图+表情表完整写法》；CSDN《用 GPT-Image-2 生成人物特写+三视图》；GitHub/chenxing3060/character-sheet-generator；头条《专业AI人物三视图提示词》；知乎《Ai漫剧-人物三视图提示词》；CSDN《26_AI角色一致性难题，用"三视图"一招破解》；tahou.com《AI漫剧人物角色一致性角色三视图万能公式》；OpenNana《专业角色三视图设定参考图》；FlowPix《三视图AI绘画怎么搞》
- Midjourney 一致性：promptmake.net《--cref Guide》；aiarty.com《How to Create Consistent Characters in Midjourney》；geratools.com《Character Reference (--cref) Guide》；cropupai.com《--cref: Complete Guide》《Seeds & Consistency: Limits Without --cref》；picovix.app《Consistent Character in Midjourney (2026)》；media.io《Character Reference Guide》；midjourney-ai.uk《Character Consistency Workflow (CREF)》；creatide.ai《SREF vs CREF》《7-Step Cref Tutorial》；Midjourney 官方文档《Seeds》；prompt-architects.com《Midjourney Seed: Not for Saving Styles》；aituts.com《Midjourney's -seed explained》；aidigitalspace.com《Midjourney Character Consistency - 4 ways》；知乎《万字干货!Midjourney 如何控制角色一致性？》
- Flux/PuLID/ID 系：runcomfy.com《PuLID Flux II in ComfyUI》《Flux Kontext Pulid》；oneplaceforai.com《PuLID: Face and Character Consistency》；civitai.com《Flux PuLID Face Swap Inpainting Workflow》；selfielabstudio.com《Flux 2 Multi-Ref Character Consistency Guide》；GitHub/iFayens/ComfyUI-PuLID-Flux2；runflow.io《ComfyUI Consistent Character With FLUX》；media.io《ComfyUI Consistent Characters: IP-Adapter, PuLID and LoRA》；aiindigo.com《PuLID-FLUX Tutorial》；aiofm.info《PuLID vs InstantID vs IP-Adapter FaceID: 2026 Showdown》；iimagined.ai《Face LoRA vs InstantID vs IP-Adapter》；arxiv.org《InstantID: Zero-shot Identity-Preserving Generation》；CSDN《IP-Adapter 和 InstantID 的核心机制比较》；Gera Tools《PhotoMaker & InstantID Guide》；Reddit r/StableDiffusion《IP adapter FaceID vs InstantID》
- 即梦/Seedream：知乎《即梦AI如何保持漫画人物一致性》《小白必看!即梦ai多人物一致性》；头条《如何通过提示词解决即梦AI的人物一致性》《即梦ai如何保持漫画人物一致性》《即梦豆包，官方 Seedream 4.0-4.5 提示词指南》；搜狐《即梦图片3.0智能垫图》；CSDN《即梦ai提示词实战：结构化写法与模板》；即梦提示词完全实战指南（derince0529-ops.github.io）；php.cn《即梦ai角色参考图使用技巧》（仅摘要）；seed.bytedance.com《Seedream 4.0》；CSDN/cnblogs/volcengine《Seedream 4.0 使用指南详解》；知乎《即梦4.0 完整使用指南》《Seedream 4.0 教程：比 Nano Banana 更懂中文》；sider.ai《用 Seedream 4.0 和参考图像实现风格一致性》
- Nano Banana/GPT-Image：selfielabstudio.com《Nano Banana 2 Character Consistency Prompts Guide》《Nano Banana Pro: Perfect Character Consistency Guide》；promptlibrary.space《How to Use Reference Images in GPT Image 2, Nano Banana 2…》；nanobananalib.com《GPT Image 1.5 multi-image consistency》；techyheaven.com《Nano Banana Pro Character Consistency》；nanobananatool.com《Nano Banana 2 Character Consistency with Reference Images》；gptimg.co《Nano Banana Reference Images (Subject Identity Guide)》；crun.ai / pixelbin.io《Nano Banana Prompt Guide》；OpenAI developers《gpt-image-1.5 Prompting Guide (cookbook)》《Image prompting》；Promptomania《GPT Image 1 — Prompting Guide》；fal.ai《GPT Image 1.5 Prompt Guide》；Civitai Education《Civitai's Guide to GPT Image 1》；GitHub/jamez-bondos/awesome-gpt4o-images
- 场景/光影一致性：B站《保持场景一致性!100%成功的方案!（九宫格/俯视图）》《AI视频场景一致性完整工作流》《AI多角度一致性出图流程和光影切换提示词指令》《AI多角度风格一致性工具升级》；CSDN《AI 绘画进阶必学：光影重构底层逻辑》；什么值得买《如何用AI生成场景一致性超高的多视角图？》《角色不崩、场景不乱!AI绘画人物与背景一致性的保姆级实战攻略》；知乎《Qwen Multiangle 多角度一致性》；腾讯云《Midjourney进阶：光影控制详解》；CSDN《SD【角色一致性】：不同视角创造一致的人物角色》
- 提示词公式/质量词：eastondev.com《Stable Diffusion Prompt Guide: Structure, Weights, Templates》；dreamdrive.ai《SD Prompts: Structure, Weights, Negatives》；neurocanvas.net《SD Prompting: Beginner to Pro》；promptmake.net《SD Prompt Guide 2026》《SDXL Prompt Guide: Weights, Negatives》；artpromptsgenerator.org《Negative Prompts in Stable Diffusion》；qwe.edu.pl《SD Prompt Weights: Syntax Guide》；generativelabs.com《SD prompt syntax FAQ》；discover.oreateai.com《How to Write Technical Prompts…（Quality Soup 失效）》；freeaipromptmaker.com《SDXL Prompt Guide (2026)》；groprompt.com《Do HD, 8K and 4K Keywords Actually Work in Midjourney?》；Reddit r/midjourney《Does the use of "4K","8K","Ultra" affect the image?》；Medium《The Prompt Formula That Actually Works Across Midjourney, GPT…》；masterprompting.net《Image Generation Prompting Guide》
- 中英差异/横评：搜狐《英文提示词vs中文提示词，AI到底更理解哪个？》；CSDN/devpress《Midjourney/Stable Diffusion 提示词分类宝典（中英文对照表）》；CSDN《Midjourney和Stable Diffusion实战》；知乎《Stable Diffusion 和 Midjourney优劣势比较》；developer.baidu.com《SD与Midjourney：风格提示词的实践解析》；腾讯云/阿里云/CSDN《AI绘画提示词创作指南：DALL·E 2、MJ 和 SD 大比拼》；findimageprompt.com / kenerateai.com / thepromptbench.com / sjlyedu.com / zetrax.app 负面提示词横评；promptorb.ai / toolstacky.com / artpromptsgenerator.org《Flux vs Midjourney vs SD Prompt Differences》
- 景别/镜头：知乎《从"远景"到"特写"：AI绘画景别提示词全解析》《超全总结!13个ai摄影景别提示词》；Yolo Lab《电影景别有哪些？＋Ai 景別提示詞》；Floniks《镜头景别全解析》；小黄技术栈《常用镜头与分镜提示词速查表》；shot.gpsx.io《镜头语言速查系统》；CSDN/腾讯云《Midjourney进阶：景别详解》；搜狐《Ai绘图技巧：从极远景到特写的提示词》；jsnoteclub.com《Stable Diffusion 镜头拍摄 Prompt 中英文汇总》
- 风格化：Reddit r/midjourney《What prompts can I use to achieve this artstyle?》；Reddit r/StableDiffusion《cel shaded anime style》；smartaiedits.com《Midjourney Prompt Guide (2026)》；AtomWords《cel shading prompt》；PromptHero/stablediffusionweb（cel shading 标签库）；promptkoi.com《30+ Best Anime AI Prompts》；aiunpacking.com / ai-chemists.com《AI Image Prompts Guide》；抖音/可灵官方《风格提示词集合：皮克斯、吉卜力、赛博朋克、国风插画》；百度文库《3D动画风格提示词怎么写？5步打造皮克斯质感》；原创力文档《赛博朋克AI提示词.xlsx》；NavXD 提示词库；知乎《AI绘画风格全指南：50+画风提示词》；aimindwork.com《Midjourney V7 皮克斯动画风 --sref 3687830488》
- 人物+场景融合：贝果科技《ChatGPT 生图提示词与改图指令（2026-10）》；CSDN《如何让Stable Diffusion在不同场景保持人物形象的一致性》；tahou.com《GPT Image 2人物提示词技巧》；知乎《一个文生图角色一致性工具》《Ai生图如何人物风格每张都一致呢？》；pixverse.ai《如何用 AI 保持角色一致》；renoise.ai《AI 角色一致性实战指南》；B站《comfyui+flux精准塑造人物场景一致性指南》
- 漫剧工程化：知乎《Ai漫剧提示词模板全集》《漫剧Prompt不是玄学》；头条《AI漫剧全流程提示词手册》《做Ai漫剧不用瞎写提示词》；CSDN《Ai漫剧分镜脚本提示词大全》《Ai漫剧新手避坑指南》；GitHub/4022chat/zaoju-prompt（450+ 条提示词库）；tahou.com《一文读懂AI漫剧分镜：7大核心要素》

### 未能抓取/无结果

- php.cn 即梦角色参考图页（抓取返回空）
- OpenAI developers《Image prompting》正文（仅得导航；要点改引 cookbook 摘要）
- 2 组查询无结果（"8k RAW quality tag myth" 精确措辞、"cyberpunk photorealistic pitfalls" 英文组合），均已用替代查询补上
- ref:// 短链 3 条（Medium 提示词公式、IP-Adapter vs InstantID 技术对比、PhotoMaker vs InstantID）未展开全文，仅用搜索摘要

---

## ⑦ 与现有做法的冲突 / 修正建议

针对 `work/CLAUDE.md` 与 manju-pipeline 现行规则：

1. **"出图风格标准：3D 都市动漫·卡通渲染（cel-shading）"——建议补一句禁令**：提示词中**禁止混入写实摄影词**（85mm、DSLR、skin pores、photorealistic），它们与 cel-shading 对冲（gptimage2.hk 实测）。建议在 pre_gen_gate 的风格检查里加"写实词黑名单"。
2. **画质词策略需分平台，不要统一挂 8k/RAW**：8k/RAW/masterpiece 是**模型相关**的弱偏置——动漫 Booru 底模上 masterpiece 有效、SDXL 写实上反而拉向绘画、Flux/MJ/GPT/即梦上基本是噪声（Promgrammer 实测 + groprompt + BFL 官方）。若现有模板统一附加"8k, ultra-detailed, RAW"，建议改为：即梦/SD 动漫底模保留 2-3 个质量词且放最前；其余平台删掉换成**具体材质/镜头词**。
3. **负面提示词不能跨平台照搬**：Flux、GPT-Image、Nano Banana、即梦/Seedream **没有负面词通道**（BFL 官方、PromptMake 2026 横评）；Midjourney 只有 `--no` 且 3-5 词为宜。若 pre_gen_gate 或模板对所有平台输出统一负面墙，在 Flux/即梦上是纯浪费甚至被 T5 反读。建议按③的负面词通道表分流。
4. **Midjourney 种子 ≠ 人物锁定**：官方文档明言 seed "Not for Saving Styles"，锁不住脸跨场景（Midjourney 官方、cropupai）。若工作流依赖"固定 seed 保人物"，应改为 **--cref/--cw 80 + 原样重复人物锚点段**，seed 仅用于 A/B 测试。
5. **只写角色名 ≠ 模型拿到角色图**：Arcloop 明确警告"只在提示词里写角色名或文件名，并不会让模型获得那张图片"。这与"素材关联"硬闸同向，建议 gate 校验里把"露脸镜头必须显式携带角色参考图输入位（而非仅文本提及角色名）"写成硬条件。
6. **三视图验收不能只看"像不像"**：应按 Arcloop 清单逐项核对（脚底基线/头身比/侧面轮廓线/服装正背延续/不对称物不换边），并注意"五官对齐≠头部体积正确"；修改后必须整体重验（修下巴会带动颈和发际线）。
7. **多参考图必须写"职责分工"**：即梦/Seedream 多图融合的头号翻车点是"参考关系混乱"（zhang-jian）——若素材关联只挂图不写"图一供人物、图二供场景、图三供服装"，效果大打折扣。建议模板固定"每图一句职责"。
8. **中文提示词在即梦链路是合法的**：不必强行全部英化——SD/MJ 走英文（CLIP 损耗），即梦/Seedream 用中文结构化（官方中文语义第一梯队）；Flux 两者皆可。按目标模型分流，而非一刀切。
9. **"一图一变量"原则**：多镜批量生成时一次只变（动作/景别/表情/服装/场景）中的一项，全变必漂（gptimage2.hk、Arcloop）。与分镜批量出图的效率诉求有张力——建议每批先锚点后扩散，而不是每镜独立自由生成。
10. **光影四件套进模板**：现有分镜细节 250 字下限之外，建议固定"光源位置+类型+色温/时段"字段进 prompt 模板并逐镜复制（CSDN 光影重构 + B站多角度光影切换实践），这是"同场景多镜统一"最便宜的杠杆。
