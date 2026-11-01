# 批次 2 调研报告：图像侧官方机制（即梦/Seedream 参数、设定表工艺、文字渲染、一致性边界）

- 日期：2026-10-31
- 目标：为素材侧（人物/场景/道具出图）130 条硬要求补外部官方来源；每条结论标注来源 URL + 性质（**官方** / **社区** / **推测**）
- 检索：中英双语 ≥10 组检索；深抓 ≥12 页（火山方舟 API 文档全文 3 段、BytePlus 教程、Seed 官网模型页、Arcloop 三视图手册、Krea 官方博客、ezcharacter 表情表指南、arXiv IP-Adapter、catchmeta/mooko 服装拆解、GitHub 官方文档复刻等）
- 约束执行：skill 文件只读未改动；查不到的在「⑥ 空白清单」明说，未编造

---

## ① 即梦 / Seedream 官方参数与能力

来源主轴：火山方舟《图片生成 API》官方文档（2026-10-14 更新，全文 43k 字已抓完）+ BytePlus/火山《图片生成教程》+ Seed 官网 Seedream 4.0 页。

### 1.1 提示词（prompt）官方口径 【官方】

- 语言：所有模型支持中英文提示词；Seedream 5.0 pro/flash 另支持俄/阿/菲/泰/土/韩/马/西/葡/印尼/法/德/越/日共 15 种语言。
- **字数上限官方建议：中文 ≤300 字、英文 ≤600 词**。原话：「字数过多信息容易分散，模型可能因此忽略细节，只关注重点，**造成图片缺失部分元素**」。
  → 这是「长提示词导致丢元素」的唯一直接官方依据，可直接写进 skill 当硬要求。
- 来源：https://www.volcengine.com/docs/82379/1541523

### 1.2 尺寸/分辨率官方参数 【官方】

- 双模式（不可混用）：
  - 方式 1（推荐）：`size` 传档位（Seedream 4.0 可选 **1K / 2K / 4K**；4.5 为 2K/4K；5.0 lite 为 2K/3K/4K；5.0 pro/flash 为 1K/1.5K/2K），再在 prompt 里用自然语言描述宽高比/形状/用途，**由模型判断最终大小**。
  - 方式 2：`size` 传具体「宽x高」像素。Seedream 4.0：总像素须 ∈ [1280x720(921600), 4096x4096(16777216)]，宽高比 ∈ [1/16, 16]，默认 2048x2048。
- Seedream 4.0 档位映射参考值（官方表，节选）：2K 档 16:9 = 2848x1600、1:1 = 2048x2048、9:16 = 1600x2848、21:9 = 3136x1344；4K 档 16:9 = 5504x3040。
- 7 个标准宽高比：1:1、4:3、3:4、16:9、9:16、3:2、2:3、21:9。
- 来源：https://www.volcengine.com/docs/82379/1541523

### 1.3 seed 支持：**官方图片生成 API 无 seed 参数** 【官方（否定结论）】

- 通读官方《图片生成 API》全部请求参数（prompt、image、layer_decomposition、size、optimize_prompt_options、output_format、background、response_format、sequential_image_generation(_options)、stream、tools、watermark、model）——**没有 seed、没有 guidance_scale、没有 strength/denoise**。
- 对 skill 的意义：即梦/Seedream 出图链路**不能承诺 seed 复现**；「锁参数复现」只能锁 prompt/参考图/size 等参数，不能锁 seed。社区文章（CSDN 即梦教程提到「随机种子/CFG」）描述的疑似 SD 系参数，与官方 API 对不上，按**社区存疑**处理。
- 反例存在：第三方中转文档（AIML API）声称 "same seed same output"，但该说法不在火山官方文档中，不采信为官方口径。
- 来源：https://www.volcengine.com/docs/82379/1541523 （否定结论基于全文核对）

### 1.4 负面词（negative prompt）：**官方 API 无 negative_prompt 参数** 【官方（否定结论）】

- 同上全文核对，无该字段。想排除内容只能在 prompt 里**正向陈述**（官方 i2i 示例即此写法：「保持模特姿势不变。将服装材质从银色金属改为……」）。
- skill 中凡写「负面词」的条目，在即梦/Seedream 后端应降级为「prompt 正向排除句」，不能假设负面词生效。

### 1.5 图生图 / i2i「重绘幅度」官方口径：**无重绘幅度参数，指令式编辑** 【官方】

- 官方对 i2i 的定义：「基于已有图片，结合文字指令进行图像编辑：图像元素增删、风格转化、材质替换、色调迁移、改变背景/视角/尺寸等」。控制保留/改动程度的唯一手段是**提示词里的「保持 X 不变，改为 Y」句式**（官方示例原文：「保持模特姿势和液态服装的流动形状不变。将服装材质从银色金属改为完全透明的清水」）。
- 官方无 strength/denoise/重绘幅度滑杆（API 无此参数）。即梦网页端是否有「参考图强度」滑杆未在官方帮助核实到（见⑥空白）。
- 来源：https://www.volcengine.com/docs/82379/1541523 ；https://ai.byteplus.com/ark/region:ap-southeast-1/docs/image-generation-tutorial

### 1.6 多参考图官方用量与写法 【官方】

- 数量上限：Seedream 5.0 pro/flash **≤10 张**；Seedream 5.0 lite / 4.5 / **4.0 ≤14 张**；组图模式下「输入参考图数 + 生成图数 ≤ 15」。
- 单图要求：jpeg/png/webp/bmp/tiff/gif/heic/heif；宽高比 [1/16,16]；边长 >14px；≤30MB；总像素 [196, 3600 万]。
- 官方多图引用写法：prompt 里用「图1 / 图2 / 参考图1」指代输入顺序（官方示例：「将图1的服装换为图2的服装」「参考图1，生成四图片，图中人物分别带着墨镜……」）。
- 组图（sequential_image_generation="auto" + max_images）：官方定位即「**漫画分镜、品牌视觉、故事板**」一组内容关联的图片；官方示例 prompt 直接写明数量与逐张内容（「生成一组电影级科幻写实风的4张影视分镜：场景1……→场景4……」）。
- 来源：https://www.volcengine.com/docs/82379/1541523 ；https://docs.volcengine.com/docs/ark/seedream-4-0-5-0

### 1.7 官方提示词建议（结构公式）【官方复刻，次级】

- GitHub「seedream-guide」自称**官方文档完整复刻**，给出结构公式：「主体 + 行为/状态 + 环境/背景 + 风格/美学」；美学词分风格/光影/构图/质感四类；组图提示词必须写明数量与逐张内容。注意：该仓库的尺寸表有旧值错误，参数一律以火山文档为准，此公式可作次级来源。
- 官方文档内另有《Seedream 4.0-5.0 提示词指南》内链（prompt 字段处），本批未抓到全文（见⑥）。
- 来源：https://github.com/xujfcn/seedream-guide （性质：社区复刻，内容承自官方）

### 1.8 其他可写入 skill 的官方参数事实 【官方】

- `watermark` 默认 **true**（右下角「AI 生成」水印）——出片素材必须显式传 false。
- `response_format=url` 的下载链接**24 小时失效**，必须即时转存。
- `optimize_prompt_options.mode`：standard（默认，质量优先）/ fast（**仅 Seedream 4.0 与 5.0 pro 支持**，提速略降质）。
- Seedream 4.0 输出格式仅 jpeg；png 需 5.0 lite/pro/flash。
- output_tokens 计费公式：`sum(图宽*图高)/256` 取整——尺寸每升一档成本近似平方增长（4K 档 ≈ 2K 档 4 倍）。
- 来源：https://www.volcengine.com/docs/82379/1541523

---

## ② 三视图 / 表情表 / 服装拆解外部方法论

### 2.1 三视图（turnaround）工艺——Arcloop 手册（与漫剧/短剧语境直接对口）【社区/厂商教程，实测生成为据】

来源：https://arcloop.ai/handbook/zh-CN/character-turnaround-sheet-guide （深抓全文）。该手册就是「为漫剧/短剧做角色参考图」语境，且附真实生成 prompt 原文，是本批最贴合的方法论来源。

- **站姿**：「肩膀齐平并放松，头部端正，双手自然放在身体两侧。**手臂与躯干留出少量空隙，让手部和服装轮廓可见**，各个视图保持相同姿态。避免耸肩、歪胯或夸张动作；只有后续流程明确需要时才用 A-pose / T-pose」。
  → 直接校准 skill 自攒参数「双臂稍离躯干」：外部依据成立，措辞可对齐为「手臂与躯干留少量空隙、露手部与服装轮廓」。
- **入画/对齐**：「一起生成正面、标准侧面和背面的全身图，**人物尺度一致，脚底对齐**，背景简单。每个视图都应**完整露出头顶和鞋子**」；英文 prompt 原文："Feet aligned, arms slightly away from the torso, all heads and boots visible with comfortable margins"。
  → 「头顶鞋底入画」「同尺度/同基线」外部依据成立。
- **机位**：要求 "true side profile"（真侧视）与「避免夸张透视」（mooko，见 2.3），ComfyUI 官方工作流页亦称 "orthographic multi-view"（https://comfy.org/workflows/ad315e41d8c2-ad315e41d8c2/ ）。
  → 「同相机高度/正交无透视」的外部依据是「true side profile + orthographic」，skill 的「同相机高度」可改述为「正交/平视、无夸张透视」。
- **先锁脸再全身**：「全身图中脸可能只占很小一块。**增加一张较近的肖像**，可以更清楚地交代眼睛、脸型和发际线……是让已确认的设计更清晰，**不要在补特写时又生成另一套五官**」。
  → 「先锁脸再全身」外部依据成立：特写必须从同一已确认设计派生，不能重新生成五官。
- **版式两档**：漫剧/风格化 2D 用简洁三视图即可；电影/精细 3D/真人用「头部+全身」不等高四宫格（上排 1/3 高度放正/侧脸特写，下排 2/3 放正/侧全身）。注意原文明言「不代表四宫格已证明能提升视频一致性」——只补看不清的信息。
- **光影**：所有视图 "even lighting / 均匀光"，"Plain warm off-white background"。场景/背景不进设定表。
- **诚实边界（原文反复强调）**：「复杂的参考表不会自动赋予视频模型保持角色一致的能力」；「不要把『参考图里已经画清楚』当作『视频一定能够还原』」——细节（纹身/疤痕/配饰）跨镜头仍可能丢、变形、换边。
- **服装换装/多套管理**：以确认的三视图为 identity+composition reference，"Change only the outfit across all three views"，并逐件核对「领口、袖长、腰线、裙褶、裙摆、鞋子」在三视图中对应；每套服装/年龄段**独立生成、独立审阅、独立命名存档**（`character-01_adult_workwear_v01` 式命名），「不是对模型一致性的承诺」。

### 2.2 表情表（expression sheet）方法论 【社区/厂商教程】

- **格数**：ezcharacter 指南：**8 个为行业标准**（neutral, happy, sad, angry, surprised, fearful, disgusted, confident）；对话密集项目加到 12（+smug/embarrassed/exhausted/determined）；次要角色 6 个也行。「非妥协五件套」= 平静/开心/生气/害怕/惊讶。排版：**单行等距，每脸下标签**；neutral 是基线（动画插值从它出发）；缩略图尺寸下**嘴型比眉眼更能读出情绪**，要显式描述嘴部状态；锁定头部角度防各行歪头。来源：https://ezcharacter.com/how-to/design-character-expression-sheet
- **网格写法**：Krea 官方博客：「a 4x2 grid」或「a row of six expressions」，逐个点名情绪；角色描述「short and tight so it does not drift across the grid」。表情网格用方形画幅。来源：https://www.krea.ai/blog/character-design-with-krea-2
- **与我们场景的差异（诚实提示）**：Arcloop 明说「常规视频参考中，额外加入静态表情图**并不会自动提升**角色一致性……常规表情直接通过视频 Prompt 描述，只有特别夸张、视频模型难理解的表情才提供表情参考」。→ 表情表的价值主要是**人工审阅与绘制参照**，不是一致性保险。

### 2.3 服装拆解（costume breakdown）方法论 【社区/厂商教程】

- 模块清单（mooko 模板 + catchmeta prompt）：三视图 + 表情组（≥5）+ **服装分层展示（外套/内搭/下装/鞋）+ 装备局部放大与结构标注** + 色板（主/辅/点缀色 + 材质标注：布料/皮革/金属）+ 版式白底网格化。
  - mooko 血泪要点：只写「装备拆解」不写「局部放大+标注」→「只给你一把武器摆在旁边，啥也看不清」；三视图必须写「比例一致，避免夸张透视」「保持同一张脸/同一套服装**版型**」；列出「不可变特征」清单当硬约束；「避免随机新增配饰、避免换发型、避免改变服装剪裁与纹样主题」。来源：https://www.mooko.cn/article/347 （社区实操）；https://catchmeta.com/prompts/diagrammatic-character-sheet-3-view-costume-breakdown （社区 prompt 库）
  - 标注语气：细线引出、短硬标签（"Ceremonial clasp" / "Hidden hinge"）、无衬线小字、左信息栏/中三视图/右拆解区（mooko）。
  - Krea：**服装变体表 = 角色描述恒定，只有每格服装变**（"the same original character shown in five outfits — ..."），16:9 画幅；配色 3-5 个色彩词全表复用，「palette drift 是不一致的最大成因」。
  - 随身物品（包/手机/武器）**默认不进基础三视图**，单独出图参考（Arcloop）；已属服装结构的刀鞘/枪套/背带可留在身上。
  - Krea 站方 FAQ 的诚实边界：多视图「视觉一致（同衣同发色同比例）但**非像素级一致**；要像素级，先出正视图再以它为 image reference 出其他视图」。

---

## ③ 文字渲染与比例的真实口径

### 3.1 「AI 小字必乱码」——真实口径分两层

- **官方能力宣称**：Seedream 4.0 官方页展示大量文字类样例（黑板方程组、朝代时间轴、中英海报、步骤教程图），MagicBench 雷达图中「文本渲染」高分；官方宣称「精准渲染图片中的文字」。来源：https://seed.bytedance.com/zh/seedream4_0 （官方）。中文语境生成（中文 prompt 直出）官方/榜单背书见知乎测评转述（社区）。
- **社区实测的边界**（更接近可写入 skill 的硬要求）：
  - 「同一个模型画 4 个大字可能正确，但 **20 个小字几乎必错**」；「低分辨率输出、**小字号密集排版、中英混排**会进一步放大错误率」。来源：https://post.smzdm.com/p/az84x0mo/ （社区聚合，含腾讯云/知乎/搜狐等 13 个来源）
  - 社区通行对策：单块区域文字 **≤10 字**；prompt 写死文字规则（「中文清晰可读、笔画完整、不允许乱码/变形/残缺笔画」）；**成片文字后期加**（先出无文字底图，再 Canva/PS 叠字）——「AI 适合画面氛围，中文标题和重点信息自己加」。来源：同上（抖音/公众号作者汇总，社区）
  - 「汉字乱码是所有生图模型的硬伤」，选对模型解决大半；社区横评点名即梦 5.0 Pro / GPT-Image-2 / NanoBanana2 中文较好。来源：https://zhuanlan.zhihu.com/p/2063914125097547410 （社区）
- **可写入结论**：「AI 小字必乱码」应表述为**概率性硬规律**——大字/少字可直出；小字号、密集、中英混排、长句多字则错误率陡升，成片级文字默认后期叠字。官方宣称「精准文字渲染」不覆盖小字密集场景（官方无字号阈值声明——见⑥）。

### 3.2 「AI 比例易崩」——无官方承认，外部依据在方法论侧

- **无任何官方文档/研究声称「比例易崩」**（查不到，如实说明）。Seedream 官方口径反而说「通过对提示词的深度推理，**自动适配最优的图像比例尺寸**」（https://ark.volcengine.com/region:cn-beijing/model/detail?Id=doubao-seedream-4-0 ，官方）。
- 外部方法论对「比例崩」的防御口径（可写入）：
  - 三视图必须显式要求「same scale / 比例一致 / feet on one baseline / 人物尺度一致」，并「避免夸张透视」（Arcloop、mooko，社区）；
  - prompt ≤300 字防「元素缺失」是官方唯一相关硬口径（①.1）；
  - Krea：多视图「视觉一致非像素一致」，想锁比例先出正视图再图生其他视图（社区/厂商）。
- 结论：「比例易崩」保留为**经验断言（社区/实践）**，写入 skill 时给防御参数（同尺度/同基线/正交机位/短 prompt），不要标成官方结论。

---

## ④ 一致性技术真实边界（IP-Adapter / 角色 LoRA）

- **IP-Adapter 原论文（官方/学术）**：22M 参数的解耦 cross-attention 适配器，冻结底模，实现 image prompt 能力，可与 text prompt、ControlNet 类结构控制共用；效果「comparable or even better than fully fine-tuned image prompt model」——注意论文主张的是**图像提示能力**，**不是身份锁定保证**。来源：https://arxiv.org/abs/2308.06721 （官方论文）
- **IP-Adapter-FaceID（作者官方续作）**：tencent-ailab/IP-Adapter 官方 Wiki：「We use faceID embedding from a face recognition model instead of CLIP image embedding, additionally, **we use LoRA to improve ID consistency**. Hence, **IP-Adapter-FaceID = IP-Adapter + LoRA**」——官方自己承认纯 IP-Adapter 的 ID 一致性不够，需要人脸嵌入 + LoRA 补强。来源：https://github.com/tencent-ailab/IP-Adapter/wiki/IP%E2%80%90Adapter%E2%80%90Face （官方）；多脸输入增强相似度（默认 5 张）：https://huggingface.co/h94/IP-Adapter-FaceID （官方模型卡）
- **社区对比结论（真实天花板表述）**：
  - 「Trained LoRA（25–40 张图）**没有对手**（no competitor comes close）」在超一致性上；免训练参考方案里 PuLID 略优于 IP-Adapter-FaceID，InstantID 在 SDXL 上准、Flux 上不稳。来源：https://aiofm.info/en/guides/face-consistency-deep-dive （社区横评）
  - 「IP-Adapter 更快上手，LoRA 在**大角度/多角度下更稳**、更可被 prompt 控制」；主流做法是**参考式生成攒数据集 + LoRA 出片**。来源：https://loradataset.com/guides/ipadapter-vs-lora-consistent-characters （社区）
  - IP-Adapter「在大姿态变化时丢稳」；ControlNet 只管姿态结构不管身份。来源：https://www.media.io/image-tips/comfyui-consistent-characters （社区）
- **对 skill 的口径**：一致性两层控制里，参考图（即梦多参考图/图生图）≈ IP-Adapter 式「参考条件」，**天花板 = 视觉近似不等于身份保证**；跨镜长期一致性最终靠「设定卡为唯一入口 + 每镜挂资产 + 崩坏镜重生成」的流程兜底，而不是模型承诺。Krea 站方自己也只承诺「visually consistent, not pixel-perfect」。

---

## ⑤ 可直接写入 skill 的硬要求（标源）

| # | 硬要求 | 来源 | 性质 |
|---|--------|------|------|
| H1 | 即梦/Seedream 出图 prompt ≤300 汉字（英文 ≤600 词），超长会「忽略细节、缺元素」 | volcengine API 文档 | 官方 |
| H2 | 出图素材显式关闭水印（watermark=false，默认 true 会打「AI 生成」） | volcengine API 文档 | 官方 |
| H3 | 生成图 URL 24h 失效，必须生成后立即转存入库 | volcengine API 文档 | 官方 |
| H4 | 不得依赖 seed 复现；「锁参数」= 锁 prompt+参考图+size，重生成必抽卡 | volcengine API 文档（无 seed 参数） | 官方（否定式） |
| H5 | 即梦/Seedream 无负面词参数，排除内容写成 prompt 正向句（「保持 X 不变，不要出现 Y」式指令句） | volcengine API 文档（无 negative_prompt） | 官方（否定式） |
| H6 | i2i 无重绘幅度参数；改动程度用「保持 X 不变，将 Y 改为 Z」指令句控制 | volcengine API 文档 + 官方教程示例 | 官方 |
| H7 | 多参考图按「图1/图2」序号引用；Seedream 4.0 ≤14 张，组图模式参考图+生成图 ≤15 | volcengine API 文档 | 官方 |
| H8 | 组图/分镜 prompt 必须写明数量与逐张内容（官方示例句式「生成4张……场景1→场景4」） | volcengine 文档 + seedream-guide | 官方/复刻 |
| H9 | 三视图站姿：肩平放松、头正、双臂稍离躯干（露手部与服装轮廓）、禁止耸肩歪胯夸张动作；仅流程需要才 A/T-pose | arcloop 手册 | 社区（实测） |
| H10 | 三视图入画：同尺度、脚底对齐同一基线、头顶与鞋全入画留余量、真侧视（true side profile）、避免夸张透视、均匀光、纯色浅背景 | arcloop + mooko + comfy.org | 社区（实测） |
| H11 | 先锁脸再全身：脸特写必须从已确认设计派生（或同图内加格），禁止补特写时重新生成五官 | arcloop | 社区 |
| H12 | 表情表：8 格为标准（平静/喜/悲/怒/惊/惧/厌/自信），单行等距+逐格标签，平静为基线；嘴型显式描述；网格用方形画幅、4x2 或一行六格 | ezcharacter + krea | 社区/厂商 |
| H13 | 服装拆解：分层展示（外套/内搭/下装/鞋）+ 局部放大 + 结构标注（短硬标签）+ 色板材质；三视图写死「同一套服装版型（领口/袖口/腰线/下摆）」+「不可变特征」清单 + 「禁止新增配饰/换发型/改剪裁」 | mooko + catchmeta | 社区 |
| H14 | 多套服装 = 独立资产独立命名（character-XX_阶段_服装_vNN），逐套核对三视图对应后入库；每套作为独立版本审阅 | arcloop | 社区 |
| H15 | 随身道具默认不进人物三视图，单独出图 + 使用者/拿法在分镜描述 | arcloop | 社区 |
| H16 | 成片级小字（≤10 字/块可试直出；密集小字/中英混排默认后期叠字），prompt 写「文字清晰可读、笔画完整、无乱码」仅降概率不根治 | smzdm 聚合 + 知乎实测 | 社区 |
| H17 | 参考图 ≠ 一致性保证：复杂参考表可能反增混乱；生成后必须人工核对配饰换边/丢疤/变色，崩坏镜单独重生成 | arcloop + krea + aiofm | 社区/厂商 |
| H18 | 角色 LoRA > 参考式（IP-Adapter/PuLID/InstantID）在多角度身份稳定上；「参考式攒数据、LoRA 出片」是通行组合；IP-Adapter-FaceID 官方自己都要求 +LoRA 补 ID | arXiv 2308.06721 + tencent-ailab wiki + aiofm/loradataset | 官方论文+社区 |
| H19 | 即梦/Seedream 出图尺寸按「档位+prompt 自然语言描述比例」官方推荐方式；成片 16:9 用 2K 档 2848x1600 映射值；成本 ∝ 像素数（4K≈2K 的 4 倍） | volcengine API 文档 | 官方 |
| H20 | 配色一致性：每角色固定 3-5 个色彩词全表复用，「palette drift 是不一致最大成因」 | krea 博客 | 厂商 |

---

## ⑥ 空白清单（查不到 / 未证实，禁止当依据用）

1. **《Seedream 4.0-5.0 提示词指南》全文**：官方 API 文档有内链，本批未抓到独立页面 URL 与全文；仅通过官方复刻仓库得到结构公式（主体+行为+环境+风格）。待补抓。
2. **即梦帮助中心（jimeng.jianying.com 站内官方帮助）**：检索仅命中官网首页与社区教程；**未找到可抓取的官方帮助中心参数页**。即梦网页 UI 是否暴露「随机种子 / 参考图强度 / 重绘幅度」滑杆：社区文章（CSDN）说法互有矛盾且疑似搬运 SD 参数，**官方口径未证实**。
3. **文字渲染的字号阈值**：官方宣称「精准文字渲染」但无「小字于 X px 必错」的量化口径；「20 个小字几乎必错」为社区实测经验值，无官方数字。
4. **「比例易崩」的官方/研究承认**：无。仅方法论侧防御写法。
5. **IP-Adapter 在即梦/Seedream 闭源后端上的等效性**：即梦多参考图的内部机制未公开，本报告的 IP-Adapter 边界只能作「参考式一致性」类比，不能声称机制相同（推测层）。
6. **表情表/服装拆解的「行业官方标准」**：无正式行业标准文本；8 格/16:9/版式等均为厂商与社区经验聚合（ezcharacter/krea/mooko），标社区级。
7. **Dreamina（海外版）帮助中心**：与即梦同源但文档入口多为产品营销页，官方教程深度内容缺失；未深挖出参数级文档。

---

## 附：本批深抓来源清单

| # | URL | 性质 | 用途 |
|---|-----|------|------|
| 1 | https://www.volcengine.com/docs/82379/1541523 | 官方 | Seedream 4.0-5.0 API 全参数（3 段全文） |
| 2 | https://ai.byteplus.com/ark/region:ap-southeast-1/docs/image-generation-tutorial | 官方 | 模型能力对比表、i2i/多图/组图示例 |
| 3 | https://docs.volcengine.com/docs/ark/seedream-4-0-5-0 | 官方 | 中文版教程、多参考图写法 |
| 4 | https://seed.bytedance.com/zh/seedream4_0 | 官方 | 文字渲染宣称与样例、MagicBench |
| 5 | https://ark.volcengine.com/region:cn-beijing/model/detail?Id=doubao-seedream-4-0 | 官方 | 自动适配比例宣称（检索摘要） |
| 6 | https://arcloop.ai/handbook/zh-CN/character-turnaround-sheet-guide | 社区/厂商 | 三视图工艺全文（站姿/入画/锁脸/换装/边界） |
| 7 | https://ezcharacter.com/how-to/design-character-expression-sheet | 社区/厂商 | 表情表 8 格标准 |
| 8 | https://www.krea.ai/blog/character-design-with-krea-2 | 厂商官方博客 | 四类设定表 prompt 配方、LoRA 边界 |
| 9 | https://www.mooko.cn/article/347 | 社区 | 服装拆解/一致性提示词实操 |
| 10 | https://catchmeta.com/prompts/diagrammatic-character-sheet-3-view-costume-breakdown | 社区 | 三视图+拆解 prompt 模板 |
| 11 | https://arxiv.org/abs/2308.06721 | 官方论文 | IP-Adapter 能力边界 |
| 12 | https://github.com/tencent-ailab/IP-Adapter/wiki/IP%E2%80%90Adapter%E2%80%90Face | 官方 | FaceID=IP-Adapter+LoRA 表述 |
| 13 | https://post.smzdm.com/p/az84x0mo/ | 社区聚合 | 小字乱码实测口径 |
| 14 | https://github.com/xujfcn/seedream-guide | 社区复刻 | 提示词结构公式 |
| 15 | https://huggingface.co/h94/IP-Adapter-FaceID | 官方模型卡 | 多脸输入（默认 5 张） |
