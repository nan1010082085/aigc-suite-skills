# 风格 skill 证据来源审计（9 个 style skill 全部 .md）

- 日期：2026-10-31
- 审计范围：`aigc-suite-skills/skills/` 下 style-3d-anime、style-anime、style-cg-refined、style-comic、style-cyberpunk、style-fantasy、style-infinite-flow、style-photoreal、style-pixar 共 18 个文件（每个 skill：SKILL.md + references/style-profile.md）
- 审计对象：硬要求 / 风格词模板 / 风格词库 / 负面词 / 边界词表 / 翻车点与对策（跳过纯目录、流程指路、frontmatter 元信息）
- 本报告只读 skill 文件，未改动任何 skill 文件

## 分级口径

| 级 | 含义 | 判定依据 |
|----|------|---------|
| U | 用户令 | 原文标注「用户令 / 用户原话 / 用户定 / 用户方案 / 应用户要求」且带日期 |
| O | 外部官方 | 原文标注官方文档/官方指南并有出处（BFL 官方可灵官方、Seedream 官方等，含经研究 §3/§4-5 转引的官方结论） |
| C | 外部调研/社区 | 标注调研报告章节（研究 §X = `docs/superpowers/reports/2026-10-27-prompt-optimization-research.md`，该报告有来源清单 §6 与逐条站名）或社区/他人实测出处（Promgrammer、PromptMake、gptimage2.hk、Arcloop 等） |
| S | 自测实证 | 翻车点/对策口吻、或标「实测/事故/翻车修复」，但无外部出处（含链路止于内部无外部出处的条目） |
| G | 无标注/推测/杜撰嫌疑 | 无任何来源标注、显式【推测】、或引用错位（标注的出处里根本没有该内容） |

链路核实说明（本次审计顺带核了引用链，不是只看字面标注）：

- `docs/superpowers/reports/2026-10-27-prompt-optimization-research.md` 存在，含来源清单（BFL 官方、Google Cloud 官方、OpenAI cookbook、Midjourney 官方 Seeds 文档、Promgrammer《Quality Tags — A Deep Dive》固定 seed 实测、PromptMake、gptimage2.hk、Arcloop、CSDN 等），故「研究 §X」标注按 C 计；其中直接引官方文档的按 O 计
- `shared/style-library.md` 实际内容是**风格选择器与沉淀路由**（一剧一风格清单 + 取词规则 + 回写路由），**不含任何词效/负面词纪律正文**——凡引「style-library §二 / §三」当作词效出处的均为**引用错位**，按 G 计并入疑似杜撰清单
- `shared/lessons.md` 存在，是带日期的内部实战翻车日志（「漫剧实战中逐条验证过的翻车点与解法」「2026-10-28 xyq 倒吊影被拦实测」），引它按 S 计
- 研究报告 §4-x 各风格小节里**逐条未挂出处的翻车点**（如赛博「人脸受光」、皮克斯「产品图卡通化」），本表随 skill 侧标注按 C 计（表头挂了研究章节），但已在缺口清单中单列「链路末端无外部出处」主题

## 各级别条目计数

| skill | U | O | C | S | G | 合计 |
|-------|---|---|---|---|---|------|
| style-3d-anime | 0 | 0 | 0 | 5 | 18 | 23 |
| style-anime | 0 | 0 | 22 | 0 | 7 | 29 |
| style-cg-refined | 16 | 0 | 0 | 6 | 1 | 23 |
| style-comic | 0 | 0 | 0 | 0 | 7 | 7 |
| style-cyberpunk | 4 | 1 | 22 | 0 | 5 | 32 |
| style-fantasy | 0 | 0 | 0 | 0 | 6 | 6 |
| style-infinite-flow | 0 | 0 | 0 | 1 | 6 | 7 |
| style-photoreal | 0 | 13 | 9 | 0 | 6 | 28 |
| style-pixar | 0 | 0 | 22 | 0 | 7 | 29 |
| **合计** | **20** | **14** | **75** | **12** | **63** | **184** |

覆盖极不均匀：style-cg-refined 全靠用户令（U=16/23），style-anime / cyberpunk / photoreal / pixar 有调研链（C+O ≈ 75%），而 **style-3d-anime（23 条全部无外部来源）与 style-comic / fantasy / infinite-flow（合计 20 条几乎全 G）是四个零外部标注 skill**——比此前认为的三个还多一个。

---

## 逐条审计

### style-3d-anime（SKILL.md + references/style-profile.md）

| 条目 | 摘要 | 级 | 原标注文字 |
|------|------|----|-----------|
| SKILL.md:8 | 风格定位「日漫的脸，3D 的质感」，观感=顶尖 3D 二次元游戏 CG/3D 动画电影级 | G | 无 |
| SKILL.md:13 | 触发词含「米哈游风 3D 质感」（以 IP 名作质感参照） | G | 无（且与本文件 L29 禁 IP 名硬闸自相矛盾） |
| SKILL.md:18 | 硬要求：一部剧 1 种风格全剧不换、全资产共用 | G | 无（套件通用纪律） |
| SKILL.md:21 | 硬要求：脸走日漫词、材质走 3D 词分开写，缺一必漂 | G | 无 |
| SKILL.md:26 | 硬闸：禁写实真人词（photorealistic/真人皮肤质感/85mm/DSLR/明星脸），混入=恐怖谷 | G | 无（内容与研究 §7 修正 1 同向，本处未挂） |
| SKILL.md:27 | 硬闸：禁 2D 平涂词（赛璐璐/粗描边/色块平涂/扁平） | G | 无 |
| SKILL.md:28 | 硬闸：日漫造型锚+3D 渲染锚必须同时在场 | G | 无 |
| SKILL.md:29 | 硬闸：禁知名 IP/角色名 | G | 无（研究 §4-3 有同款结论，未挂） |
| style-profile.md:8 | 风格锁模板（中文整段：精致 3D 日漫 CG 渲染…3D 动画电影级画质） | G | 仅「2026-10-28 建档」 |
| style-profile.md:14 | 风格锁模板（English 版） | G | 同上 |
| style-profile.md:21 | 高效组合·脸部（日漫锚）：大眼睛/精致小巧五官/动漫比例/瞳孔高光 | G | 无 |
| style-profile.md:22 | 高效组合·皮肤毛发（3D 锚）：次表面散射/发丝根根分明 | G | 无 |
| style-profile.md:23 | 高效组合·材质：织物纹理/皮革质感/金属反光/半透明 | G | 无 |
| style-profile.md:24 | 高效组合·光影：电影级光影/明快通透/体积光/轮廓光 | G | 无 |
| style-profile.md:25 | 高效组合·画质：3D 动画电影级画质/细节清晰/高清 4K | G | 无 |
| style-profile.md:31 | 边界词表：photorealistic/85mm/DSLR/胶片颗粒/明星脸→cg-refined/photoreal，混入=恐怖谷 | G | 无 |
| style-profile.md:32 | 边界词表：赛璐璐/粗描边/色块平涂/扁平/2D 插画→style-anime | G | 无 |
| style-profile.md:33 | 边界词表：像素风/体素/乐高=风格崩坏 | G | 无 |
| style-profile.md:39 | 翻车对策：脸漂成写实脸（大眼睛词被忽略）→锚词前置+验收首查眼睛比例 | S | 「翻车点与对策」表，无日期/来源 |
| style-profile.md:40 | 翻车对策：渲染漂 2D 平涂→3D 锚在场+查皮肤体积感 | S | 同上 |
| style-profile.md:41 | 翻车对策：发丝糊成片状→写「发丝根根分明」+查发际线发梢 | S | 同上 |
| style-profile.md:42 | 翻车对策：手部畸变→沿通用验收（手指完整） | S | 同上 |
| style-profile.md:43 | 翻车对策：与 cg-refined 混写→一剧一风格整段替换 | S | 同上 |

### style-anime

| 条目 | 摘要 | 级 | 原标注文字 |
|------|------|----|-----------|
| SKILL.md:18 | 硬要求：一部剧只锁 1 种风格全剧不换 | G | 无 |
| SKILL.md:26 | 硬闸：禁写实词混入 cel 系，混入=半写实恐怖谷 | C | 「（研究 §7 修正 1）」 |
| SKILL.md:27 | 硬闸：禁知名角色名/受保护角色 | G | 无 |
| SKILL.md:28 | 硬闸：画质词按后端分流（Booru ≤3 放最前、Pony score 词、其余删、禁统一 8k/RAW） | C | 「（研究 §3）」 |
| SKILL.md:29 | 硬闸：风格污染——写实照片/西方卡通/厚涂油画入负面封堵 | G | 无（「厚涂油画」词效无任何出处） |
| style-profile.md:3 | 文件级依据声明：研究 §4-2、§3 + style-library §二 | C | 「依据：…」 |
| style-profile.md:7 | 风格定位：干净线稿+赛璐璐平涂，吉卜力味可选变体 | C | 文件头依据 |
| style-profile.md:13 | 词组：动漫插画 / anime illustration | C | 依据头（研究 §4-2 组合） |
| style-profile.md:14 | 词组：高对比活力色彩 / vibrant colors | C | 同上 |
| style-profile.md:15 | 词组：赛璐璐平涂 / cel shaded | C | 同上 |
| style-profile.md:16 | 词组：干净线稿 / clean line art | C | 同上 |
| style-profile.md:17 | 词组：日系二次元非写实 | C | 同上 |
| style-profile.md:18 | 吉卜力变体：田园/柔和水彩背景 | C | 研究 §4-2（smartaiedits） |
| style-profile.md:19 | MJ Niji 模式 --niji 二次元优化通道 | C | 研究 §4-2 |
| style-profile.md:20 | SD Danbooru 标签体（1girl/1boy, solo…） | C | 研究 §4-2（Promgrammer） |
| style-profile.md:25 | 风格锁模板（中文版） | C | 依据头（自组自 §4-2 词表） |
| style-profile.md:28 | 风格锁模板（英文版） | C | 同上 |
| style-profile.md:32 | 光影偏好：平涂分层光影、禁糊阴影 | G | 无 |
| style-profile.md:36 | 画质词分平台全规则（≤3 放最前、NovelAI 空格/Animagine 下划线、Pony score_9/score_8_up、MJ --style raw、禁统一 8k/RAW） | C | 「（研究 §3）」「（Promgrammer）」 |
| style-profile.md:37 | 禁写实词黑名单（photorealistic/写实皮肤/85mm/DSLR） | C | 「（研究 §7 修正 1）」 |
| style-profile.md:38 | 负面词通道分流（SD 5–15 词、MJ --no 3–5 词、Flux/GPT/即梦正向改写） | C | 「（研究 §3）」 |
| style-profile.md:38 | 子项：即梦无负面框 | G | 「【即梦无负面框·推测】」 |
| style-profile.md:39 | 负面词纪律：针对性 10 词>通用 50 词、正向词不入负面、只能去缺不能补缺 | G | 「（style-library §二）」——**引用错位**，该节无此文；「10 词>50 词」在研究 §3 也不存在（研究写的是 SDXL 5–15、MJ 3–5） |
| style-profile.md:45 | 翻车对策：手部崩坏→extra fingers/bad anatomy 或手部 LoRA | C | 表头「翻车点（研究 §4-2）」 |
| style-profile.md:46 | 翻车对策：文字乱码→不写字/引号写明内容 | C | 「（研究 §4-4 同策）」 |
| style-profile.md:47 | 翻车对策：混写实词→黑名单扫描+负面封堵 | C | 表头研究 §4-2 |
| style-profile.md:48 | 翻车对策：Pony 系 masterpiece 无效→score 体系 | C | 「（Promgrammer）」 |
| style-profile.md:49 | 翻车对策：角色漂移→固定特征短语+三视图+即梦引用主体 | G | 「（style-library §二）」——**引用错位**；内容实际可溯源研究①（Arcloop），挂错了文档 |
| style-profile.md:50 | 翻车对策：画风漂移→风格段每图同源复制、一剧一风格 | C | 表头研究 §4-2 |

### style-cg-refined

| 条目 | 摘要 | 级 | 原标注文字 |
|------|------|----|-----------|
| SKILL.md:8 | 风格定位「设计可假、光和材质必须真」+「2026-10-27 应用户要求由 3D 卡通 cel-shading 升级，取代主风格位」 | U | 「应用户要求…（2026-10-27）」 |
| SKILL.md:12 | 套件默认主风格 | U | 同上语境 |
| SKILL.md:26 | 硬闸：禁游戏 CG 感/塑料皮肤，皮肤写真实纹理、材质写具体 | U | 用户案例规格（style-profile.md:3 头声明） |
| SKILL.md:27 | 硬闸：禁 cel 系词混入（赛璐璐/粗描边/色块平涂/扁平） | G | 无（风格划界为编辑撰写） |
| SKILL.md:28 | 硬闸：相机词是合法武器（IMAX/Panavision/焦段光圈/胶片型号/动态模糊） | U | 用户 2026-10-27 案例含 IMAX+Panavision C 系列 |
| SKILL.md:29 | 硬闸：光影写实、曝光规则（高光不过曝/暗部留细节/过渡自然）逐镜复制 | U | 用户案例规格 |
| style-profile.md:3 | 规格来源声明：用户 2026-10-27 参考级出视频指令（原子朋克机器人案例）=验收标尺 | U | 「用户 2026-10-27」 |
| style-profile.md:7 | 观感目标 Photorealism，杜绝游戏 CG/塑料皮肤/动作僵硬 | U | 头声明 |
| style-profile.md:11 | 词组·质感基座（半写实精致 CG/电影级/超写实/真实材质） | U | 头声明 |
| style-profile.md:12 | 词组·材质武器（哑光皮革/磨砂金属/织物纹理/细腻皮肤纹理） | U | 头声明（案例词） |
| style-profile.md:13 | 词组·镜头武器（IMAX/Panavision C 系列/变形宽荧幕/长焦/浅景深/动态模糊） | U | 头声明（案例词） |
| style-profile.md:18 | 风格锁模板（中文，含胶片颗粒/低饱和/自然日光/曝光规则） | U | 头声明 |
| style-profile.md:21 | 风格锁模板（英文） | U | 头声明 |
| style-profile.md:25 | 双高对比色调写死全剧（参考案例：复古暖橙+海盐蓝） | U | 「参考案例」 |
| style-profile.md:26 | 胶片颗粒质感+低饱和度胶片滤镜 | U | 头声明 |
| style-profile.md:27 | 曝光规则三条 | U | 头声明 |
| style-profile.md:28 | 光影四件套（光源位置+类型+色温+时段）逐镜复制 | U | 头声明（「四件套」框架用语为套件概念，见研究 ⑦-10） |
| style-profile.md:34 | 翻车对策：游戏 CG 感→材质词入正文+写曝光规则逼真实光比 | S | 「翻车案例与实战校准：沉淀到本表，标日期来源」——现存条目均无日期来源 |
| style-profile.md:35 | 翻车对策：卡通词混入→cel 黑名单 | S | 同上 |
| style-profile.md:36 | 翻车对策：画质词堆砌→换具体材质词+相机词 | S | 同上（与研究 §3「真有用的替代」同向，未挂） |
| style-profile.md:37 | 翻车对策：动作僵硬→逐拍写动词（掏→按→抛→压帽→耸肩）、运镜写速度 | S | 同上（动词序列取自用户案例动作） |
| style-profile.md:38 | 翻车对策：光影乱→四件套+色调对撞组逐镜复制 | S | 同上 |
| style-profile.md:39 | 翻车对策：参考与描述脱节→@资产引用跟完整文字描述 | S | 「（见 video-producer 规则）」——内部交叉引用，非外部来源 |

### style-comic（零外部标注）

| 条目 | 摘要 | 级 | 原标注文字 |
|------|------|----|-----------|
| SKILL.md:3 | 风格要素：动态分镜/粗黑轮廓线/速度线/网点/高饱和平涂/夸张表情 | G | 无 |
| SKILL.md:6 | 硬要求：与写实类互斥，负面词必带 3D, realistic, photo | G | 无（全后端一刀切，与 shared/backends.md 负面通道分流直接冲突） |
| style-profile.md:2 | 核心视觉要素六件 | G | 无 |
| style-profile.md:3 | 英文关键词库（comic book style/manga/speed lines/halftone dots/bold ink outlines…） | G | 无 |
| style-profile.md:4 | 指令模板（主体+动作+comic book style…+画质参数） | G | 无 |
| style-profile.md:5 | 示例（young warrior… --ar 3:4 --niji 6） | G | 无（--niji 6 版本钉死无出处） |
| style-profile.md:6 | 负面词 3D/realistic/photo/lowres/text/watermark + 「MJ 用 --niji 6」 | G | 无 |

### style-cyberpunk

| 条目 | 摘要 | 级 | 原标注文字 |
|------|------|----|-----------|
| SKILL.md:18 | 先定子类（霓虹城市全景/暗黑赛博/复古赛博/轻科幻） | G | 无（研究 §4-4 有此子类，本处未挂） |
| SKILL.md:21 | 硬要求：光影四件套必写进场景段 | G | 无（研究 §2 有此法，本处未挂） |
| SKILL.md:26 | 头号红线：neon/霓虹/赛博光源只进本风格段，误加即毁图 | C | 「（研究 §4-4）」 |
| SKILL.md:27 | 硬闸：禁知名角色名——点名禁「银翼杀手等影片/角色专有名」 | G | 无（**被本 skill L60「Blade Runner style」自相违反**） |
| SKILL.md:28 | 硬闸：画质词按后端分流，换具体材质词（湿漉沥青/铬金属/全息贴膜） | C | 「（研究 §3）」 |
| SKILL.md:29 | 硬闸：人脸受光硬条件（face clearly lit, rim light on face）防光污染盖脸 | G | 无 |
| style-profile.md:7 | 风格定位：high-tech low-life、青-洋红+体积雾夜景 | C | 文件头「依据：研究 §4-4、§3、§2」 |
| style-profile.md:13–22 | 高效组合表 10 行（cyberpunk/neon-lit megacity/rain-slick streets/holographic ads/neon signs/high-tech low-life/teal-magenta/volumetric fog/night cinematic/4 子类） | C×10 | 依据头（研究 §4-4，NavXD 提示词库、原创力） |
| style-profile.md:27 | 风格锁模板（中文，含光源布局占位） | C | 依据头 |
| style-profile.md:30 | 风格锁模板（英文） | C | 依据头 |
| style-profile.md:34 | 光影/运镜偏好：光源四件套必写逐镜复制 | C | 「（研究 §2 光影统一法）」 |
| style-profile.md:38 | 画质词基本全删，换具体材质词（湿漉沥青反光/铬金属/霓虹玻璃管/全息贴膜） | C | 「（研究 §3）」 |
| style-profile.md:39 | 负面词通道分流（SD 5–15 词用途=物体清除+顽固缺陷、MJ --no 3–5、正向改写） | C | 「（研究 §3）」 |
| style-profile.md:38 | 子项：即梦无负面框 | G | 「【即梦无负面框·推测】」 |
| style-profile.md:40 | 文字处理：Flux 引号写明内容+位置+字体（"bold industrial lettering"）+hex 色号 | O | 「研究 §3 Flux 特性」→ BFL 官方 prompting guide |
| style-profile.md:46 | 翻车对策：霓虹乱入→只进本风格段 | C | 表头「翻车点（研究 §4-4）」 |
| style-profile.md:47 | 翻车对策：只堆 neon 不写光源布局→四件套写全 | C | 「（研究 §2）」 |
| style-profile.md:48 | 翻车对策：中文霓虹招牌乱码→引号写明/纯色块 | C | 表头研究 §4-4 |
| style-profile.md:49 | 翻车对策：光污染盖脸→显式 face clearly lit, rim light on face | C | 表头研究 §4-4（研究内该条本身无外部出处） |
| style-profile.md:60 | 朋克家族·赛博朋克词表（cyberpunk…Blade Runner style；负面 bright sunshine, nature） | U | 「（2026-10-30 用户方案）」 |
| style-profile.md:61 | 朋克家族·蒸汽朋克词表（steampunk/brass/gears/Victorian…） | U | 同上 |
| style-profile.md:62 | 朋克家族·柴油朋克词表（dieselpunk/retro-futurism/art deco…） | U | 同上 |
| style-profile.md:63 | 参数：--stylize 250–750 增强艺术感 | U | 同段（数值建议疑似粘贴，见疑似杜撰清单） |

### style-fantasy（零外部标注）

| 条目 | 摘要 | 级 | 原标注文字 |
|------|------|----|-----------|
| SKILL.md:6 | 适用 D&D/龙与地下城系、骑士法师精灵、黑暗奇幻；与现代都市系互斥 | G | 无（D&D 为注册商标/IP 名，与全套件禁 IP 闸冲突） |
| style-profile.md:2 | 核心视觉要素：中世纪城堡/骑士法师精灵/魔法光效/羊皮纸/史诗构图/繁复盔甲 | G | 无 |
| style-profile.md:3 | 英文关键词库（western fantasy/oil painting/dark fantasy/**dungeons and dragons style**/**Greg Rutkowski（画师风增强）**） | G | 无（两处 IP/画师名，见疑似杜撰清单） |
| style-profile.md:4 | 指令模板（种族职业+服装武器+western fantasy…+画质参数） | G | 无 |
| style-profile.md:5 | 示例（elven ranger… --ar 16:9 --v 6.0） | G | 无 |
| style-profile.md:6 | 负面词 modern/sci-fi/lowres/text + 「MJ 用 --v 6.0」 | G | 无 |

### style-infinite-flow（零外部标注）

| 条目 | 摘要 | 级 | 原标注文字 |
|------|------|----|-----------|
| SKILL.md:6a | 适用副本/生存游戏/系统流/多重世界 | G | 无 |
| SKILL.md:6b | 硬要求：惊悚词按 lessons 中性化词表降浓度 | S | 指向 `shared/lessons.md`「微恐/惊悚描述的平台审核规避（2026-10-28 xyq 倒吊影被拦实测）」——内部实测日志 |
| style-profile.md:2 | 核心视觉要素：空间撕裂/多重世界/神秘大门/数据代码/系统 UI/诡异氛围 | G | 无 |
| style-profile.md:3 | 英文关键词库（infinite flow/dimensional rift/glitch art/system UI overlay…） | G | 无 |
| style-profile.md:4 | 指令模板（主角+空间异常+infinite flow…+画质参数） | G | 无 |
| style-profile.md:5 | 示例（巨门前混合赛博城市+中世纪城堡… --ar 16:9） | G | 无 |
| style-profile.md:6 | 负面词 normal street/sunny day/lowres/text + 「MJ 可提 --stylize 250–750」 | G | 无（与 cyberpunk L63 同款数值，见疑似杜撰清单） |

### style-photoreal

| 条目 | 摘要 | 级 | 原标注文字 |
|------|------|----|-----------|
| SKILL.md:18 | 先定调性四分支（商业精致/80s 复古/2000s 卡片机/纪实粗糙） | G | 无（80s/2000s 分支源自 BFL 风格参考表，本处未挂） |
| SKILL.md:26 | 硬闸：禁卡通/动画词混入（cel-shaded/cartoon/animated/Pixar） | G | 无（研究 §3 负面三用途「媒介锁」同向，未挂） |
| SKILL.md:27 | 硬闸：禁真实明星/公众人物名与受保护形象 | G | 无 |
| SKILL.md:28 | 硬闸：quality soup 全禁，SDXL 上 masterpiece 拉向绘画 | C | 「（研究 §3/§4-5）」 |
| SKILL.md:29 | 硬闸：霓虹赛博光、皮克斯圆润比例不进本风格段 | G | 无 |
| style-profile.md:7 | 风格定位：机型+镜头+光圈+胶片/调色四件套为核心 | O | 文件头「依据：研究 §4-5、§3（BFL 官方 + imagetoprompt）」 |
| style-profile.md:13 | 词组：photorealistic portrait of [主体] | O | 依据头（BFL 官方组合） |
| style-profile.md:14 | 词组：shot on Canon EOS R5, 85mm f/1.4（机型+镜头+光圈） | O | 同上 |
| style-profile.md:15 | 词组：shallow depth of field, bokeh | O | 同上 |
| style-profile.md:16 | 词组：golden hour window light | O | 同上 |
| style-profile.md:17 | 词组：natural skin texture | O | 同上 |
| style-profile.md:18 | 词组：slight film grain | O | 同上 |
| style-profile.md:19 | 词组：Kodak Portra 400 调色 | O | 同上 |
| style-profile.md:20 | 词组：80s 复古（film grain/warm color cast/soft focus） | O | 「BFL 风格参考表」（研究 §4-5） |
| style-profile.md:21 | 词组：2000s 卡片机（early digital camera/flash/candid） | O | 同上 |
| style-profile.md:22 | 词组：纪实粗糙（documentary photography + --style raw） | C | imagetoprompt（研究 §4-5） |
| style-profile.md:27 | 风格锁模板（中文，四件套+光源四件套占位） | O | 依据头（BFL 组合自组） |
| style-profile.md:30 | 风格锁模板（英文） | O | 同上 |
| style-profile.md:34 | 光影/运镜偏好：光圈控景深（f/1.4 虚化、f/8 全清晰） | G | 无（摄影常识，无标注） |
| style-profile.md:38 | quality soup 全删；BFL：写具体机型胶片比 "professional photo" 强得多 | O | 「（BFL…）」「（研究 §3/§4-5）」 |
| style-profile.md:39 | 负面词通道分流（SD 5–15 词含 plastic skin 等、MJ --no 3–5、正向改写） | C | 「（研究 §3）」 |
| style-profile.md:38 | 子项：即梦无负面框 | G | 「【即梦无负面框·推测】」 |
| style-profile.md:40 | 手部/皮肤专项：负面 plastic skin / 正向 detailed skin texture | C | 「（研究 §4-5）」 |
| style-profile.md:46 | 翻车对策：masterpiece 拉向绘画→删质量词换相机四件套 | C | 表头「翻车点（研究 §4-5）」 |
| style-profile.md:47 | 翻车对策：quality soup 无益带 AI 味→清零 | C | 表头（oreateai《The Failure of Quality Soup》，研究 §4-5） |
| style-profile.md:48 | 翻车对策：手部崩坏/皮肤塑料感→负面+正向词 | C | 表头研究 §4-5 |
| style-profile.md:49 | 翻车对策：MJ 过度精美→--style raw + documentary photography | C | 「（imagetoprompt）」 |
| style-profile.md:50 | 翻车对策：卡通词反向污染→黑名单扫描 | C | 表头研究 §4-5 |

### style-pixar

| 条目 | 摘要 | 级 | 原标注文字 |
|------|------|----|-----------|
| SKILL.md:8 | 核心四件套：圆润比例+夸张表情+SSS 材质+电影级布光 | G | 无（研究 §4-3 有此四件套，本处未挂） |
| SKILL.md:19 | 表情词写具体情绪（curious/joyful）不写只 cute | G | 无（gptimage2.hk 对照表结论在研究 §4-3，未挂） |
| SKILL.md:21 | 硬要求：一图一变量，不一次改表情+服装+场景 | G | 无（研究 ⑦-9 有此原则，未挂） |
| SKILL.md:26 | 硬闸：禁写实词（photorealistic/skin pores/85mm/DSLR）冲掉动画感 | C | 「（研究 §7 修正 1）」 |
| SKILL.md:27 | 硬闸：禁皮克斯/迪士尼具体角色名与 IP 名 | C | 「（研究 §4-3 版权避坑）」 |
| SKILL.md:28 | 硬闸：画质词全平台删（masterpiece 拉向画廊绘画） | C | 「（研究 §3）」 |
| SKILL.md:29 | 硬闸：赛博霓虹、写实电商产品图质感不进本风格段 | G | 无 |
| style-profile.md:7 | 风格定位：四件套（研究 §4-3） | C | 「（研究 §4-3）」 |
| style-profile.md:13–21 | 高效组合表 9 行（3D Pixar-style look/头大颊柔剪影可读/大眼虹膜高光/SSS 皮肤/风格化发束/三点布光/AO/动画剧照/具体表情词） | C×9 | 依据头「研究 §4-3、§3 + style-library §三」（组合出处：可灵官方教程·抖音、gptimage2.hk） |
| style-profile.md:26 | 风格锁模板（中文） | C | 依据头 |
| style-profile.md:29 | 风格锁模板（英文） | C | 依据头 |
| style-profile.md:33 | 光影偏好：三点布光为基调 | C | 复用组合表 C 级词 |
| style-profile.md:37 | 画质词全平台删，换 SSS/材质/布光词 | C | 「（研究 §3）」 |
| style-profile.md:38 | 禁写实词黑名单 | C | 「（研究 §7 修正 1）」 |
| style-profile.md:39 | 负面词通道分流（SD 5–15 词、MJ --no 3–5、正向改写） | C | 「（研究 §3）」 |
| style-profile.md:38 | 子项：即梦无负面框 | G | 「【即梦无负面框·推测】」 |
| style-profile.md:45 | 翻车对策：只写 Pixar style cute→贴纸脸，四件套+明确表情词 | C | 表头「翻车点（研究 §4-3）」 |
| style-profile.md:46 | 翻车对策：多变量齐改→一图一变量 | C | 表头研究 §4-3 |
| style-profile.md:47 | 翻车对策：写实关键词冲掉动画感→黑名单+负面封堵 | C | 表头研究 §4-3 |
| style-profile.md:48 | 翻车对策：写实产品图套皮克斯风→产品卡通化，产品图不走本风格 | C | 表头研究 §4-3（研究内该条本身无外部出处） |
| style-profile.md:50 | 翻车对策：塑料假人/恐怖谷→眼神写有神、逐图查皮肤/眼睛/发量三件套 | G | 「（style-library §三）」——**引用错位**，该节是沉淀路由，无此文 |
| style-profile.md:51 | 翻车对策：MJ 快捷通道 --sref 3687830488 --v 7 开 3D 卡通风格门 | G | 「【推测：风格码效果随版本波动】」（研究 §4-3 记有 aimindwork 博客出处，但显式标推测） |

---

## 缺口清单

### A. G 级全部条目（63 条，按主题归组；条目定位见上表）

**A1. style-3d-anime 全文件零外部标注（18 G + 5 S，共 23 条）**——本 skill 2026-10-28 建档后无一条回写过来源，尽管 SKILL.md:36 自己规定「调研/实战发现回写翻车点表，标日期与来源」：
1. SKILL.md:8 风格定位「日漫的脸 3D 的质感」与观感目标——定位断言无出处
2. SKILL.md:13 「米哈游风」触发词——IP 名做质感参照，与自身 L29 禁令矛盾
3. SKILL.md:18 一剧一风格硬要求（套件通用纪律，全库均无用户令出处）
4. SKILL.md:21 脸/材质双组词缺一必漂——机理断言无出处
5. SKILL.md:26 禁写实词硬闸——与研究 §7 修正 1 同向但未挂（可一日补齐）
6. SKILL.md:27 禁 2D 平涂词硬闸——边界规则无出处
7. SKILL.md:28 双锚同时在场硬闸——机理断言无出处
8. SKILL.md:29 禁 IP 名硬闸——研究 §4-3 有同款，未挂
9. style-profile.md:8/14 中英风格锁模板——整段模板词无任何词效来源
10. style-profile.md:21–25 高效组合 5 组词库——词效（大眼睛/次表面散射/发丝分明/体积光等）无出处
11. style-profile.md:31–33 边界词表 3 行——「混入后果」（恐怖谷/压平/崩坏）为断言无出处
12. style-profile.md:39–43 翻车对策 5 行（S 级）——「大眼睛词被忽略」「发丝糊成片状」等为无日期无来源的经验口吻

**A2. style-comic 全文件（7 G）**：
13. SKILL.md:3 风格六要素——词库无出处
14. SKILL.md:6 「负面词必带 3D, realistic, photo」——全后端一刀切，与 shared/backends.md「MJ --no 3–5 词、Flux/即梦无负面通道」的分流规则直接冲突
15. style-profile.md:2 核心视觉要素
16. style-profile.md:3 英文关键词库（comic book/halftone/speed lines 等词效无任何实证）
17. style-profile.md:4 指令模板
18. style-profile.md:5 示例（--niji 6 版本钉死）
19. style-profile.md:6 负面词表 + MJ --niji 6

**A3. style-fantasy 全文件（6 G）**：
20. SKILL.md:6 适用 D&D/龙与地下城系——商标 IP 名入适用范围
21. style-profile.md:2 核心视觉要素
22. style-profile.md:3 英文关键词库（含 dungeons and dragons style、Greg Rutkowski）
23. style-profile.md:4 指令模板
24. style-profile.md:5 示例（--v 6.0 版本钉死）
25. style-profile.md:6 负面词表

**A4. style-infinite-flow 主体（6 G）**：
26. SKILL.md:6a 适用范围
27. style-profile.md:2 核心视觉要素（glitch art/system UI overlay 词效全无实证）
28. style-profile.md:3 英文关键词库
29. style-profile.md:4 指令模板
30. style-profile.md:5 示例
31. style-profile.md:6 负面词表 + --stylize 250–750

**A5. 引用错位（3 条，标注存在但指向错误文档）**：
32. style-anime/style-profile.md:39 「负面词纪律（style-library §二）」——style-library §二无此内容；「10 词>50 词」「只能去缺不能补缺」在被引研究 §3 中也不存在
33. style-anime/style-profile.md:49 「角色漂移（style-library §二）」——同上；内容实际在研究①（Arcloop）
34. style-pixar/style-profile.md:50 「塑料假人（style-library §三）」——style-library §三是沉淀路由，无验收清单

**A6. 显式【推测】条目（4 条，均属一查便知的平台事实）**：
35. style-anime/style-profile.md:38 即梦无负面框【推测】
36. style-cyberpunk/style-profile.md:39 即梦无负面框【推测】
37. style-photoreal/style-profile.md:39 即梦无负面框【推测】
38. style-pixar/style-profile.md:39 即梦无负面框【推测】
39. （附）style-pixar/style-profile.md:51 --sref 风格码【推测】——有 aimindwork 出处但效果断言未实测

**A7. 零散未挂来源（硬闸/词效，内容在他处有 C 级出处）**：
40. style-anime/SKILL.md:27 禁知名角色名（研究 §4-3 有）
41. style-anime/SKILL.md:29 「厚涂油画/西方卡通」负面项——词效无实证
42. style-anime/style-profile.md:32 「禁糊阴影」光影偏好
43. style-cg-refined/SKILL.md:27 cel 系词禁入（划界编辑撰写）
44. style-cyberpunk/SKILL.md:18 四子类（研究 §4-4 有）
45. style-cyberpunk/SKILL.md:21 光影四件套必写（研究 §2 有）
46. style-cyberpunk/SKILL.md:27 禁银翼杀手专有名（且被 L60 自反）
47. style-cyberpunk/SKILL.md:29 人脸受光硬条件
48. style-photoreal/SKILL.md:18 调性四分支（BFL 风格参考表有）
49. style-photoreal/SKILL.md:26 禁卡通词（研究 §3 媒介锁同向）
50. style-photoreal/SKILL.md:27 禁明星名
51. style-photoreal/SKILL.md:29 霓虹/皮克斯不进
52. style-photoreal/style-profile.md:34 光圈-景深偏好（摄影常识无标注）
53. style-pixar/SKILL.md:8 四件套定位（研究 §4-3 有）
54. style-pixar/SKILL.md:19 具体表情词（gptimage2.hk 对照表有）
55. style-pixar/SKILL.md:21 一图一变量（研究 ⑦-9 有）
56. style-pixar/SKILL.md:29 产品图/霓虹不进
57. style-anime/SKILL.md:18 / style-3d-anime/SKILL.md:18 一剧一风格（全库共 8 处复述，均无用户令/外部出处——若这是用户口径，应统一补「用户令+日期」）

### B. S 级主题缺口（外部词效资料明显存在但我们没查过）

1. **大眼睛/眼比例词效**（3d-anime 翻车「大眼睛词被忽略」）——Booru tag 词效对照、NovelAI/Animagine 词效指南、社区「anime eyes 写法」实证大量存在，未查
2. **发丝词效**（「发丝根根分明」「发丝糊成片状」）——SD/Booru 社区 hair strand/细发丝 vs 成束发 词效实测存在，未查
3. **次表面散射/材质词在生图模型的词效**（3d-anime、pixar 的 SSS 锚）——3D 渲染词在 SDXL/Flux/即梦是否真能拉出 SSS 质感无任何实证
4. **写实↔动漫边界词的社区实证**（3d-anime 边界词表 3 行的「混入后果」）——半写实恐怖谷、cel↔photoreal 互斥在社区（gptimage2.hk 之外）有大量对照实验，未查
5. **手部对策**（3d-anime 翻车「沿通用验收」）——bad hands 负面词效、手部 LoRA 横评资料极多，3d-anime 未挂研究 §4-2 已有内容
6. **曝光规则/光比断言**（cg-refined 翻车表）——摄影侧资料可查，未查
7. **动作逐拍写法对视频模型的词效**（cg-refined 翻车「动作僵硬」）——Seedance/即梦官方提示词指南对动作描写的建议可查，未查
8. **风格污染互斥矩阵**（comic「负面必带 3D, realistic, photo」、photoreal 反向禁卡通）——各风格负面词对其他风格的误伤效应（如 --no 3D 在即梦/MJ 的行为）无实证
9. **平台官方风格词建议**（comic/fantasy/infinite-flow 三个 skill 的整个词库）——Midjourney 官方 style 词条目、Niji 官方、即梦官方风格库均未查过，全部词表是裸关键词
10. **参数建议**（--niji 6 / --v 6.0 / --stylize 250–750）——官方参数文档一查便知，现状是版本钉死+疑似粘贴数值
11. **画师名词效与平台政策**（fantasy Greg Rutkowski）——社区与平台（MJ/SD）对画师名的政策与词效变化已有大量讨论，未查未更新
12. **微恐词的平台审核规则**（infinite-flow 引 lessons 中性化词表）——现依据仅一次 xyq 倒吊影实测（S 级），各平台公开审核规范可对照而未对照

---

## 疑似杜撰 / 包装过度清单

1. **style-fantasy/style-profile.md:3「Greg Rutkowski（画师风增强）」**——在世画师名当「增强词」是 2022 年 SD1.5 时代的社区梗写法；MJ v6 起已大幅弱化画师名、行业普遍视为版权风险，与全套件「禁知名 IP/角色名」精神直接冲突。像从过时英文提示词合集抄来，对不上任何本套件机制。
2. **style-fantasy/style-profile.md:3「dungeons and dragons style」**——注册商标/IP 名直接进「关键词库」，与 fantasy 自己不出镜但与其他 skill 的禁 IP 硬闸冲突；同款套路（抄 2023 年前后 fantasy prompt 合集）。
3. **style-cyberpunk/style-profile.md:60「Blade Runner style」**——**在同一文件内自相矛盾**：SKILL.md:27 明令「禁写银翼杀手等影片/角色专有名」，L60 的「用户方案」词表里却直接带着它。要么硬闸是摆设，要么该词表是从网传赛博朋克 prompt 清单粘贴进「用户方案」段落的（该清单典型组合恰好是 cyberpunk + Blade Runner style + 负面 bright sunshine/nature）。
4. **style-anime/style-profile.md:39「负面词纪律（style-library §二）：针对性 10 词>通用 50 词…负面只能去缺不能补缺」**——被引文档无此内容，被引研究的数值是 5–15 / 3–5，「10 词>50 词」「去缺不能补缺」两句话在全库找不到任何出处，措辞像自创教条。
5. **style-pixar/style-profile.md:50「逐图查皮肤/眼睛/发量三件套」**——引用错位到 style-library §三；「三件套」验收清单对不上任何真实机制或外部资料。
6. **style-anime/style-profile.md:49 挂错出处**——内容本身（锚点复述/三视图/引用主体）可溯源研究①，但挂到了不存在的章节，属杜撰式标注。
7. **「--stylize 250–750 增强艺术感」**（cyberpunk L63 + infinite-flow L63 两处同款）——MJ stylize 参数真实存在（0–1000），但「250–750」这个带区间的推荐像 blog 粘贴，且在 cyberpunk 处混进「2026-10-30 用户方案」段落里未与用户原话区分。
8. **style-3d-anime/style-profile.md:39–41 翻车机理断言**——「大眼睛词被忽略」「发丝糊成片状」以确定机理口吻写成对策，既无实测记录（lessons.md 无对应条目）也无外部来源，属未经验证的经验包装。
9. **版本钉死参数**（comic「MJ 用 --niji 6」、fantasy「MJ 用 --v 6.0」）——当前 MJ 主力是 v7 时代，把版本号写成硬参数且无出处，像 2024–2025 年的旧合集原文照搬。

---

## 系统性问题（供整改排序参考）

1. **四个 skill 零外部标注**：style-3d-anime、style-comic、style-fantasy、style-infinite-flow（合计 63 条里 61 条 G/S）。其中 style-3d-anime 是有完整模板/词表/翻车表的「重」skill，风险最高；comic/fantasy/infinite-flow 是 10-30 一天建成的 6 行壳，词库层等于裸关键词合集。
2. **style-library 被当成万能出处引用**：3 次引用全部错位——style-library 实际只是选择器/路由。凡需「负面词纪律」「塑料假人对策」这类内容应引研究 §3 或 lessons.md。
3. **「一剧一风格」「禁 IP 名」等全库性硬要求无用户令背书**：各 skill 复述 8+ 次，但 CLAUDE.md 与文档里找不到「用户令+日期」；若是用户口径应统一补标，若是套件约定应明示「套件约定」而非裸硬闸。
4. **四个【推测】项集中在同一个问题（即梦有无负面框）**：属低成本可查证的平台事实，查一次可消 4 个 G。
5. **skill 间纪律冲突**：comic 的「负面词必带 3D, realistic, photo」违反 shared/backends.md 分流；cyberpunk L60 违反自身 IP 禁令；fantasy/comic 的 IP 名/画师名违反全库禁 IP 闸。
