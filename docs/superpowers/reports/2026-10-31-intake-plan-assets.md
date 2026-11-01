# 素材侧三档入库施工单（character-studio / scene-studio / prop-studio）

- 日期：2026-10-31
- 施工员：intake-assets（素材侧入库施工）
- 流程：**阶段 1 = 本施工单**（每条：报告条目号 → 目标文件:落点 → 档位 → 处理方式）；**阶段 2 = 按单施工**，逐条日志见文末「执行日志」
- 喂料：
  1. `2026-10-31-batch2-image-official.md` ⑤ 表 H1–H20（含①②③④节背景裁定）
  2. `2026-10-31-batch5-style-word-efficacy.md` 第④节（SSS/材质词效）
  3. 队长重点落点（三件套改写 / 三视图校准 / 表情表重定位 / 小字口径 / 一致性天花板）
  4. 第三波附加（已获批）：C 类剧内数据换占位 ×2
- 档位口径（铁律①）：**官方级**直接入，标（官方：火山方舟《图片生成 API》2026-10-14）；**社区实证级**带源入，标（社区实测：来源）；**经验值**标（经验·内部）
- 铁律执行：②U 级用户令/用户供样例一律不动（character-prompts §1.1 设定卡模板「2026-10-28 用户定版」、prop-asset-system 头注用户定版框架均保留）③禁编造报告外内容 ④被覆盖条目留注记不硬删（注记固定句式：「已被火山官方 API 校正 2026-10」）⑤逐条日志（源→落点→档位）
- 目标文件共 10 个：三 studio 的 SKILL.md + references/（character-prompts / character-asset-system / scene-asset-system / scene-library / scene-shot-light / prop-asset-system / prop-prompts）

---

## 一、施工单（36 条）

### 组 A · 三件套改写（seed / 负面词 / 重绘幅度）——官方级

| # | 源 | 目标文件:落点 | 档位 | 处理方式 |
|---|----|--------------|------|---------|
| A01 | H4 | prop-prompts.md §4.2「固定种子+固定画风词」 | 官方（否定式） | 改写为「提示词固定一套+首张合格图存参考图后续 i2i+size 固定，重生成必抽卡」；blockquote 注记保留原句并写「已被火山官方 API 校正 2026-10：无 seed 参数」 |
| A02 | H6 | prop-prompts.md §4.2「i2i 重绘幅度 0.3–0.4」 | 官方 | 改写为指令式编辑（「保持 X 不变，将 Y 改为 Z」）；注记「已被火山官方 API 校正 2026-10：无 strength/denoise/重绘幅度参数」 |
| A03 | H6 | prop-studio/SKILL.md 硬闸「状态变体走 i2i 挂主图（重绘幅度 0.3–0.4）」 | 官方 | 删参数改为「i2i 挂主图+指令式编辑句（保持 X 不变将 Y 改为 Z）」；注记同 A02 |
| A04 | H5 | prop-prompts.md §1 模板「负面提示词：复杂背景，人物，…」 | 官方（否定式） | 改写为正向排除句「排除约束（正向句）：画面中无任何人物、无复杂背景、…」；注记「已被火山官方 API 校正 2026-10：无 negative_prompt 参数」 |
| A05 | H5 | prop-prompts.md §8 示例模板「负面提示词：…」 | 官方（否定式） | 同 A04 |
| A06 | H5 | prop-prompts.md 抬头「…+ 负面词」结构行 | 官方（否定式） | 改述「+ 排除约束（正向排除句；SD 系后端有负面框才走负面词）」 |
| A07 | H5 | character-prompts.md 抬头「负面段按 `shared/backends.md` 方言」 | 官方（否定式） | 补注：即梦/Seedream 无 negative_prompt 参数，负面意图一律正向排除句；SD 系负面框才放负面词 |
| A08 | H5 | scene-library.md 模板行〔负面段〕 | 官方（否定式） | 补短注同 A07（〔负面段〕槽位=正向排除句填充） |
| A09 | H6 | prop-prompts.md §3 状态变体模板下 | 官方 | 补一行官方句式注：改动程度靠「保持 X 不变，将 Y 改为 Z」，本模板「只改状态要素，禁止改造型花纹」即此写法 |
| A10 | H6 | scene-asset-system.md §三 场景变体条 | 官方 | 补指令式编辑句式「保持机位/光影/空间结构不变，将 X 改为 Y」（原「同机位同光影只改道具层」保留为其具体化） |

### 组 B · 即梦/Seedream 调用参数块（H1/H2/H3/H4/H5/H6/H7/H8/H19）——官方级

| # | 源 | 目标文件:落点 | 档位 | 处理方式 |
|---|----|--------------|------|---------|
| A11 | H1–H8,H19 | character-prompts.md 新增「§2 即梦/Seedream 调用硬要求」（§1.7 后） | 官方 | 新增参数块：prompt ≤300 字、watermark=false、URL 24h 转存、无 seed/负面词/重绘幅度三件套替代、多参考图「图1/图2」序号 ≤14 张、size 档位+比例描述、组图=漫画分镜/故事板定位（用则写明数量+逐张内容） |
| A12 | 同上 | prop-prompts.md 新增「§9 即梦/Seedream 调用硬要求」（文末） | 官方 | 同 A11，示例句换成道具语境（状态变体编辑句、主图+场景参考「图1/图2」） |
| A13 | 同上 | scene-shot-light.md 新增「§五 即梦/Seedream 调用硬要求」 | 官方 | 同 A11，落 H19 具体值：成片 16:9 空镜用 2K 档 2848x1600 映射值、成本 ∝ 像素（4K≈2K 四倍）；H8 落场景应用：全景/中景/特写变体组可用组图模式一次出 |
| A14 | H1/H2/H3 | character-studio/SKILL.md 硬闸加一行指针 | 官方 | 「调用硬要求（官方）：watermark=false、URL 24h 失效即时转存、prompt 中文 ≤300 字」→ 指向 character-prompts §2 |
| A15 | H1/H2/H3 | scene-studio/SKILL.md 硬闸加一行指针 | 官方 | 同 A14 → scene-shot-light §五 |
| A16 | H1/H2/H3 | prop-studio/SKILL.md 硬闸加一行指针 | 官方 | 同 A14 → prop-prompts §9 |

### 组 C · 三视图工艺校准——社区实证级（Arcloop/mooko/comfy.org）

| # | 源 | 目标文件:落点 | 档位 | 处理方式 |
|---|----|--------------|------|---------|
| A17 | H9 | character-asset-system.md §二「同站姿（双臂稍离躯干）」 | 社区实测（Arcloop） | 措辞校准+带源：「手臂与躯干留少量空隙、露手部与服装轮廓」；补肩平放松/头正/禁耸肩歪胯；A-pose/T-pose 仅流程明确需要时用（U 级模板「标准A站姿」原句不动） |
| A18 | H10 | character-asset-system.md §二「同相机高度…头顶鞋底完整入画」 | 社区实测（Arcloop/mooko） | 「同相机高度」改述「正交/真侧视（true side profile）机位、避免夸张透视」；「脚底对齐同一基线」「头顶与鞋全入画留余量」「均匀光/纯色浅背景」带源印证 |
| A19 | H11 | character-asset-system.md §二 新增「先锁脸再全身」条 | 社区实测（Arcloop） | 新增：特写/面部卡从已确认设计派生（i2i 挂已锁主体或同图加格），禁止补特写时重新生成五官 |
| A20 | H11 | character-prompts.md §1.4 面部身份卡下补一行 | 社区实测（Arcloop） | 同 A19 的出法约束（从已确认设计派生） |

### 组 D · 表情表重新定位——社区实证级（Arcloop/ezcharacter/Krea）

| # | 源 | 目标文件:落点 | 档位 | 处理方式 |
|---|----|--------------|------|---------|
| A21 | H12 + ②2.2 | character-prompts.md §1.3 新增定位注+外部标准参照 | 社区实测 | 新增两注：①定位——表情表是审阅/绘制参照与镜头表情描述素材，**不自动提升视频/跨镜一致性**（Arcloop 明说），一致性靠设定卡挂载+流程兜底；②外部标准参照——8 格为行业标准（平静/喜/悲/怒/惊/惧/厌/自信），6–12 弹性、单行等距或 4×2、逐格标签、平静为基线、嘴型显式（ezcharacter/Krea）。**不动** U 级 §1.1 六格表情板布局与 2×2 模板句 |
| A22 | ②2.2 | character-asset-system.md §二 模块段/§一 expressions 行补注 | 社区实测 | 补「表情表=审阅参照非一致性保险」短注（原无逐字「=一致性保险」句，此为显式重定位；U 级合一卡结构不动） |

### 组 E · 服装拆解/多套服装/道具边界/配色——社区实证级（mooko/catchmeta/Arcloop/Krea）

| # | 源 | 目标文件:落点 | 档位 | 处理方式 |
|---|----|--------------|------|---------|
| A23 | H13 | character-prompts.md §1.2 要点区 | 社区实测（mooko/catchmeta/Arcloop） | 补服装拆解分层写法：外套/内搭/下装/鞋分层展示+装备局部放大+结构标注（细线引出、短硬标签、无衬线小字）+色板（主/辅/点缀色+材质标注）；「不可变特征」清单当硬约束；版型逐件对应（领口/袖长/腰线/裙褶/裙摆/鞋）；禁随机新增配饰/换发型/改剪裁纹样 |
| A24 | H13/H14 | character-asset-system.md §三 多套服装规则 | 社区实测（Arcloop/Krea） | 补：每套服装独立生成/独立审阅/独立命名存档（`character-XX_阶段_服装_vNN` 文件命名）；Krea 变体表公式=角色描述恒定只有服装变、配色 3–5 色词全表复用；`名` 字段现有「剧情语义+关键件」规则保留 |
| A25 | H15 | character-asset-system.md §二 新增条 | 社区实测（Arcloop） | 新增：随身道具（包/手机/武器）默认不进三视图，走 prop-studio 单独出图+使用法在分镜描述；已属服装结构的刀鞘/枪套/背带可留身上 |
| A26 | H20 | character-asset-system.md §四 新增条 | 社区实测（Krea） | 新增：每角色固定 3–5 个色彩词全表复用，「palette drift 是设定表不一致最大成因」 |

### 组 F · 小字乱码真实口径——社区实证级（smzdm 聚合/知乎）

| # | 源 | 目标文件:落点 | 档位 | 处理方式 |
|---|----|--------------|------|---------|
| A27 | H16 | prop-studio/SKILL.md 硬闸「刻字不进 AI 生成（AI 小字必乱码）」 | 社区实测 | 修订为概率性口径：4 个大字可对、20 个小字几乎必错；单块 ≤10 字可试直出+prompt 写死「文字清晰可读、笔画完整、无乱码」仅降概率；密集小字/中英混排默认后期叠字（出无字版实践保留）；注记原绝对表述已按社区实测校正 2026-10 |
| A28 | H16 | prop-prompts.md §4.1 | 社区实测 | 同 A27 |

### 组 G · 一致性真实边界/天花板——官方论文+社区实证级

| # | 源 | 目标文件:落点 | 档位 | 处理方式 |
|---|----|--------------|------|---------|
| A29 | H17/H18 + ②2.1 诚实边界 | character-asset-system.md 新增「§五 一致性真实边界」 | 社区实测+官方论文 | 新增：①参考式（IP-Adapter/PuLID/InstantID）=参考条件非身份锁——IP-Adapter 原论文只承诺图像提示能力（arXiv 2308.06721），FaceID 官方自认需 +LoRA 补 ID（tencent-ailab wiki）；②角色 LoRA 25–40 图多角度超一致性无对手、大角度更稳（社区横评：aiofm/loradataset）；通行组合=参考式攒数据+LoRA 出片；③复杂参考表不自动赋予一致性，生成后人工核对配饰换边/丢疤/变色，崩坏镜单独重生成（Arcloop/Krea）；④Krea 只承诺 visually consistent, not pixel-perfect |
| A30 | H18 | character-prompts.md §1.6 用途行后补注 | 同上 | 天花板短注+指针 §五 |
| A31 | H17 | character-studio/SKILL.md 硬闸「一致性两层控制」 | 同上 | 补短句：两层是流程下限；天花板如实（参考式≠身份保证），长期一致性靠设定卡唯一入口+每镜挂资产+崩坏镜重生成兜底 |

### 组 H · SSS/材质词效（batch5 ④）——社区实证级（含查不到边界）

| # | 源 | 目标文件:落点 | 档位 | 处理方式 |
|---|----|--------------|------|---------|
| A32 | batch5 ④ | prop-prompts.md §1 材质光影行下补「材质词效注记」 | 社区实证（Reddit/Promgrammer/Civitai） | 新增：SSS 类材质词 SD 系写实侧有效、与 3D 渲染语料强关联、Flux 需 LoRA 补；**Seedream/即梦侧无 A/B 实证（查不到）**——即梦出图材质以具象中文描述为准，SSS 属跨模型借用勿当保证；intricate details/super detail 类细节词过用产生 busy 的 AI 感纹理，克制 |
| A33 | batch5 ④ | character-prompts.md 补同短注（皮肤/服装材质域） | 同上 | 同 A32 精简版 |

### 组 I · 比例断言标注——经验·内部

| # | 源 | 目标文件:落点 | 档位 | 处理方式 |
|---|----|--------------|------|---------|
| A34 | batch2 §3.2 | prop-asset-system.md §三.1「AI 比例易崩」 | 经验·内部 | 标注为经验断言（官方无承认、查不到研究）+防御口径：同尺度/同基线/正交机位/prompt ≤300 字；禁标官方 |

### 组 J · 第三波 C 类剧内数据换占位（已获批）——纪律清理

| # | 源 | 目标文件:落点 | 档位 | 处理方式 |
|---|----|--------------|------|---------|
| A35 | 第三波（已获批） | prop-studio/SKILL.md:8 括注 | C 类清理 | 「（信物褪色/道具甲睁眼/笔记本翻页）」→「（`道具名-状态`（示例占位））」；原文留档（见下） |
| A36 | 第三波（已获批） | prop-asset-system.md:53 好坏对照 | C 类清理 | 「绑一根褪色信物」→「绑一根〔道具名-状态（示例占位）〕」；原文留档（见下） |

**原文留档（C 类，换占位前逐字存档）**：

1. prop-studio/SKILL.md:8 原文：「**道具随剧情演进**（信物褪色/道具甲睁眼/笔记本翻页），不同道具状态本身就是看点——每个状态是独立素材。」——其中（信物褪色/道具甲睁眼/笔记本翻页）为无出处剧内数据（《实测项目A》类剧目状态名），换占位；前后句不动。
2. prop-asset-system.md:53 原文：「> ❌ 干净好看的牛皮笔记本 → ✅ 封面边角磨白、书脊两道胶带、扉页干涸墨点、绑一根褪色信物（因为剧本里主角一直带着它翻看）」——「褪色信物」为无出处剧内数据，换占位；好坏对照结构与教学点（痕迹要有剧本依据）保留。

> 备注：prop-prompts.md §8 曾有《实测项目A》信物-原色完整示例，已于 2026-10-31 纪律批次替换为占位模板（现文「示例占位：剧目专属资产段勿入 skill」），本次不再重复处理。

---

## 二、不动清单（U 级保护，铁律②）

- character-prompts.md §1.1 基础形象设定卡模板全文（2026-10-28 用户定版）：含「标准A站姿，手脚自然张开，无动作」「右上区域6个头部特写表情板」「高清4K」等句——A17 的 Arcloop 站姿细则只写入 character-asset-system.md 方法段，模板字句不改
- character-prompts.md §1.1 避坑五条、§1.2/§1.7 的 2026-10-28 xyq 实测教训记录——只在相邻处加源标注/注记，不改实测结论
- prop-asset-system.md 头注「2026-10-28 用户定版」框架、§〇拆解表、§五校对两步、§七 LOCKED 契约
- 一切 `shared/*` 文件（负面对照 `shared/backends.md` 方言只加指针注，不动该文件——不属本单范围）
- 剧目专属数据（人物 LED 屏幕脸类示例等）：第三波未点名者一律不动

## 三、档位分布（施工单）

| 档位 | 条数 | 条目 |
|------|------|------|
| 官方级（直接入） | 16 | A01–A16 |
| 社区实证级（带源入） | 17 | A17–A33 |
| 经验·内部 | 1 | A34 |
| C 类清理（纪律，已获批） | 2 | A35–A36 |
| 合计 | 36 | |

---

## 四、执行日志（阶段 2 回填，2026-10-31 完成）

格式：条目 | 源 → 落点 | 档位 | 实际改动 | 状态

| # | 源 → 落点 | 档位 | 实际改动 | 状态 |
|---|----------|------|---------|------|
| A01 | H4 → prop-prompts.md §4.2 | 官方 | 「固定种子」→「提示词固定一套+size 固定+首图存参考图」，注记保留原句+「已被火山官方 API 校正 2026-10」 | done |
| A02 | H6 → prop-prompts.md §4.2 | 官方 | 「i2i 重绘幅度 0.3–0.4」→指令式编辑句，注记同上 | done |
| A03 | H6 → prop-studio/SKILL.md 硬闸 | 官方 | 「（重绘幅度 0.3–0.4）」→「i2i 挂主图+指令式编辑句」，注记同上 | done |
| A04 | H5 → prop-prompts.md §1 模板尾行 | 官方 | 「负面提示词：…」→「排除约束（正向排除句）：…」，注记保留原句 | done |
| A05 | H5 → prop-prompts.md §8 示例模板尾行 | 官方 | 同 A04 | done |
| A06 | H5 → prop-prompts.md 抬头结构行 | 官方 | 「+负面词」→「+排除约束（正向排除句）」+注记 | done |
| A07 | H5 → character-prompts.md 抬头 | 官方 | 补注：即梦/Seedream 无 negative_prompt，〔负面段〕=正向排除句 | done |
| A08 | H5 → scene-library.md 模板行 | 官方 | 补短注同 A07 | done |
| A09 | H6 → prop-prompts.md §3 模板下 | 官方 | 补「改动程度控制」注（官方句式示例原文引用） | done |
| A10 | H6 → scene-asset-system.md §三 变体条 | 官方 | 补「保持机位/光影/空间结构不变，将 X 改为 Y」指令句 | done |
| A11 | H1–H8/H19 → character-prompts.md 新增 §2 | 官方 | 9 条参数硬要求块（300 字/watermark/URL/seed/负面/重绘/图1图2/size/组图） | done |
| A12 | 同上 → prop-prompts.md 新增 §9 | 官方 | 同上，道具语境示例（状态编辑句、主图+场景参考图1图2、状态谱系组图） | done |
| A13 | 同上 → scene-shot-light.md 新增 §五 | 官方 | 同上，落 H19 具体值 2K 档 2848x1600、H8 落全景/中景/特写变体组应用 | done |
| A14 | H1/H2/H3 → character-studio/SKILL.md 硬闸 | 官方 | 新增调用硬要求指针行 → character-prompts §2 | done |
| A15 | H1/H2/H3 → scene-studio/SKILL.md 硬闸 | 官方 | 同上 → scene-shot-light §五 | done |
| A16 | H1/H2/H3 → prop-studio/SKILL.md 硬闸 | 官方 | 同上 → prop-prompts §9 | done |
| A17 | H9 → character-asset-system.md §二 站姿句 | 社区实测 | 「双臂稍离躯干」带源（Arcloop）+补肩平/头正/禁耸肩歪胯/A-pose 限定 | done |
| A18 | H10 → character-asset-system.md §二 同条件句 | 社区实测 | 「同相机高度」→「正交/真侧视（true side profile）、避免夸张透视」；脚底同基线/头顶鞋全入画/均匀光/纯色底带源 | done |
| A19 | H11 → character-asset-system.md §二 新增 | 社区实测 | 新增「先锁脸再全身」条 | done |
| A20 | H11 → character-prompts.md §1.4 | 社区实测 | 补面部卡出法注（从已确认设计派生） | done |
| A21 | H12+②2.2 → character-prompts.md §1.3 | 社区实测 | 新增「表情表定位」（不提升视频一致性，审阅参照）+「外部标准参照」（8 格/嘴型/基线）；U 级 2×2 与 6 格布局未动 | done |
| A22 | ②2.2 → character-asset-system.md §二 模块段 | 社区实测 | 补「表情表定位」条（非一致性保险） | done |
| A23 | H13 → character-prompts.md §1.2 | 社区实测 | 补服装拆解分层写法（分层/局部放大/短硬标注/色板材质/版型逐件/不可变特征清单/禁改剪裁纹样） | done |
| A24 | H13/H14 → character-asset-system.md §三 | 社区实测 | 命名条补 `character-XX_阶段_服装_vNN`；新增#6 每套独立审阅、#7 变体表公式+配色复用 | done |
| A25 | H15 → character-asset-system.md §二 新增 | 社区实测 | 新增「随身道具默认不进三视图」条 | done |
| A26 | H20 → character-asset-system.md §四 新增 #10 | 社区实测 | 新增「3–5 色彩词全表复用/palette drift」条 | done |
| A27 | H16 → prop-studio/SKILL.md 硬闸 | 社区实测 | 「AI 小字必乱码」→概率性口径（4 大字可对/20 小字必错/≤10 字可试/默认后期叠字），注记原表述 | done |
| A28 | H16 → prop-prompts.md §4.1 | 社区实测 | 同 A27 | done |
| A29 | H17/H18/②2.1 边界 → character-asset-system.md 新增 §五 | 官方论文+社区实测 | 新增「一致性真实边界」5 条（IP-Adapter 非身份锁/FaceID+LoRA/LoRA 25–40 图无对手/参考表不自动一致/Krea 非像素级/流程兜底） | done |
| A30 | H18 → character-prompts.md §1.6 | 同上 | 补天花板注+指针 §五 | done |
| A31 | H17 → character-studio/SKILL.md 硬闸 | 同上 | 一致性两层控制条补天花板短句（流程兜底） | done |
| A32 | batch5④ → prop-prompts.md §1 材质行下 | 社区实证 | 新增「材质词效注记」（SSS SD 系有效/Flux 需 LoRA/Seedream 查不到/细节词过用 busy） | done |
| A33 | batch5④ → character-prompts.md §1.1 要点区 | 社区实证 | 同 A32 精简版 | done |
| A34 | batch2 §3.2 → prop-asset-system.md §三.1 | 经验·内部 | 「AI 比例易崩」标经验断言+防御口径（官方无承认） | done |
| A35 | 第三波 C 类 → prop-studio/SKILL.md:8 | 纪律清理 | 「（信物褪色/道具甲睁眼/笔记本翻页）」→「（`道具名-状态`（示例占位））」，原文已留档 | done |
| A36 | 第三波 C 类 → prop-asset-system.md:53 | 纪律清理 | 「绑一根褪色信物」→「绑一根〔道具名-状态（示例占位）〕」，原文已留档 | done |

**施工核验**：残留扫描——`固定种子/重绘幅度 0.3/负面提示词：/信物褪色/道具甲/褪色信物/小字必乱码` 在三个 studio 目录仅存于注记留档行（铁律④要求保留原句），活指令/模板已全部改写；10 文件代码围栏配对完整（fences 偶数）；U 级模板（character-prompts §1.1 设定卡全文含「标准A站姿/6 格表情板/高清4K」、§1.1 避坑五条、§1.2/§1.7 实测教训、prop-asset-system 用户定版框架）未改动字句。

**执行统计**：36/36 done。改动文件 10/10（character-studio ×3、scene-studio ×4、prop-studio ×3）。
