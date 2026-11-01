# 入库施工单：质检侧三档入库（2026-10-31）

> 施工员：intake-qa｜两阶段：先写施工单（本文件），再按单施工。
> 喂料：`2026-10-31-batch4-qa-post-audit.md`（主）+ `2026-10-31-batch1-video-official-supplement.md`（sd2-pe 兜底/标识）+ `2026-10-31-batch2-image-official.md`（watermark/URL 24h）。
> 目标文件：`skills/shot-qa/**`、`skills/clip-review/**`、`skills/video-producer/**`、`shared/hard-gates.md`、`shared/backends.md`、`shared/lighting-system.md`。**不动 storyboard-director/ 与 pacing 类文件**。
> 三档入库（用户已批）：**官方级直接入｜社区实证级带源入｜经验值标【经验·内部】**。
> 铁律：①每条必带来源标注 ②U 级用户令与用户供样例不动 ③禁编造报告外内容 ④被校正条目留注记 ⑤逐条日志（施工后回填本文件末尾）。

## 分档口径

| 档 | 判定 | 入法 |
|----|------|------|
| 官方级 | 法律法规/监管机构/平台官方规范/官方 API 文档/官方教程 | 直接入，标【官方】+ 出处 |
| 社区实证级 | 行业工具/学术论文/社区教程（有源可溯） | 带源入，标【行业/学术/社区】+ URL |
| 经验值 | 查无外部依据的内部启发式/配方/预算参数 | 数值保留，标【经验·内部】+ 注记（禁标行业标准） |

---

## 一、hard-gates.md（3 条）

| # | 条目 | 档 | 落点 | 动作 | 来源 |
|---|------|----|------|------|------|
| QA-01 | **《人工智能生成合成内容标识办法》法定义务**（2025-09-01 施行）：显式标识=视频**起始画面 + 播放周边**显著提示、导出/下载文件必含；隐式标识=文件元数据嵌生成属性/服务提供者/内容编号；发布**主动声明**+用标识功能，禁删除/篡改/伪造/隐匿标识；视频号 6.4 同款 | 官方（最高优先级） | hard-gates 新增「10. AI 生成内容标识闸」+ 零容忍清单补 1 行 + 执行顺序总览补「交付前标识检查」 | 新增 | 国信办通字〔2025〕2 号全文（xwb.neu.edu.cn/2025/0316/c9646a279035/pagem.htm 转载）；视频号规范 6.4 |
| QA-02 | **内容审核依据库**：细则(2021) 58/62/77/82/93/99、(九)37–40；视频号 5.2.5/5.5.1/5.8.1–5.8.3/5.13.1/5.11.4/5.14.2；快手第四章二（尸体/密集恐惧/自杀自残示例）。判定=**效果标准**（引发惊恐/焦虑/厌恶/恶心/不适，非词面）；扫描范围含**标题/话题/弹幕/字幕**（细则总则+5.5.1）；禁点词对账（骷髅/尸体/密集恐惧/自杀自残/枪击/刺伤/拷打/恐怖灵异）↔ 微恐中性化词表（lessons 微恐节）；空白注记（抖音公约全文抓取失败、外部现成词表不存在） | 官方 | hard-gates 新增「11. 内容审核依据与惊悚判定」（含对账注记） | 新增 | 央视网细则全文；weixin.qq.com 视频号规范；kuaishou.com/norm（批4 ③） |
| QA-03 | **广告合规补入广告植入闸（§6）**：《广告绝对化用语执法指南》（市监总局 2023-02-25）极限词红线（国家级/最高级/最佳及近似用语）+ **6 类豁免**情形 + 医疗医美/药品保健食品/招商投资/教育培训**从严**；广告可识别性（视频号 4.6.4）；禁违规产品植入（细则 99）；避真实商标仿冒（视频号 3.4/3.5、快手五-3） | 官方 | hard-gates §6 追加小节 | 追加 | jinchuan.gov.cn 执法指南全文；视频号 4.6.4/3.4/3.5；快手规范（批4 ⑥） |

## 二、shot-qa（3 条）

| # | 条目 | 档 | 落点 | 动作 | 来源 |
|---|------|----|------|------|------|
| QA-04 | **交付清单=AI 标识三义务检查**（显式/隐式/发布主动声明），出片验真后、交付/发布前必查，与 hard-gates §10 联动。注记：output-formats.md LOCKED 检查报告契约**不在本次施工范围**，交付清单以 shot-qa 侧新增段承载（登记，不动契约） | 官方（最高优先级） | shot-qa/SKILL.md 流程补「交付前检查」步 + 产出段补交付清单；three-gates.md 补「交付清单」模板段 | 新增 | 同 QA-01 |
| QA-05 | **违禁扫描范围与判定标准**：扫描范围=画面/台词/旁白/字幕/**标题/话题/弹幕**（细则总则+视频号 5.5.1 标题惊悚词同管）；惊悚/微恐用**效果标准**（细则 62：引发惊恐/焦虑/厌恶/恶心）；禁点词表须覆盖官方明文示例（对账指向 hard-gates §11） | 官方 | three-gates.md「违禁与细节下限」追加；shot-qa/SKILL.md 闸 2 条目 4 补注 | 追加 | 批4 ③3.1/3.2、⑦6 |
| QA-06 | **品牌检查补极限词与广告可识别性**：台词/字幕/贴片品牌宣传语禁极限词（执法指南红线+6 类豁免可引）；品牌露出须具广告可识别性（视频号 4.6.4） | 官方 | three-gates.md「品牌三层扫」追加一行 | 追加 | 批4 ⑥6.2 |

## 三、shot-qa trust-audit（1 条）

| # | 条目 | 档 | 落点 | 动作 | 来源 |
|---|------|----|------|------|------|
| QA-07 | **trust-audit 阈值全部改标**：叙事 35%/25%、相似度 65%/80%、≥3 处判 C——**数值保留**（`tools/trust_audit.py` 依赖），全部改标【经验·内部启发式·无行业依据】+ 注记行业对照（AI 视频 QC 通行形态=逐项 PASS/FAIL+时间码+Critical/Warning/Info 严重度计数升级，行业不用加权百分比阈值）。框架本身=2026-10-29 用户令（U 级）**不动** | 经验值（+行业对照注记） | shot-qa/references/trust-audit.md 表头注记块 | 改标+注记 | 批4 ①1.4/⑧1（阈值「戳穿」）；行业对照 framesense.io |

## 四、clip-review（4 条）

| # | 条目 | 档 | 落点 | 动作 | 来源 |
|---|------|----|------|------|------|
| QA-08 | **VBench 16 维命名对照**（CVPR 2024 Highlight）：subject identity inconsistency=主体一致性、motion smoothness=运动平滑、temporal flickering=时序闪烁、spatial relationship=空间关系 ↔ 现五项核验映射（②↔主体一致性、④↔运动平滑、①⑤↔空间关系），**时序闪烁为现清单覆盖缺口**→并入 QA-09 硬伤扫描补位 | 社区实证级（学术） | clip-review/references/checklist.md 新增「质量维度命名对照」小节 | 新增 | vchitect.github.io/VBench-project/（批4 ①1.2） |
| QA-09 | **成片硬伤最低覆盖**：黑帧、定帧（stuck media）、静音/爆音、响度/峰值、规格（分辨率/帧率/容器）、字幕文案错（错别字/语法）、音画相关性——音画/口型一致性=**平台官方违规项**（视频号 5.11.4 配音与画面不相关）；5.14.2 官方低质缺陷清单（画质模糊/内容不完整/音画不相关/重复/过度剪裁/上下颠倒/黑边/扭曲花屏）一并入列 | 社区实证级（行业）+官方 | clip-review/references/checklist.md 新增「成片硬伤扫描（最低覆盖）」小节 | 新增 | framesense.io（批4 ①1.1）；视频号 5.14.2/5.11.4 |
| QA-10 | **核验报告格式升级**：逐项 PASS/FAIL + **时间码** + **严重度（Critical/Warning/Info）**三件套，**禁止只给加权总分** | 社区实证级（行业） | clip-review/references/checklist.md 核验报告格式行扩写 + SKILL.md 流程注记 | 改写 | framesense.io（批4 ⑦1） |
| QA-11 | **C 类换占位（第三波①，已获批）**：checklist.md 报告格式示例「✗道具乙形态漂」= 剧内实证词，换占位（示例占位），**原文留档**（见执行日志）。仅动示例词，不动格式结构 | 专项清洗 | clip-review/references/checklist.md 核验报告格式行 | 换占位 | 第三波附加令；lessons「剧内数据勿入 skill」2026-10-31 纪律 |

## 五、video-producer（5 条）

| # | 条目 | 档 | 落点 | 动作 | 来源 |
|---|------|----|------|------|------|
| QA-12 | **口型策略补即梦对口型约束**：清晰正脸（真人/动漫图或视频均可）；三种模式——大师/快速仅图片输入**成片 ≤15s**、基础仅视频输入**≤36s**；音频走「上传音频」或「文案 ≤120 字即梦 TTS 合成」；积分随音频时长/文字量计。工具层依据：主流 TTS 文本→音频单向生成（火山豆包语音官方文档），「先产音频反锁时长」自然成立；验收底线=视频号 5.11.4 官方违规项；空白注记：音素-视位对齐度量化验收无公开标准。**分镜切分/台词长度约束写法 →intake-direct** | 社区实证级（社区教程·工具行为）+官方红线 | video-producer/references/video-consistency.md §四 追加；SKILL.md 口型条目补注 | 追加 | it.sohu.com/907806985_120142897（三郎教程，批4 ④4.2）；volcengine.com/docs/6561/1594356（官方）；视频号 5.11.4 |
| QA-13 | **sd2-pe 强制兜底包入库**：画质包（高清，细节丰富，电影质感，色彩自然，光影柔和）+ 稳定包（人物面部稳定不变形、五官清晰、动作连贯自然，不僵硬，无穿模无卡顿）+ 字幕兜底 + 水印/Logo 兜底——每次输出必挂；多人场景加双胞胎兜底、动漫场景加风格锚定、多人正面动态加强方位约束；**眼睛发光兜底**（强烈情绪词触发瞳孔发光→最高优先级写「人物为正常人眼、不发光」，2.5 指南 FAQ+BytePlus） | 官方级 | video-producer/references/video-consistency.md §二 新增「官方兜底包」块 | 新增 | 火山 sd2-pe SKILL.md（arkdocs.tos-cn-beijing.volces.com/files/video-generation/SKILL.md）；批1 ⑤5/⑤10 |
| QA-14 | **30% 重生成余量改标**：数值保留（预算口径），标【经验·内部：AI 视频重生成失败率无公开统计，批4 核验】。落点四处：video-producer/SKILL.md 步骤 4、video-consistency.md §五、production-workflow.md §六路线表、backends.md 计价块 | 经验值 | 上述四处 | 改标+注记 | 批4 ②2.3/⑧3 |
| QA-15 | **0.8–1.5 倍缩放改标**：标【经验·内部：批4 核验查无行业标准/教程给出该区间】。同句「单镜 2–4s」=**镜长参数 →intake-direct（登记，本单不动）** | 经验值 | video-producer/SKILL.md 步骤 5（静态漫剧模式句内仅注缩放参数） | 改标+注记 | 批4 ②2.3/⑧2 |
| QA-16 | **卡点/定格参数注记**：名条停留 0.8–1.5 秒、卡点同步等量化参数=**U 级用户定值（2026-10-28 用户定）不动**，文件头补注【经验·内部：卡点剪辑属社区教程生态实践，无量化权威资料，批4 核验】——只加注记，不改任何用户定内容 | 经验值（注记级） | video-producer/references/first-appearance-nametag.md 文头注记 | 加注记 | 批4 ②2.3/⑧4；铁律② |

## 六、shared/backends.md（3 条）

| # | 条目 | 档 | 落点 | 动作 | 来源 |
|---|------|----|------|------|------|
| QA-17 | **Dreamina Web 时长能力补遗**：Seedance 2.5 单次最长 30s；**extended generation 5–180s**；**Multiframes ≤10 参考帧、每段 0–8s** | 官方级 | backends.md 即梦计价/能力块追加一行 | 追加 | dreamina.capcut.com/seedance/how-to-use-seedance-2-5（官方教程，批1 ③/④） |
| QA-18 | **volcengine 图片 API 素材侧两条**：`watermark` 默认 **true**（右下角「AI 生成」水印）→ 出图素材显式传 **false**；`response_format=url` 下载链接 **24h 失效** → 生成后立即转存入库。注记：素材关水印≠成品免标识——发布成品的显式标识义务见 hard-gates §10 | 官方级 | backends.md 即梦行/计价块追加 | 追加 | volcengine 图片生成 API 文档（批2 H2/H3） |
| QA-19 | **《实测项目A》口径换归属注记（第三波②，已获批）**：剧名改「计费实测口径（实测项目口径，2026-10-29）」，**全部数字保留**（实测来源禁删），**原文留档**（见执行日志） | 专项清洗（S 级实测） | backends.md 计价块 | 换注记 | 第三波附加令；铁律②延伸（剧内数据勿入 skill） |

## 七、shared/lighting-system.md（2 条）

| # | 条目 | 档 | 落点 | 动作 | 来源 |
|---|------|----|------|------|------|
| QA-20 | **色温物理锚注记**：烛光 ~1500K、日出/日落 3200K（=钨丝灯规格）、自然日光 5500K（灯具行业通称 5600K）、蓝天 12000K；K 值越高越冷、越低越暖；WB 设定值以上偏冷、以下偏暖；暖=温暖/冷=疏冷的情绪关联=**行业惯例非标准**；钨丝 3200K/日光 5600K 双色温=影视灯具行业规格 | 社区实证级（行业） | lighting-system.md 配方表前新增「色温物理锚」注记块 | 新增 | studiobinder.com/blog/what-is-color-temperature-definition/（批4 ⑤5.1） |
| QA-21 | **六配方数值改标**：各档色温区间=物理锚有据（3200–4200K 暖区间锚成立、5500/5600K 可写、冷区间标「行业惯例」），**情绪用途=行业惯例非标准**；「暗部占比 <15%」「60% 以上暗部」等百分比=【经验·内部·风格配方值，可调，无行业标准】；整表注「配方=起点不是枷锁」（已有使用规则 3）+【经验·内部】批注 | 经验值（+行业锚注记） | lighting-system.md 六配方表头注记 + 两处百分比行内注记 | 改标+注记 | 批4 ⑤5.2/⑧5 |

## 八、→intake-direct / 裁定项（team-lead 2026-10-31 三项裁决后处置）

| # | 条目 | 去向 | 处置结论 |
|---|------|------|------|
| G-1 | 「单镜 2–4s」标经验区间（ASL 社区口径 3–5s、快节奏 2–3s；学术方法论 UChicago Cinemetrics/Barry Salt/Cutting） | **关单（已覆盖）** | 已被 intake-direct 镜长定案覆盖（`skills/storyboard-director/references/shot-timing.md` 文件头定案 + `selfcheck-7` + `pacing-templates` 同步校正），不再转手 |
| G-2 | 即梦对口型 15s/36s/120 字上限影响分镜切分与台词长度约束的写法 | **已执行（team-lead 指定动手项）** | shot-timing.md 音画对齐段补一行交叉引用（口型/音频约束→video-consistency，标【社区教程·工具行为】） |
| G-3 | sd2-pe 引用语法/Asset ID 屏蔽/素材指代编号/任务句式防误判（提示词结构侧） | **关单（已覆盖）** | 已被 `storyboard-director/references/prompt-format.md` §十 sd2-pe 硬约束覆盖，不再转手 |
| G-4 | 单镜 5–10s 时长甜点（研究口径 RMD/误差累积） | **关单（已覆盖）** | 已被 shot-timing.md 三·附「时长-质量机制」+ backends Dreamina 段落地，不再转手 |
| G-5 | clip-review 归因矩阵实证列（「道具乙三变事故」「镜1 首版事故」「长发女相事故」「上午戏挂黄昏景」） | **已执行（team-lead 裁定）** | 实证列=B 类实测证据资产，**内容保留**；剧内标识换「实测项目」归属注记+补日期（2026-10-30 材料提炼），「道具乙」类道具词/事故关键词作真实事故锚保留；「镜1」镜位标识换归书注记（→「首版事故（实测项目镜位…）」）；无整体无标注冒充通用规则示例的条目，无需换占位。原文留档见执行日志 |

## 九、施工统计（施工后回填）

- 施工单条目数：21（QA-01～QA-21）+ 5 条 →intake-direct/登记项（G-1～G-5）
- 三档分布：官方级 9（QA-01/02/03/04/05/06/13/17/18）｜社区实证级带源 5（QA-08 学术、QA-09 行业+官方、QA-10 行业、QA-12 社区工具行为、QA-20 行业）｜经验值 5（QA-07/14/15/16/21）｜专项清洗 2（QA-11/19，第三波）

## 十、执行日志（施工后逐条回填）

| # | 落点 | 动作 | 结果 | 备注 |
|---|------|------|------|------|
| QA-01 | shared/hard-gates.md | 新增 §10 AI 标识闸（显式/隐式/主动声明三义务）+ 零容忍 1 行 + 执行顺序「→ 交付前：AI 标识检查」 | DONE | 标【官方】国信办通字〔2025〕2 号 + 视频号 6.4 |
| QA-02 | shared/hard-gates.md | 新增 §11 审核依据库（细则 58/62/77/82/93/99、(九)37–40；视频号 5.2.5/5.5.1/5.8.1–5.8.3/5.13.1/5.11.4/5.14.2；快手四-二）+ 效果标准 + 扫描范围含标题/话题/弹幕 + 禁点词对账（含 lessons 词表覆盖缺口登记）+ 空白注记（抖音公约/外部词表） | DONE | 标【官方】；词表扩充属 lessons 域未动 |
| QA-03 | shared/hard-gates.md §6 | 追加「广告合规补充」：极限词红线 + 6 类豁免 + 三领域从严 + 4.6.4 可识别性 + 细则 99 + 商标仿冒（3.4/3.5、快手五-3） | DONE | 标【官方】执法指南 2023 |
| QA-04 | skills/shot-qa/SKILL.md + references/three-gates.md | SKILL.md 流程补「交付前检查（AI 标识·法定义务）」+ 产出段补交付清单块；three-gates.md 补「交付清单填写模板」 | DONE | output-formats.md LOCKED 契约未动（不在施工范围，登记） |
| QA-05 | skills/shot-qa/SKILL.md 闸 2-4 + three-gates.md 违禁区 | 补扫描范围（标题/话题/弹幕/字幕）+ 效果标准 + 禁点词指向 hard-gates §11 | DONE | 标【官方】细则 62/5.5.1 |
| QA-06 | skills/shot-qa/references/three-gates.md 品牌三层扫 | 追加极限词扫描行（红线+豁免+从严领域+可识别性） | DONE | 标【官方】 |
| QA-07 | skills/shot-qa/references/trust-audit.md | 表头加「阈值来源注记」+「行业对照」两块；T1/T3/T5 三行阈值逐处标【经验·内部】 | DONE | 数值全保留（trust_audit.py 依赖）；U 级框架不动；批4「戳穿」注记 |
| QA-08 | skills/clip-review/references/checklist.md | 新增「质量维度命名对照（VBench 16 维）」：②↔主体一致性、④↔运动平滑、①⑤↔空间关系、时序闪烁标原缺口→硬伤扫描补位 | DONE | 标【学术：VBench·CVPR 2024】 |
| QA-09 | skills/clip-review/references/checklist.md | 新增「成片硬伤扫描（最低覆盖）」8 项（黑帧/定帧/静音爆音/响度峰值/规格/字幕文案/音画相关/官方低质缺陷清单） | DONE | 行【行业：framesense.io】+官方 5.11.4/5.14.2 |
| QA-10 | skills/clip-review/references/checklist.md + SKILL.md | 核验报告格式改「逐项 PASS/FAIL + 时间码 + 严重度（Critical/Warning/Info）三件套，禁只给加权总分」；SKILL.md 流程同步 | DONE | 标【行业：framesense.io】 |
| QA-11 | skills/clip-review/references/checklist.md | 报告格式示例「✗道具乙形态漂」→「✗形态漂【示例占位】」 | DONE | **原文留档**：`核验：①穿模 过（接触面分离清晰）②脸 过 ③道具 ✗道具乙形态漂 ④运动 过 ⑤光 过｜归因：③→参考图权重弱（道具图特写被场景稀释）→回流通道②：分镜道具暴露面设计规避`（「道具乙形态漂」=剧内实证词，2026-10-31 纪律换占位） |
| QA-12 | skills/video-producer/references/video-consistency.md §四 + SKILL.md 口型条目 | 新增「即梦对口型工具约束」块：清晰正脸/图片 ≤15s/视频 ≤36s/TTS ≤120 字/积分计法；TTS 单向生成工具层依据；5.11.4 验收底线；音素-视位空白注记 | DONE | 标【社区教程·工具行为：it.sohu.com】+【官方：volcengine/5.11.4】；分镜切分写法已标 →intake-direct（G-2） |
| QA-13 | skills/video-producer/references/video-consistency.md §二 + SKILL.md 话术条目 | 新增「官方兜底包」块：画质包/稳定包/字幕兜底/水印·Logo 兜底 + 双胞胎兜底/风格锚定/强方位约束/眼睛发光兜底 | DONE | 标【官方：火山 sd2-pe SKILL + 2.5 指南 FAQ】 |
| QA-14 | video-producer/SKILL.md:23、video-consistency.md §五、production-workflow.md §六、backends.md 计价块 | 30% 重生成余量四处全部标【经验·内部】+ 注记 | DONE | 数值保留 |
| QA-15 | video-producer/SKILL.md:24 | 0.8–1.5 倍缩放标【经验·内部】+ 注记 | DONE | 同句「单镜 2–4s」未动（→intake-direct，G-1） |
| QA-16 | video-producer/references/first-appearance-nametag.md | 文头加「参数注记」：0.8–1.5 秒/卡点参数=U 级用户定值标【经验·内部】 | DONE | **U 级内容一字未动**，仅加注记（铁律②） |
| QA-17 | shared/backends.md 计价块 | 新增 Dreamina Web 端能力行：2.5 单次 30s / extended 5–180s / Multiframes ≤10 帧每段 0–8s | DONE | 标【官方：dreamina.capcut.com 教程】批1 |
| QA-18 | shared/backends.md 计价块 | 新增素材侧两条：watermark 默认 true→素材显式 false；URL 24h 失效即时转存 + 与 hard-gates §10 互链 | DONE | 标【官方：volcengine 图片 API】批2 |
| QA-19 | shared/backends.md 计价块 | 「《实测项目A》口径：」→「计费实测口径（实测项目口径，2026-10-29）：」，数字全保留 | DONE | **原文留档**：`《实测项目A》口径：2310 镜成片 11166s → 计费约 11719s ≈ 70314 积分全剧；每集 516–780 积分（均 ~703）；613 积分 ≈ 0.87 集`（剧名=剧内数据，换归属注记；数字=实测来源禁删，全部保留） |
| QA-20 | shared/lighting-system.md 配方表头 | 新增「色温物理锚」注记块（1500K/3200K/5500–5600K/12000K + WB 关系 + 暖冷情绪=行业惯例非标准） | DONE | 标【行业：StudioBinder + 灯具行业规格】 |
| QA-21 | shared/lighting-system.md 六配方 | 表头加「配方数值档位」注记；6 个色温格 + 2 个百分比格（喜 <15%、悬疑 >60%）逐处标【经验·内部】 | DONE | 数值保留；批4 5.2 口径（锚有据/情绪用途=惯例/百分比=纯内部） |
| G-2 | skills/storyboard-director/references/shot-timing.md 音画对齐段 | 补一行交叉引用（口型/音频约束见 video-consistency，即梦 ≤15s/≤36s/≤120 字——分镜切分与音频反锁时长注意） | DONE（team-lead 指定动手项，越界仅此一行） | 标【社区教程·工具行为：it.sohu.com，2026-10】 |
| G-5 | skills/clip-review/references/defect-attribution.md 实证列 | 按裁定：内容保留，换「实测项目」归属注记+补日期（2026-10-30 材料提炼）；「镜1」镜位标识→「实测项目镜位」；道具乙/长发女相等事故关键词保留；表头加实证列说明块 | DONE | **原文留档**：实证列原值逐条=`2026-10-30 根治实证`（→加归属注记）、`镜1 首版事故`（→`首版事故（实测项目镜位，2026-10-30 材料提炼）`）、`道具乙三变事故`、`长发女相事故`、`上午戏挂黄昏景`（三者关键词保留，各加（实测项目，2026-10-30 材料提炼）） |
| G-1/3/4 | — | 关单：已被 intake-direct 镜长定案（shot-timing/selfcheck-7/pacing-templates）、prompt-format §十 sd2-pe 硬约束、shot-timing 三·附+backends Dreamina 段覆盖 | CLOSED | 登记覆盖落点，不再转手 |

**统计核对**：21 条施工条目全部 DONE；三档分布=官方级 9、社区实证级带源 5、经验值 5、专项清洗 2；G 项 5 条全部闭环（G-2/G-5 执行、G-1/3/4 关单）。本单越界动作仅 G-2 一行（team-lead 指定）；output-formats.md、lessons.md、tools/（trust_audit.py 阈值）未动。
