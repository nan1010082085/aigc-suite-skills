# 素材侧三 Skill 证据来源审计（character-studio / scene-studio / prop-studio）

- 审计日期：2026-10-31
- 范围：`aigc-suite-skills/skills/{character-studio,scene-studio,prop-studio}/` 下全部 10 个 .md（SKILL.md + references/），共 567 行
- 性质：只读审计，未改动任何 skill 文件
- 审计对象：硬要求/规则/参数/模板句/词表口径；跳过 frontmatter、目录、"何时使用"路由等纯元信息

## 分级口径

| 级 | 定义 |
|----|------|
| **U** | 用户令：标注「用户令/用户原话/用户定/用户定版/用户终定」+ 日期 |
| **O** | 外部官方：标注官方文档/官方指南且有可核查出处 |
| **C** | 外部调研/社区：标注调研/社区/他人实测且有可核查出处 |
| **S** | 自测实证：标注「实测/翻车/教训/事故」但无外部出处 |
| **G** | 无标注/推测/杜撰嫌疑 |

边界档（为审计诚实性单列，向主档合并计数）：

- **U?**：行文明显属 2026-10-28 用户定版批次（如 prop-prompts 标题「2026-10-28 二版」），但没有「用户定」字样 → 计数并入 U 并打问号
- **C?**：标注「行业提炼/行业标准/调研提炼」但出处仅为内部转述（`manhua-production-standard.md` 头注=「行业流水线提炼 · 2026-10-28 用户供」；prop「调研提炼」无任何出处），无可核查外部源 → 计数并入 G 档缺口（按 rubric「有出处才够 C」降档），行内保留 C? 便于回溯

另设 **G(契约)**：项目自定义 LOCKED 字段/格式/文件夹契约，属约定而非事实断言，无来源标注，按 rubric 计 G，但修法是"补一条契约决定记录"而非"查外部资料"。

## 交叉引用核验（先做的可信度地基）

skill 内所有 `shared/*`、`tools/*`、跨 skill 引用均实际存在并可解析：`shared/{output-formats,prompt-formula,lighting-system,lessons,hard-gates,pre-gen-research,manhua-production-standard,backends}.md`、`tools/{brand_scan,credit_gate,prompt_selfcheck}.py`、`skills/video-producer/references/video-consistency.md` 均在。**未发现指向不存在文件的杜撰引用**，仅一处节号引用错误（见"内部一致性缺陷"D3）。

注意：`shared/manhua-production-standard.md` 自身头注为「行业流水线提炼 · 2026-10-28 用户供」——凡三个 studio skill 以「行业工艺/行业字段」名义引用它的条目，实为**用户转述的行业经验**，无可核查外部源，故记 C?。

---

## 一、character-studio

### SKILL.md

| 文件:行号 | 条目摘要 | 级 | 原标注文字 |
|---|---|---|---|
| character-studio/SKILL.md:8 | 基础形象设定卡=三视图+表情板+服饰道具特写合一身份锚、随剧本阶段演进、设定卡=出视频时角色参考图唯一入口 | U | 「2026-10-28 用户定版」（character-prompts.md:7） |
| character-studio/SKILL.md:8 | 「人物建模质量是留存三主轴之一——本 skill 是它的唯一出口」 | G | 无标注（"留存三主轴"框架自造，见杜撰清单 Z1） |
| character-studio/SKILL.md:18 | 读剧本建人物清单+出场顺序表；外貌锚点一字不差；主要角色加名条、龙套不加 | C? | 「行业工艺总纲见 `shared/manhua-production-standard.md`」（用户供转述，无外部源） |
| character-studio/SKILL.md:18 | 人设卡行业完整字段：外貌细到脸型/眼型/瞳色/唇形/发型、固定穿搭每套配图、禁止项、角色色卡、表情库 6–8 种、三角度参考 | C? | 「按行业完整字段」 |
| character-studio/SKILL.md:18 | characters[]/outfits[] 按 character-asset-system §一 登记 | G(契约) | 无标注 |
| character-studio/SKILL.md:19 | 出图前置调研四步固定工序、禁止跳过（检索→对齐→出指令→沉淀） | G | 「执行 `shared/pre-gen-research.md` 四步」（该文件自身亦无来源标注） |
| character-studio/SKILL.md:20 | 设定卡合一排版（三视图+表情板 6 格+服饰特写分块）、纯白底影棚柔光、抽卡择优锁 visual_id、随阶段演进出新卡命名「角色-基础形象A/B/C+阶段范围」、本卡=该阶段所有分镜/出视频角色参考唯一入口 | U | 「2026-10-28 用户定版」 |
| character-studio/SKILL.md:21 | 服装三视图/表情表 i2i 挂主体强制同光影/站姿/机位；服装逐件写死+配饰拆解；表情解剖式写法 | S | 「卫衣漂裙装教训」等 `shared/lessons.md` 实测教训 |
| character-studio/SKILL.md:22 | 面部身份卡/色卡供近景与调色对齐 | G | 无标注 |
| character-studio/SKILL.md:23 | 交付写 assets.json（LOCKED 字段逐字）、与分镜 `素材映射[]` 逐镜对账、露脸角色全挂 | S | 「`shared/output-formats.md` §3」+「`shared/lessons.md`」（第 13 条双人镜漏挂） |
| character-studio/SKILL.md:27 | 一致性两层控制：人物基准层锁身份→场景融合层锁光影，两层缺一必漂 | C? | 「`shared/prompt-formula.md` §二」（内称「行业标准做法」无外部出处，见 Z2） |
| character-studio/SKILL.md:28 | t2i/i2i 分工：主体 t2i 文字控构图；模块 i2i+构图硬锁句防参考图排版锚走 | S | 「lessons 第 1 条」+ 2026-10-28 xyq 实测 |
| character-studio/SKILL.md:29 | 广告闸：手持物/商品素色无品牌+禁包装特写，过 `tools/brand_scan.py` | S | 「`shared/hard-gates.md` §6」+ lessons 9 |
| character-studio/SKILL.md:30 | 花钱门：扣积分出图走 `tools/credit_gate.py`（报价→用户批→跑） | G | 无标注（流程契约；语义与全局出图闸一致但 skill 内未标用户令） |
| character-studio/SKILL.md:31 | 出图验收清单逐张过（五官锚点/机位正交/服装逐件/手部完整/无品牌/表情差异） | G | 引用 character-prompts §4，清单本身无标注 |
| character-studio/SKILL.md:32 | 设定卡避坑五条（A 站姿无动作/配色结构统一/纯白背景/表情板绑识别点/本卡即唯一入口） | G | 「（character-prompts.md §1.1）」无日期（疑随用户定版派生） |
| character-studio/SKILL.md:33 | 一枪一停、重制不夹带、验真只认新产物 | S | 「`shared/hard-gates.md`」+ lessons 6/7 |
| character-studio/SKILL.md:34 | 违禁词/裸英文过 `tools/prompt_selfcheck.py`，后端方言长度按 `shared/backends.md` | G | 无标注（工具链契约） |
| character-studio/SKILL.md:38 | assets.json characters[]/outfits[] 字段名逐字 LOCKED 契约 | G(契约) | 「`shared/output-formats.md` §3 LOCKED 契约」 |
| character-studio/SKILL.md:39 | 人物生图指令五段式组装、代码块交付、按目标后端方言 | G | 「`shared/prompt-formula.md` §四」 |
| character-studio/SKILL.md:40 | 对账表（角色×镜头×挂载节点）交 shot-qa 素材校验 | G(契约) | 无标注 |

### references/character-asset-system.md

| 文件:行号 | 条目摘要 | 级 | 原标注文字 |
|---|---|---|---|
| character-asset-system.md:3-4 | 字段名 LOCKED 契约、改名一律回 output-formats 提 | G(契约) | 「LOCKED 契约」 |
| character-asset-system.md:11 | visual_id = `node_`+10 位小写字母数字；注册后不换、不复用 | G(契约) | 无标注（格式疑对齐外部节点 ID，见 Z4） |
| character-asset-system.md:12 | three_view 锁脸/身材/头身比永久、中性基础款服装、t2i 定稿即锁 | S | lessons 1/3 派生 |
| character-asset-system.md:13 | face_card=面部特写+色卡（主色/发色/瞳色/肤色调） | G | 无标注 |
| character-asset-system.md:14 | expressions[] i2i 挂主体；每格只写表情解剖（眉/眼/嘴/神态收束 25–40 字） | S+G | lessons 4（实测）；「25–40 字」参数无标注（见 Z3） |
| character-asset-system.md:22 | t2i 文字控构图；i2i 垫图会锚死视角景别 | S | 「lessons 第 1 条」 |
| character-asset-system.md:23 | 三视图同条件：同站姿（双臂稍离躯干）/同身高尺度/同相机高度/同光照；头顶鞋底完整入画 | G | 无标注（三视图工艺，外部方法论存在） |
| character-asset-system.md:24 | 先补看不见的部分：后领/衣长/背面接缝/不对称细节（角色自身哪侧）先写死 | G | 无标注 |
| character-asset-system.md:25 | 定稿写 visual_id 锁定，永不再改 | G(契约) | 无标注 |
| character-asset-system.md:30 | 构图硬锁句必备「单人单图、正常站姿、忽略参考图排版」 | S | lessons 1 解法（⚠与 character-prompts.md:47/102 实测结论冲突，见 D2） |
| character-asset-system.md:31 | 表情表外貌/年龄/妆感/背景/风格只在布局头写一次；禁 6 字碎片、禁每格抄全外貌 | S | lessons 4/12 |
| character-asset-system.md:32 | 单人立绘（视频 ref 用）同规则；设定图/三视图永远不是视频素材 | S | 「lessons 第 5 条」 |
| character-asset-system.md:36 | 服装逐件写死（上装版型+颜色+面料/下装/鞋袜/配饰）——只写「休闲装」必漂 | S | 「卫衣漂裙装教训」 |
| character-asset-system.md:37 | 配饰逐件登记「名称+佩戴位置+角色自身左右」；不对称配饰禁换边、禁整图镜像 | G | 无标注 |
| character-asset-system.md:38 | 服装命名「剧情语义+关键件」，一套一图一登记 | G(契约) | 无标注 |
| character-asset-system.md:39 | 同源铁律：分镜服装描写与服装提示词段同源；换装回写 outfits[] 对账 | S | lessons 3 解法 |
| character-asset-system.md:44 | 每图复述同一组固定特征短语+「细节一致，无变化」 | G | 无标注（提示词口径，有效性无实测/出处） |
| character-asset-system.md:45 | 主体 t2i；模块 i2i 挂主体+构图硬锁句 | S | lessons 1 |
| character-asset-system.md:46 | 角色写国籍（中国角色明写「中国面孔」）防出欧美脸 | G | 无标注（社区常用法，未查外部） |
| character-asset-system.md:47 | 生图只写固定景别，不写运镜词 | G | 无标注 |
| character-asset-system.md:48 | 露脸角色全挂、双人镜逐人挂 | S | 「`shared/lessons.md`」（第 13 条） |
| character-asset-system.md:49 | 术语准确、特征具体（「银色短发狼尾」而非「好看的发型」） | G | 无标注 |
| character-asset-system.md:50 | 不对称细节写死角色自身左右 | G | 无标注 |
| character-asset-system.md:51 | 广告闸：素色无品牌+禁包装特写，过 brand_scan.py | S | 「`tools/brand_scan.py`」+ hard-gates §6 |
| character-asset-system.md:52 | 重制不夹带；扣积分走花钱门 | G | 无标注（hard-gates §5 未标用户令） |

### references/character-prompts.md

| 文件:行号 | 条目摘要 | 级 | 原标注文字 |
|---|---|---|---|
| character-prompts.md:3 | 五段式见 prompt-formula §四；风格段从风格 skill 取；负面段按 backends 方言 | G | 指针句，无标注 |
| character-prompts.md:7 | 一张设定卡=三视图+表情板+服饰道具特写三区合一；本卡=后续所有分镜/镜头角色参考图唯一入口 | U | 「2026-10-28 用户定版」 |
| character-prompts.md:8 | 基础形象随剧本阶段演进即出新卡，命名「角色-基础形象A（EP001-010）」带阶段范围 | U | 同上块 |
| character-prompts.md:10-22 | 设定卡模板句：标准A站姿手脚自然张开无动作、右上 6 格表情板绑定核心识别点、右下服饰特写 3–5 块、影棚柔光、造型配色结构完全统一、不要多余人/文字、高清4K | U+G | 模板=「2026-10-28 用户定版」；「6 格」「3–5 块」「4K」参数无标注 |
| character-prompts.md:24-29 | 避坑五条硬规则（禁动态姿势防三视图跑偏/统一句必须在场/纯白背景禁场景/表情板绑识别点禁真人五官/本卡即参考唯一入口） | G | 「避坑五条（硬规则，逐条必守）」无日期（疑随用户定版派生） |
| character-prompts.md:31 | t2i 抽卡 2–4 张择优后锁定 visual_id | G | 「要点」无标注 |
| character-prompts.md:32 | 排版强化：t2i 易无视宫格排版；对策=逐格显式定位/验收必查缺格重抽/顽固时分区 i2i 拼版 | S | 「2026-10-27 Qwen-Image 实测翻车点」 |
| character-prompts.md:33 | 显式排版锁有效（三格正交一次过）；合一设定卡按模板逐区显式定位出图 | S | 「xyq 实测验证（2026-10-28 · 智能图片V2.5 Pro）」 |
| character-prompts.md:37-45 | 服装三视图模板：同光影站姿机位、逐件写死、图中标注部件清单、构图锁禁改发型发色/身高比例/新增道具/背景场景 | U?+G | 无独立标注（随 2026-10-28 实测修正口径写成） |
| character-prompts.md:47 | i2i 参考图排版是锚定的，「忽略参考图排版」压不住（实测复刻宫格）；服装三视图要的正是复刻属正确行为；单人格立绘走 §1.7 画框锁 | S | 「2026-10-28 xyq 实测修正」 |
| character-prompts.md:51-61 | 表情表 2×2 模板：每格眉/眼/嘴/神态收束写满 25–40 字、四格差异明确、标签贴人设禁通用、构图锁四格纯脸禁气泡 | G | 无标注（⚠与 SKILL.md「表情板 6 格/表情库 6–8 种」口径并存，见 D4） |
| character-prompts.md:63 | 每格只写表情解剖，外貌由参考图锁；同脸解药=写满写差异 | S | lessons 4 派生 |
| character-prompts.md:67-71 | 面部身份卡/色卡模板（正面免冠、中性表情、色卡条四项、无背景无道具） | G | 无标注 |
| character-prompts.md:75-79 | 人物×场景融合图模板（一致性第二层、面部光线与环境光一致、真实阴影投影） | C? | 「一致性第二层」= prompt-formula §二「行业标准做法」无出处 |
| character-prompts.md:83-86 | 角色参考卡模板（一大两小三视图、纯浅灰底、无文字标注） | G | 无标注 |
| character-prompts.md:88 | 用途=图生视频/IP-Adapter/角色 LoRA 的参考入口；视频层每镜只挂本卡+该镜服装三视图 | G | 外部机制名词（IP-Adapter/LoRA）未挂官方出处；用量规则指 video-consistency §一（内部） |
| character-prompts.md:92-100 | 剧情立绘模板：单人格画框锁（仅一名人物/仅一个画面格/无分格/无特写小图/无画中画）+取景下缘写死切点 | S | 源自 :102 实测教训 |
| character-prompts.md:102 | i2i 复刻宫格排版教训+画框锁解法+v2 复测验证（画框锁生效；小偏差信物被加珠粒→配饰类补「无珠无坠」） | S | 「2026-10-28 xyq 实测教训」「v2 复测验证」 |
| character-prompts.md:104-111 | 出图验收清单六项（五官锚点/机位正交/服装图中标注/手部完整/无品牌/表情四格差异） | G | 无标注 |
| character-prompts.md:113 | 任一不过→修指令写回 Notion→从 Notion 取文重抽；禁止临时改写提示词 | U | 全局工作流「Notion 是唯一控制面」（CLAUDE.md 2026-10-18 用户令；skill 内未标日期） |

---

## 二、scene-studio

### SKILL.md

| 文件:行号 | 条目摘要 | 级 | 原标注文字 |
|---|---|---|---|
| scene-studio/SKILL.md:8 | 一场景一主图（必要时变体）、光影锁定全镜共用 | G(契约) | 无标注 |
| scene-studio/SKILL.md:8 | 「场景转场连贯是留存三主轴之一」 | G | 无标注（自造框架，见 Z1） |
| scene-studio/SKILL.md:18 | 读剧本建场景清单、登记 scenes[]（含光影锁定）、每景建场景设定卡（行业字段） | C? | 「总纲见 `shared/manhua-production-standard.md` §四」 |
| scene-studio/SKILL.md:18 | 固定物件清单（道具不能凭空消失）、天气/时段多版本、场景分层（远景/中景/前景遮挡，前景模糊做景深） | C? | 「行业字段」 |
| scene-studio/SKILL.md:18 | 「竖版 9:16 构图机位」 | C?⚠ | 「行业字段」——与 manhua-production-standard §一「2026-10-28 用户终定：统一 16:9 横版」直接冲突（见 D1） |
| scene-studio/SKILL.md:19 | 出图前置调研四步（与人物 skill 同工序） | G | 「`shared/pre-gen-research.md` 四步」 |
| scene-studio/SKILL.md:20 | 镜头前缀三选一（全景默认/中景对话/特写背景），同场景同光影只换前缀出变体 | S | 2026-10-28 xyq 实测教训（scene-shot-light.md:7） |
| scene-studio/SKILL.md:20 | 光影配套时段型预设（白天顺光柔和/黄昏暖侧逆光/夜单一暖顶光）+「和角色光影匹配」 | U | 「2026-10-28 用户定」（scene-shot-light.md） |
| scene-studio/SKILL.md:21 | 场景变体 i2i 挂主图、同机位同光影只改道具层 | G | 无标注 |
| scene-studio/SKILL.md:22 | 交付 assets.json scenes[]（LOCKED 逐字）、与素材映射对账、场景必挂 | G(契约) | 「`shared/output-formats.md` §3」 |
| scene-studio/SKILL.md:26 | 空镜铁律：绝对无人物/人群/剪影/手——有人场景不能用于出视频，重出 | G⚠ | skill 内无标注；实为全局「出图/出视频五道硬闸」第 4 条（CLAUDE.md 2026-10-19 用户令）——应补标 U |
| scene-studio/SKILL.md:27 | 贴人五条（无人物写死/中心留空/无文字水印/风格锁死/低饱和不抢戏） | U | 「`references/scene-shot-light.md`」+「2026-10-28 用户定」 |
| scene-studio/SKILL.md:28 | 光影配套：与角色设定卡（柔和影棚柔光）匹配；禁杂乱多光源/强硬阴影/大面积刺眼光斑；锁定值细化不违反光质预设 | U | 「2026-10-28 用户定」 |
| scene-studio/SKILL.md:29 | 光影锁定=环境层+主光层写入，情绪层留分镜逐镜微调；同场景所有镜头共用 | C? | 「`shared/lighting-system.md` 三层」（三层体系无外部出处） |
| scene-studio/SKILL.md:30 | 广告闸：商品/陈设/灯牌素色无品牌无文字，过 brand_scan.py | S | 「`tools/brand_scan.py`」+ hard-gates §6 |
| scene-studio/SKILL.md:31 | 花钱门 credit_gate.py | G | 无标注 |
| scene-studio/SKILL.md:32 | 验收清单四项：无人物/光影一致/可行动空间/门向与道具连续性 | G | 「`scene-library.md` §4」无标注 |
| scene-studio/SKILL.md:33 | 一枪一停、重制不夹带 | G | 「`shared/hard-gates.md`」 |
| scene-studio/SKILL.md:37-39 | 产出格式（scenes[] 契约）/五段式组装/对账表交 shot-qa | G(契约) | 无标注 |

### references/scene-asset-system.md

| 文件:行号 | 条目摘要 | 级 | 原标注文字 |
|---|---|---|---|
| scene-asset-system.md:3 | 字段名 LOCKED 契约指针 | G(契约) | 「LOCKED 契约」 |
| scene-asset-system.md:9-11 | 台账三字段建法（名与素材映射逐字一致/纯空镜/光影锁定同景共用） | G(契约) | 无标注 |
| scene-asset-system.md:15 | 空镜铁律：不出现人/人群/人潮/剪影/手，人物靠资产挂参考，有人即重出 | G⚠ | 无标注（同 SKILL.md:26，实为 2026-10-19 用户令五道硬闸第 4 条） |
| scene-asset-system.md:16 | 道具文字/品牌一律「无文字、无商标、无品牌标识」 | S | 「广告闸，过 `tools/brand_scan.py`」 |
| scene-asset-system.md:17 | 场景图=该场景光影基调来源；同场景共用一主图+同一光影锁定描述 | G | 无标注 |
| scene-asset-system.md:21 | 同一场景全剧只出一张主图（必要时+一张昼夜切换版） | G | 无标注 |
| scene-asset-system.md:22 | 变体图=同机位同光影只改道具层，i2i 挂原场景图 | G | 无标注 |
| scene-asset-system.md:23 | 留可行动空间（人物将站/走的位置）；关键道具入画（门向、持物台面）——连续性靠场景资产交代 | C? | 无标注（影视连续性方法论，外部资料存在） |
| scene-asset-system.md:24 | 分镜转场交代（时间+地点）与场景资产呼应：场景名=转场旁白点名的地点 | G | 无标注 |
| scene-asset-system.md:28-32 | 场景侧自检五项（无人物含虚化人群/光影与锁定值一致/可行动空间/门向摆位连续/无品牌无文字） | G | 无标注 |

### references/scene-library.md

| 文件:行号 | 条目摘要 | 级 | 原标注文字 |
|---|---|---|---|
| scene-library.md:3 | 模板通用结构（〔风格句〕。〔类别配方〕。空镜无人物。构图锁固定机位无文字无品牌。〔负面段〕） | G | 无标注 |
| scene-library.md:6-16 | 十类高频场景配方表（粉系直播间/客厅/卧室/厨房餐厅/玄关/街道夜景/车内/校园教室/办公室/咖啡店——逐类构图必备道具+光影色调） | G | 全表无标注（场景美术配方词表，外部概念设计资料存在） |
| scene-library.md:18 | 自定义场景：先定最近似类别的基调再替换道具；光影沿用该类别配方并写入光影锁定 | G | 无标注 |
| scene-library.md:22-26 | 双语示例（即梦中文 / MJ/Flux 英文） | G | 无标注 |
| scene-library.md:28-30 | 验收清单指针 | — | （指针，不计条目） |

### references/scene-shot-light.md（标题级「2026-10-28 用户定」覆盖全篇）

| 文件:行号 | 条目摘要 | 级 | 原标注文字 |
|---|---|---|---|
| scene-shot-light.md:1 | 全篇口径（镜头变体×光影配套×贴人规则）用户定 | U | 「2026-10-28 用户定」 |
| scene-shot-light.md:3 | 核心原则：场景与角色风格统一、方便贴人、光影可控、构图适配短剧；背景衬托不抢戏 | U | 同上 |
| scene-shot-light.md:7 | 前缀只是引导，变体必须连正文一起改 | S | 「2026-10-28 xyq 实测教训：只换前缀=三张几乎一模一样，白烧积分」 |
| scene-shot-light.md:9-13 | 镜头类型表：全景/中景/特写背景的前缀+正文必须同步改（删远景元素/主体改单件小物放大/构图锁改写） | U+S | 「2026-10-28 用户定」表 + 实测教训 |
| scene-shot-light.md:15 | 一场景默认全景主图；验收必查三张互不重复（构图/景别/取景肉眼可辨），重复即重写正文重出 | S | 实测教训延伸 |
| scene-shot-light.md:19 | 角色设定卡=柔和均匀影棚柔光；场景光影必须与角色光影匹配，否则贴人必违和 | U | 「2026-10-28 用户定」 |
| scene-shot-light.md:21-25 | 时段型光影预设三条（白天顺光/黄昏暖侧逆光/室内夜单一暖顶光暗部不死黑） | U | 同上 |
| scene-shot-light.md:27 | 固定光影模板句「柔和侧顺光，阴影过渡自然，环境光统一，和角色光影匹配」 | U | 同上 |
| scene-shot-light.md:28 | 避免：杂乱多光源、强硬阴影、大面积刺眼光斑 | U | 同上 |
| scene-shot-light.md:29 | 光影锁定值在预设基础上细化（光源位置/色温/时段），不得违反光质约束 | U | 同上 |
| scene-shot-light.md:33-37 | 贴人避坑五条（禁 AI 自动生成路人/中心留空/无字含 logo 涂鸦/风格锁死/低饱和弱化背景） | U | 同上 |
| scene-shot-light.md:41-47 | 五段式场景指令模板（风格锁段/镜头前缀/光影预设+锁定值/氛围/构图锁） | U | 同上 |

---

## 三、prop-studio

### SKILL.md

| 文件:行号 | 条目摘要 | 级 | 原标注文字 |
|---|---|---|---|
| prop-studio/SKILL.md:8 | 道具=独立第三类素材（人物是演员、场景是舞台、道具=会被拿起/移动/单独给镜头的物件）；道具随剧情演进，每状态独立素材、状态本身是看点 | U | 「2026-10-28 用户定版」（prop-asset-system.md:3） |
| prop-studio/SKILL.md:18 | 剧本拆解表出图前必做，抓 4 类信息（文本描述/剧情功能/归属角色/世界观时代），逐行定稿才出图 | U | 同上 |
| prop-studio/SKILL.md:19-21 | 分类判定：✅单独出图（手持/佩戴/会变化/要特写动效）vs ❌画进场景（固定装饰） | U | 同上 |
| prop-studio/SKILL.md:22 | 通用道具与角色专属道具分栏登记 | U | 同上 |
| prop-studio/SKILL.md:23 | 出图前置调研四步 | G | 「`shared/pre-gen-research.md` 四步」 |
| prop-studio/SKILL.md:24 | 道具主图 t2i 白底/透明底 PNG；复杂道具三视图（正/侧）简单道具一张主视图；造型锚点短语写死跨状态跨镜复述一字不差；大小比例参考入图 | U | 用户定版 §三/§五 |
| prop-studio/SKILL.md:25 | 状态变体=独立素材（【合上的笔记本】【翻开第3页】是两张图）；同光影同画风只改状态要素；旧状态退役不改图 | U | 用户定版 §二 |
| prop-studio/SKILL.md:26 | 交付 props[] LOCKED（引 §3.4）、文件夹归档、特写版+远景版两套、与素材映射对账点名道具全挂 | G(契约)⚠ | 「`shared/output-formats.md` §3.4」——节号引用错误（见 D3） |
| prop-studio/SKILL.md:27 | 校对+试嵌入两步（剧本对照校验/嵌入测试：比例自然、光影融入不像贴纸、特写可读） | U | 用户定版 §五 |
| prop-studio/SKILL.md:27 | 「发『浮』=阴影方向或饱和度不匹配」 | G | 无标注（诊断断言） |
| prop-studio/SKILL.md:31 | 分类判定硬规则：会被拿起/移动/特写/变化的才单独出图，判错=素材浪费或分层失败 | U | 用户定版 §一 |
| prop-studio/SKILL.md:32 | 造型锁定防穿帮：「AI 生成每款花纹形状都会漂」；提示词固定一套，状态变体 i2i 挂主图（重绘幅度 0.3–0.4），禁每状态重新 t2i | S+G | 实测类断言无标；「0.3–0.4」参数无出处（见 Z5） |
| prop-studio/SKILL.md:33 | 刻字不进 AI 生成（AI 小字必乱码）：先出无字版、后期手动加字保剧本文字准确 | S | 「AI 翻车」实操纪律 |
| prop-studio/SKILL.md:34 | 痕迹克制：只加剧本逻辑支持的；剧本没写的不乱加 | U | 用户定版 §四 |
| prop-studio/SKILL.md:35 | 比例基准=主角手掌统一比例尺，全剧道具统一「和手掌对比」 | U | 用户定版 §三 |
| prop-studio/SKILL.md:36 | 状态=独立素材，禁止一张图混多个状态 | U | 用户定版 §二 |
| prop-studio/SKILL.md:37 | 比例参考在图（带参照物或比例标注） | U | 用户定版 §五 |
| prop-studio/SKILL.md:38 | 广告闸：无品牌无商标无包装特写，真实商品素色化 | S+U | 「`shared/hard-gates.md` §6」+ 用户定版 |
| prop-studio/SKILL.md:39 | 花钱门/一枪一停/重制不夹带 | G | 无标注 |
| prop-studio/SKILL.md:40 | 幂等自检：新道具与既有撞形先查重再建 | U | 用户定版 §二「撞形先查重」 |
| prop-studio/SKILL.md:44-46 | props[] 契约/道具版五段式/对账表交 shot-qa | G(契约) | 无标注 |

### references/prop-asset-system.md（标题级「2026-10-28 用户定版（两批方法论合并）」）

| 文件:行号 | 条目摘要 | 级 | 原标注文字 |
|---|---|---|---|
| prop-asset-system.md:3 | 核心一句话（道具=塞进剧本/角色/镜头信息服务剧情）+一句话分工 | U | 「2026-10-28 用户定版」 |
| prop-asset-system.md:7-12 | 拆解 4 类信息细则：材质/新旧/破损痕迹逐项、剧情功能四问（特写→高清/变化→多张/伏笔→隐藏细节/情绪→破旧感）、归属角色贴合人设、世界观时代避穿越道具 | U | 同上 |
| prop-asset-system.md:16-18 | 拆解表模板（7 列含材质光影备注；银戒指例） | U | 同上 |
| prop-asset-system.md:20 | 避坑：道具和剧本脱节的根源=只看名词，忽略新旧/痕迹/细节/用途 | U | 同上 |
| prop-asset-system.md:24-28 | 分类判定表（动作/变化/镜头三行对照） | U | 同上 |
| prop-asset-system.md:32-34 | 命名「道具名-状态」（常态省略）；状态=独立素材禁原图修改覆盖；两类道具+撞形先查重 | U | 同上 |
| prop-asset-system.md:38 | 比例基准=主角手掌比例尺（吊坠=半个手掌、长刀=1.2 人高例）；「AI 比例易崩」统一基准强制约束 | U+G | 用户定版；断言「AI 比例易崩」无标 |
| prop-asset-system.md:39 | 光影色调统一：先定全剧光影规则（主光源方向/硬光软光/冷暖基调），与人设/场景卡光影匹配，否则悬浮违和 | U | 同上 |
| prop-asset-system.md:40 | 线条上色风格对齐（粗黑卡通线/日系平涂/厚涂写实），防道具写实+人物 Q 版割裂 | U | 同上 |
| prop-asset-system.md:41 | 图层输出透明底 PNG；特写版+远景版两套（远景简化细节） | U | 同上 |
| prop-asset-system.md:45-48 | 痕迹三类：使用痕迹/个人印记/暗示剧情（各带例） | U | 同上 |
| prop-asset-system.md:50 | 克制原则：痕迹要有理由，禁堆无意义花纹；剧本没写的不加 | U | 同上 |
| prop-asset-system.md:52 | 原画三原则：轮廓优先/功能先于装饰/蓝图属性（三视图同轴对齐/比例一致/材质倒角标注） | C? | 「2026-10-28 调研提炼」无出处 |
| prop-asset-system.md:53 | 例：❌干净好看的牛皮笔记本 → ✅磨白胶带墨点信物 | U | 同上 |
| prop-asset-system.md:57 | 交付五项（白底透明底 PNG/复杂三视图简单主视图/标注三要素/状态名入文件名/统一画风光影） | U | 同上 |
| prop-asset-system.md:60-62 | 校对两步（剧本对照校验/嵌入测试）；「浮」两个病根=阴影方向不对、饱和度不匹配 | U+G | 用户定版；病根断言无标 |
| prop-asset-system.md:66-73 | 工程文件夹结构（人物/场景/道具+通用/角色专属） | G(契约) | 无标注 |
| prop-asset-system.md:77-88 | assets.json props[] 示例契约（白瓷茶壶，含状态数组/比例参考/备注） | G(契约) | 无标注 |
| prop-asset-system.md:92-96 | 常见踩坑五条（脱离人设/细节无依据/忽略镜头/光影自成一派/不做版本） | U | 同上 |

### references/prop-prompts.md（标题「2026-10-28 二版」）

| 文件:行号 | 条目摘要 | 级 | 原标注文字 |
|---|---|---|---|
| prop-prompts.md:3 | 提示词结构七段（主体+剧本描述+使用痕迹+材质光影+画风约束+分层要求+负面词）；核心纪律（锚点写死/比例入图/透明底/一图一物一状态） | U? | 「2026-10-28 二版」（版本标注，无「用户定」字样） |
| prop-prompts.md:7-15 | 通用模板（复杂道具三视图 t2i：正/侧/四分之三透视同轴对齐+材质纹理特写分块+部件拆解小图；负面提示词句） | U? | 同上 |
| prop-prompts.md:20 | 简单道具：单张主视图居中+旁附细节特写 | U? | 同上 |
| prop-prompts.md:24-29 | 状态变体模板（i2i 挂主图=唯一合法出法；只改状态要素，禁改造型花纹禁变形） | U? | 同上 |
| prop-prompts.md:33 | 文字/刻字乱码：不让 AI 生成小字，后期 PS/Procreate 手动加字（刻字/标签/编号一律后期加） | S | 「AI 翻车三解法（实操纪律）」 |
| prop-prompts.md:34 | 每次生成长得不一样：固定种子+固定画风词；首张合格图存参考图，后续 i2i 重绘幅度 0.3–0.4 | S+G | 同上；参数无出处（见 Z5） |
| prop-prompts.md:35 | 光影脱节：i2i 同时挂本集人物/场景图作风格参考（光比、色调对齐） | S | 同上 |
| prop-prompts.md:38-40 | 特写版+远景版两套交付（特写拉满/远景省材质纹理层不糊脸） | U? | 同上 |
| prop-prompts.md:44 | 手绘方案备用：草图进场景缩略图核对比例→细化→分层绘制（固有色/阴影/高光层） | G | 无标注 |
| prop-prompts.md:46-50 | 原画三原则（设计层纪律） | C? | 「2026-10-28 调研提炼」无出处 |
| prop-prompts.md:54-58 | 防穿帮五条（锚点一字不差/比例参考在图/白底透明底一图一物一状态/光影匹配/无品牌） | U? | 同上 |
| prop-prompts.md:62-72 | 《实测项目A》信物-原色示例提示词+状态谱系走 i2i（浅红/三成/最后一截/断裂）；刻字类道具图内不生成文字 | S | 示例为实测产出案例（「防乱码保准确」实操） |

---

## 计数（按行/条目计）

| 级 | character-studio | scene-studio | prop-studio | 合计 |
|----|----|----|----|----|
| U（含 U?） | 8 | 18 | 28 | **54** |
| O（外部官方有出处） | 0 | 0 | 0 | **0** |
| C（外部调研有出处） | 0 | 0 | 0 | **0** |
| C?（标注行业/调研但无出处，降档计入缺口） | 3 | 6 | 2 | **11** |
| S（自测实证） | 13 | 4 | 5 | **22** |
| G（无标注/契约/疑似杜撰） | 17 | 18 | 8 | **43** |
| 合计 | 41 | 46 | 43 | **130** |

主档口径：U=54、O=0、C=0、S=22、G=54（43 G + 11 C?）。

**一眼结论：全库 O 级=0、C 级=0——130 条硬要求里没有任何一条挂着可核查的外部出处。** U 级占 42%（用户定批次覆盖好），但凡涉外部事实/参数/方法论的条目全部悬空。

---

## 缺口清单

### A. G 级全部条目（43 条，按主题归并）

**A1 流程/工序类（无来源标注）**
1. 出图前置调研四步固定工序（character-studio/SKILL.md:19、scene-studio/SKILL.md:19、prop-studio/SKILL.md:23；pre-gen-research.md 自身也无出处）
2. 花钱门报价→用户批→跑（character-studio/SKILL.md:30、scene-studio/SKILL.md:31、prop-studio/SKILL.md:39）
3. 一枪一停、重制不夹带（character-studio/SKILL.md:33、scene-studio/SKILL.md:33、prop-studio/SKILL.md:39 部分）
4. 违禁词/裸英文过 prompt_selfcheck.py、后端方言长度按 backends.md（character-studio/SKILL.md:34）

**A2 人物方法论（外部方法论明显存在未查）**
5. 三视图同条件（同站姿双臂稍离躯干/同身高尺度/同相机高度/头顶鞋底入画）（character-asset-system.md:23）
6. 先补看不见的部分（后领/衣长/背面接缝/不对称左右）（character-asset-system.md:24）
7. 表情表参数与写法（25–40 字/2×2/6 格/6–8 种口径）（character-prompts.md:51-61、character-asset-system.md:14）
8. 配饰登记「名称+佩戴位置+角色自身左右」（character-asset-system.md:37）
9. 面部身份卡/色卡模板（character-prompts.md:67-71、character-asset-system.md:13）
10. 「每图复述固定特征短语+『细节一致，无变化』」（character-asset-system.md:44）
11. 角色写国籍（「中国面孔」）防欧美脸（character-asset-system.md:46）
12. 生图只写固定景别不写运镜词（character-asset-system.md:47）
13. 术语准确特征具体（character-asset-system.md:49）
14. 不对称细节写死角色自身左右（character-asset-system.md:50、:37 重复口径）
15. 设定卡避坑五条（character-studio/SKILL.md:32、character-prompts.md:24-29）
16. 抽卡 2–4 张择优（character-prompts.md:31）
17. 角色参考卡/剧情立绘模板无出处部分（character-prompts.md:83-86、:92-100 模板句）
18. IP-Adapter/角色 LoRA 参考入口用法（character-prompts.md:88）——外部技术名词未挂官方文档

**A3 场景方法论（外部方法论明显存在未查）**
19. 十类场景配方表全表（scene-library.md:6-16）——场景概念设计/美术 kit 方法论
20. 模板通用结构/自定义场景近似法（scene-library.md:3、:18）
21. 场景变体 i2i 挂主图只改道具层（scene-asset-system.md:22、scene-studio/SKILL.md:21）
22. 转场交代场景名=旁白点名地点（scene-asset-system.md:24）
23. 场景侧自检五项/验收四项含门向连续性（scene-asset-system.md:28-32、scene-studio/SKILL.md:32）
24. 一场景一主图+昼夜切换版（scene-asset-system.md:17、:21、scene-studio/SKILL.md:8）

**A4 道具类**
25. 「发『浮』=阴影方向或饱和度不匹配」诊断断言（prop-studio/SKILL.md:27、prop-asset-system.md:62）
26. 手绘方案（prop-prompts.md:44）
27. 常见踩坑五条属 U? 未落签（prop-asset-system.md:92-96）

**A5 契约/格式类（补"契约决定记录"即可）**
28. visual_id `node_`+10 位小写字母数字（character-asset-system.md:11、output-formats.md:63）
29. assets.json LOCKED 字段全集（character-studio/SKILL.md:38、scene-studio/SKILL.md:37、prop-studio/SKILL.md:44）
30. 服装命名「剧情语境+关键件」、道具命名「道具名-状态」（character-asset-system.md:38、prop 两条为 U）
31. 工程文件夹结构（prop-asset-system.md:66-73）
32. 五段式组装公式（character-studio/SKILL.md:39、scene-studio/SKILL.md:38）
33. 对账表交 shot-qa 流程（三个 SKILL.md 产出段）
34. "留存三主轴" 框架（character-studio/SKILL.md:8、scene-studio/SKILL.md:8）——兼疑似杜撰 Z1

### B. C?/S 级中「外部官方/方法论资料明显存在但我们没查过」的主题（优先补查）

| # | 主题 | 涉及条目 | 明显存在的外部资料类型 |
|---|------|---------|------------------|
| B1 | 三视图/角色设定表（character sheet）方法论 | A2-5/6/9、manhua-production-standard §三 | 动画/游戏行业角色设定集规范、原画教程（三视图正交、头身比、转面） |
| B2 | 表情表（expression sheet）方法论 | A2-7 | 动画表情表标准做法（转面表情、极端表情对） |
| B3 | 服装拆解/ costume breakdown 方法论 | A2-8 | 服装设定、角色圣经 costume 设计规范 |
| B4 | 三视图/蓝图属性「原画三原则」 | prop-asset-system.md:52、prop-prompts.md:46-50（标「调研提炼」无出处） | 概念设计/工业设计蓝图（orthographic/blueprint）方法论 |
| B5 | 即梦/Seedream 图像官方指南、出图参数官方口径 | 全部模板句的「高清4K」「负面词」「固定种子」等 | 即梦/Seedream 官方文档、模型卡 |
| B6 | i2i 重绘幅度（denoising strength）0.3–0.4 | prop-studio/SKILL.md:32、prop-prompts.md:34 | SD/即梦 img2img 参数官方说明、社区实测区间 |
| B7 | 「AI 小字必乱码」 | prop-studio/SKILL.md:33、prop-prompts.md:33 | 图像模型文字渲染能力的官方说明/论文 |
| B8 | 「固定种子+固定画风词」 | prop-prompts.md:34 | 需查即梦/xyq 后端是否支持 seed——可能与后端能力不符 |
| B9 | 三层光影体系（环境/主光/情绪）、时段型预设 | scene-studio/SKILL.md:29、scene-shot-light.md §二 | 影视布光方法论（三点布光、色温时段惯例） |
| B10 | 一致性两层控制「行业标准做法」 | character-studio/SKILL.md:27、character-prompts.md:75-79 | IP-Adapter/角色一致性官方论文与文档 |
| B11 | 影视连续性（可行动空间/门向/道具摆位） | scene-asset-system.md:23、scene-studio/SKILL.md:32 | 影视连续性（continuity）教材/行业规范 |
| B12 | 空镜铁律出处标注 | scene-studio/SKILL.md:26、scene-asset-system.md:15 | 不需外部查——应补标「2026-10-19 用户令五道硬闸第 4 条」 |
| B13 | 「行业工艺总纲」整体 | manhua-production-standard.md（被 character/scene skill 引为「行业字段」） | 头注仅「行业流水线提炼 · 2026-10-28 用户供」，建议补一条可核查外部源或改称「本项目工艺约定」 |

---

## 疑似杜撰/包装过度清单

| # | 条目 | 位置 | 判断 |
|---|------|------|------|
| Z1 | 「留存三主轴」+「本 skill 是它的唯一出口」 | character-studio/SKILL.md:8、scene-studio/SKILL.md:8 | 自造增长框架当既定事实陈述，无任何出处；「唯一出口」措辞是自我包装。要么补用户令出处，要么改写为本套件约定 |
| Z2 | 「一致性两层控制=跨镜同人的行业标准做法」 | 经 prompt-formula §二 引入 character-studio/SKILL.md:27 | 「行业标准」标签无出处；做法本身（基准图+融合层）在 IP-Adapter/LoRA 社区确有对应实践，但"行业标准"的定性是包装 |
| Z3 | 「每格表情解剖写满 25–40 字」 | character-asset-system.md:14、character-prompts.md:58 | 精确到区间的参数无任何来源，典型"像编的精度"。实用但应标「经验值（待实测校准）」 |
| Z4 | visual_id=`node_`+10 位小写字母数字 | character-asset-system.md:11、output-formats.md:63 | 精确格式无出处。若对齐 xyq 真实节点 ID 格式应标注来源；若随手定的应标「契约约定」 |
| Z5 | 「重绘幅度 0.3–0.4」 | prop-studio/SKILL.md:32、prop-prompts.md:34 | 机制真实（img2img denoising），但区间无出处、且跨后端未必通用（即梦/xyq 的"重绘幅度"口径与 SD 不同） |
| Z6 | 「AI 生成每款花纹形状都会漂」「AI 小字必乱码」「AI 比例易崩」 | prop-studio/SKILL.md:32-33、prop-asset-system.md:38 | 绝对化断言（每/必）口语经验包装成定律；行为方向大体属实但措辞过度 |
| Z7 | 表情板示例「黑色LED显示屏脸/黄色疑惑脸、红色愤怒脸、绿色笑脸、蓝色平静脸、粉色爱心眼、白色懵圈脸」 | character-prompts.md:13-18 | 疑似把《实测项目A》某具体角色（屏幕脸）的特例表情色卡泛化为通用模板示例——以偏概全风险；作示例无害但不宜写成通则 |
| Z8 | 十类场景配方的精确光影配置（「暖粉主调，屏幕冷光+补光灯双光源」等） | scene-library.md:6-16 | 配方化包装，无出处；美术上合理但来源不明，宜标「本套件词表口径」 |

结论：**未发现"对不上任何真实机制"的纯虚构条目**——所有可疑项都是"真实做法 + 无出处的精确参数/自造定性"的包装过度型。

---

## 内部一致性缺陷（顺带发现，建议一并修）

| # | 缺陷 | 位置 | 严重度 |
|---|------|------|--------|
| D1 | **画幅口径冲突**：scene-studio 引「竖版 9:16 构图机位」，但 manhua-production-standard §一「2026-10-28 用户终定：统一 16:9 横版（竖版 9:16 会导致素材生成不全）」——该冲突源自 shared 标准自身（§四未随 §一 改 16:9 而更新），scene-studio 照抄了陈旧口径 | scene-studio/SKILL.md:18 ← manhua-production-standard.md §一 vs §四 | **高** |
| D2 | **被实测证伪的话术仍列为必备**：character-asset-system.md:30 把「忽略参考图排版」写进构图硬锁句必备，但 character-prompts.md:47/102（2026-10-28 xyq 实测）明确该句"压不住"，解法已改为正面画框锁 | character-asset-system.md:30 vs character-prompts.md:47/102 | **高** |
| D3 | **节号引用错误**：prop-studio/SKILL.md:26 引「`shared/output-formats.md` §3.4」，output-formats.md 无 3.4 小节（props[] 在 §3 内，行 83） | prop-studio/SKILL.md:26 | 中 |
| D4 | **表情口径三套并存**：SKILL.md「表情库 6–8 种」「表情板 6 格」「不止 2×2」 vs character-prompts §1.3「表情表 2×2 四格」——设定卡表情板与独立表情表两种物料的数量口径未在文中对齐说明 | character-studio/SKILL.md:18/20 vs character-prompts.md:49-61 | 中 |
| D5 | character-prompts.md 章节编号跳跃（§1.7 后直接 §4） | character-prompts.md:104 | 低 |
| D6 | 空镜铁律（有人场景不能用于出视频）实为 2026-10-19 用户令五道硬闸第 4 条，skill 内未标用户令——按本 rubric 被降为 G | scene-studio/SKILL.md:26、scene-asset-system.md:15 | 低（补标即可） |

---

## 修复建议（按性价比排序）

1. **补 D1 画幅口径**：scene-studio/SKILL.md:18 与 manhua-production-standard §四 的「竖版 9:16」统一为「16:9 横版（2026-10-28 用户终定）」。
2. **改 D2 话术**：character-asset-system.md:30 的构图硬锁句删「忽略参考图排版」或加注"已被实测证伪，单人格走 §1.7 画框锁"。
3. **补用户令标注**：空镜铁律（D6）、花钱门、Notion 重抽（character-prompts.md:113）补「2026-10-19/10-18 用户令」字样，升 U。
4. **参数类补"经验值"标记**：25–40 字、0.3–0.4、抽卡 2–4 张、node_+10 位（Z3/Z4/Z5）标「经验值/契约约定，待实测校准」。
5. **B 组主题补查外部源**（优先 B5 即梦官方参数口径、B6 重绘幅度、B8 seed 支持）：查到后升 C/O，查不到降格改写。
6. **「留存三主轴」「行业标准」定性**（Z1/Z2）：改为"本套件约定"或补出处。
7. **prop-studio/SKILL.md:26 节号**改「§3」。
