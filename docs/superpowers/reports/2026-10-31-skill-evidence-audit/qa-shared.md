# 证据来源审计：QA/出片执行/共享库（2026-10-31）

> 审计对象：`skills/shot-qa/`、`skills/clip-review/`、`skills/video-producer/` 全部 .md（SKILL.md + references/），`shared/` 全部 14 个 .md。
> 只读审计，未改动任何 skill/shared 文件。共 24 个文件、1758 行。

## 分级口径

| 级 | 含义 | 判定标准 |
|----|------|---------|
| U | 用户令 | 文件内标注「用户令/用户原话/用户定/用户供/用户终定/用户纠正/用户重排/用户立标」+ 日期 |
| O | 外部官方 | 标注官方文档且出处可追溯（本批仅 1 条经调研报告间接引用官方文档） |
| C | 外部调研/社区 | 标注调研/社区/他人实测且给出出处（含指向 `docs/superpowers/reports/2026-10-27-prompt-optimization-research.md` 的条目——该报告已核实存在、引 22 组检索/11 页深抓、来源清单齐全） |
| S | 自测实证 | 标注「实测/事故/翻车/审查实锤/机检」但无外部出处；含**有日期的内部决策/工序记录** |
| G | 无标注 | 无任何来源标注。细分：**G-A=漏标可补**（实源可考，补个标注即可，多半是用户令散落在 CLAUDE.md 五道硬闸/工作流规则/其他文件里）、**G-B=无源可考**（需调研或补实测才能背书） |

聚合口径：`camera-dictionary.md`（约 80 词条）、`director-styles.md`（6 风格）、`lighting-system.md`（6 配方）、`lessons.md`（按小节，23 节）按节/按条聚合为一行；其余文件逐条拆。纯目录/元信息/示例正文跳过，示例中承载规则的数字参数保留。

---

# 一、逐条清单

## skills/shot-qa/SKILL.md

| 位置 | 条目 | 级 | 原标注 |
|---|---|---|---|
| SKILL.md:10 | 三闸全过才准出片，任一 FAIL 打回对应环节 | S | 引 hard-gates「实战逐条验收」+ output-formats LOCKED |
| SKILL.md:43 | 分镜块↔剧本/Notion 逐字一致（SHA-256 级）；压缩/改写/拼装/加删标注头=FAIL | S | 「零压缩铁律…历史已犯过」（hard-gates §3） |
| SKILL.md:44 | 转场三件套（时间+地点+转场过渡句，明写不硬切）；转场点=相邻镜场景标签变化 | S | 引 lessons 第 8 条 |
| SKILL.md:45 | 品牌三层扫（画面/语音/字幕），命中打回，禁化名绕过 | S | 引 hard-gates §6 + lessons 第 9 条 |
| SKILL.md:46 | 违禁废话词表（4K/8K/杰作/超清晰/大师作/wallpaper） | G-B | 无标注，词表无出处 |
| SKILL.md:46 | 每镜细节 ≥250 字保底 | G-A | 无标注（实源=CLAUDE.md 五道硬闸 2026-10-19 用户令「下限250字保底」） |
| SKILL.md:46 | 本集看点/结尾钩子句号收尾且镜内有落点 | G-A | 无标注（实源=五道硬闸 G3 剧情核验用户令） |
| SKILL.md:50 | 露脸角色全挂（含对手戏）、场景必挂 | S | 引 lessons 第 13 条（双人镜漏挂事故） |
| SKILL.md:51 | ref ID 格式 `node_[a-z0-9]{10}`、节点 success；场景图纯空镜 | G-A | 无标注（格式=output-formats 契约；「有人场景不能用于出视频」实源=五道硬闸 G4 场景纯净用户令） |
| SKILL.md:55 | Notion 状态=「生成中」才许进花钱门 | G-A | 无标注（实源=CLAUDE.md 工作流规则「Notion 先行」2026-10-18/19 用户规则） |
| SKILL.md:56 | 规格复核：≤15s 自动分段/中文≤500字/每时间片一动作一运镜/情绪可视化/无废话词 | G-B | 无标注（数字属后端方言，无官方出处） |
| SKILL.md:60 | 按实估上限报价留档位差余量（quote≠run） | S | 引 lessons 第 6 条（实测 24 vs ≥56） |
| SKILL.md:61 | 用户明确批准（批准人+上限）才执行；素材审查过≠可花钱 | G-B | 无标注 |
| SKILL.md:62 | `approved_by` 假值→PermissionError；`--credit-ceiling` 剥离独占；超账单必须重新获批 | G-B | 无标注（可对照 tools/credit_gate.py 代码验证） |
| SKILL.md:64 | shot-qa 只检查报价不执行；执行=自动为主、手动贴即梦备选 | G-B | 无标注 |
| SKILL.md:68 | 验真只认 submission.resources 且 createdAt 晚于提交；历史 success 不算 | S | 引 lessons 第 7 条 |
| SKILL.md:85-92 | 硬规 8 条：一枪一停/原节点重跑/重制不夹带/验真/Notion 唯一控制面/花钱门零容忍/零压缩/品牌三层禁 | S | 引 hard-gates 各节（实战验收） |
| SKILL.md:81 | 五道硬闸 G1–G5（分镜细节/素材关联/剧情核验/场景纯净/Notion 先行）任一 FAIL 拒绝生成 | G-A | 无标注（实源=CLAUDE.md 五道硬闸 2026-10-19 用户令） |

## skills/shot-qa/references/three-gates.md

| 位置 | 条目 | 级 | 原标注 |
|---|---|---|---|
| three-gates.md:17 | 报价单格式模板（逐镜单价×数量+总价上限+批准话术） | G-B | 无标注，模板句自定 |
| three-gates.md:20 | quote≠run 档位差，账单按实估上限报 | S | 「shared/lessons.md 第 6 条」 |
| three-gates.md:21 | 报价失败/无上限一律抛错，禁止静默报 0 | G-B | 无标注 |
| three-gates.md:25 | 批准=明确回复「批准」+批准人+批准上限 | G-B | 无标注 |
| three-gates.md:26 | 审查通过≠批准花钱，批量/重制禁自己开跑 | G-B | 无标注 |
| three-gates.md:27 | `approved_by` 假值 PermissionError；花钱门独占 ceiling | G-B | 无标注（可对代码验证） |
| three-gates.md:28 | 超账单重新 quote→重新批→才许续跑 | G-B | 无标注 |
| three-gates.md:38-40 | SHA-256 对账命令（shasum -a 256 双侧同法提取） | S | 零压缩铁律「历史已犯过」 |
| three-gates.md:43 | 空白/换行归一化必须两边同处理，禁制造假一致 | G-B | 无标注 |
| three-gates.md:44 | 本地拼装/多段合一/加删标注头=FAIL | S | 「shared/lessons.md 第 10 条」 |
| three-gates.md:48 | 转场点判定=相邻镜六要素.场景标签变化 | G-B | 无标注 |
| three-gates.md:49-53 | 转场三件套缺一即 FAIL；同场景共用场景资产；裸切打回 | S | 「shared/lessons.md 第 8 条」 |
| three-gates.md:63-64 | 品牌词表 brand-wordlist.txt；三层命中 FAIL 禁化名；商品写死素色无品牌+禁包装特写 | S | lessons 第 9 条 / hard-gates §6 |
| three-gates.md:68 | 违禁废话词表（同 6 词） | G-B | 无标注 |
| three-gates.md:69 | 每镜 ≥250 字，不足打回 storyboard-director | G-A | 无标注（实源=五道硬闸用户令） |
| three-gates.md:70 | 看点/钩子句号收尾+镜内落点；字面不中附镜内原句举证；禁为塞关键词改写剧本 | G-A | 无标注（实源=五道硬闸 G3） |
| three-gates.md:78-83 | 挂载矩阵：露脸全挂含对手戏/场景必挂/表情服装同源/refs≤9 | S（前三项，lessons 3/13）；refs≤9 为 G-B | 引 lessons 13/3；≤9 无标注（实为后端 m2v 上限方言） |
| three-gates.md:87-88 | ref 格式 node_+10 位；场景纯空镜 | G-A | 无标注（契约/五道硬闸 G4） |
| three-gates.md:92-95 | 验真流程 4 步（提交时间戳记账→submission.resources→createdAt 比对→轮询等新资源） | S | 「shared/lessons.md 第 7 条」 |
| three-gates.md:96 | Notion 查询走 tools/notion_mcp_client.py | G-B | 无标注（工具存在） |
| three-gates.md:98 | 一枪一停/原节点重跑/重制不夹带 | S | 「shared/hard-gates.md 第 5 节」 |
| three-gates.md:104-122 | 检查报告 LOCKED 填写模板 | G-B | 无标注（契约模板自定） |
| three-gates.md:125 | 三闸全过才准出片 | S | hard-gates 实战 |

## skills/shot-qa/references/trust-audit.md

| 位置 | 条目 | 级 | 原标注 |
|---|---|---|---|
| trust-audit.md:1-5 | 分镜可信度审计框架；新写分镜须 A 级才进生成包、存量 C 级强制重写 | U | 「2026-10-29 用户令」 |
| trust-audit.md:11 | T1 叙事占比 ≥35% 过 / <25% 判 C | G-B | 无标注，阈值无实证 |
| trust-audit.md:12 | T2 自足性禁词表（同镜X完整描述/复述锚点/以本描述为准/完整状态照写） | G-A | 无标注（六维细则应属用户令延伸，漏标） |
| trust-audit.md:13 | T3 模板复读相似度 <65% 过 / ≥80% 判 C | G-B | 无标注，阈值无实证 |
| trust-audit.md:14 | T4 位移镜三要素（动线/步速/谁动）；禁双动叠加 | G-A | 无标注（与 camera-dictionary「一镜一主运镜」同口径，漏标） |
| trust-audit.md:15 | T5 生产纯净：零 @引用头/〔〕/编译器指令；≥3 处判 C | G-B | 无标注，计数阈值无实证 |
| trust-audit.md:16 | T6 五要素覆盖（演/动/拍/光/声） | G-A | 无标注 |
| trust-audit.md:20-22 | A/B/C 评级规则（≤2 维不过=B；≥3 维或 T2/T4 单维=C） | U | 「用户令」框架内细则 |
| trust-audit.md:27 | 审计产出格式模板 | U | 同上 |

## skills/clip-review/SKILL.md

| 位置 | 条目 | 级 | 原标注 |
|---|---|---|---|
| SKILL.md:13 | 抽帧核验：首/中/尾帧+接触区 crop 放大 | S | 引 checklist「2026-10-30 教训」 |
| SKILL.md:14 | 缺陷归因四层（分镜写法/参考图配比/模型能力/素材缺口），层归错修也白修 | S | 引 defect-attribution「2026-10-30 材料提炼」 |
| SKILL.md:15 | 回流三通道；skill 规则须对照稿交用户批后写入，禁擅改 | G-A | 无标注（实源=lessons「改 skill 前四步」2026-10-31 用户纠正，漏标） |
| SKILL.md:18 | 一次翻车=一条新规，禁同坑二翻 | G-B | 无标注，纪律句自定 |
| SKILL.md:19 | 禁止积分试错，缺陷修文本层；模型能力上限类走设计规避 | G-B | 无标注 |
| SKILL.md:20 | 核验不过=崩坏镜按 video-producer 口径单独重生成 | G-A | 无标注（与 hard-gates §5 原节点重跑同源，漏标） |

## skills/clip-review/references/checklist.md

| 位置 | 条目 | 级 | 原标注 |
|---|---|---|---|
| checklist.md:3 | 抽帧法+接触区 crop（穿模在缩略图看不出） | S | 「2026-10-30 教训」 |
| checklist.md:6-11 | 五项核验判定清单（穿模解剖/脸与服装/道具锚/运动姿态/场景光影） | S | 「2026-10-30 材料提炼」 |
| checklist.md:13 | 核验报告格式模板（①-⑤+归因+回流通道） | S | 同上（自定模板） |

## skills/clip-review/references/defect-attribution.md

| 位置 | 条目 | 级 | 原标注 |
|---|---|---|---|
| defect-attribution.md:5-12 | 归因矩阵 8 行：穿模→接触几何律/原地踏步→运动矢量律/道具服装漂移→锚句+暴露面规避/镜内变脸→参考图职责表/文字乱码→纯净律/光比→代景禁「以正文为准」/声画两张皮→声画绑定四层/模型能力上限→设计规避 | S | 「2026-10-30 材料提炼」；实证列：2026-10-30 根治实证、镜1 首版事故、道具乙三变事故、长发女相事故、上午戏挂黄昏景 |
| defect-attribution.md:14 | 归因口诀（分镜→参考图→模型→素材） | S | 同上 |

## skills/video-producer/SKILL.md

| 位置 | 条目 | 级 | 原标注 |
|---|---|---|---|
| SKILL.md:20 | 前置资产校验（三视图无歧义/五官统一/场景风格对齐/LoRA·IP-Adapter「强一档」） | G-B | 无标注，效果断言无出处 |
| SKILL.md:21 | 单镜隔离生成，禁批量连跑（一崩全崩） | G-B | 无标注（实战口吻但无实证标注） |
| SKILL.md:22 | 试产 2–3 镜锁参（特写/中景/带动作各一），验变脸/服装/运镜；批量期禁改 | G-B | 无标注 |
| SKILL.md:23 | 每镜 2 版备选，预算 30% 重生成余量 | G-B | 无标注，30% 无出处 |
| SKILL.md:24 | 后期统一收口工艺包（气泡/音效三分层+不盖台词/整片一个 LUT/转场词典/静态漫剧 0.8–1.5 倍缓动/首出场名条/崩坏镜单独重生成） | U | 引 manhua-production-standard「2026-10-28 用户供」+ first-appearance-nametag「2026-10-28 用户定」 |
| SKILL.md:28 | 出片五律（分镜即指令/付费前审查/@素材真实绑定/素材-分镜数据一致/Notion 对齐），任一 FAIL 拒绝生成 | U | 「2026-10-29 用户令，最高优先级」 |
| SKILL.md:28 | 五律 1 唯一机械处理=换行归一化+剥离素材映射行/资源ID | U | 「2026-10-30 用户令」 |
| SKILL.md:29 | 画幅统一 16:9 横版（--ratio 16:9） | U | 「2026-10-28 用户终定」 |
| SKILL.md:30 | 即梦出片一律 seedance_2.0_fast_vip；其他模型禁用于产品生成，比价只准 quote 不准 run | U | 「2026-10-29 用户定」 |
| SKILL.md:31 | 花钱门含重生成余量一并报价；重生成也走闸 | G-B | 无标注 |
| SKILL.md:33 | 参考图用量：每角色 ≤正面1+侧视1；禁多张三视图同 prompt；总 ref ≤9 | G-B | 无标注（video-consistency §一 同；≤9 实为后端方言） |
| SKILL.md:34 | 一致性锁句每镜必带 | G-B | 无标注 |
| SKILL.md:35 | 动作减法：单镜 1 核心动作，复杂动作拆镜 | G-A | 无标注（同 hard-gates §8「每时间片一动作」，漏标） |
| SKILL.md:36 | 运镜保守：禁高速环绕/大幅摇镜/动态模糊+特写（人脸必漂） | G-B | 无标注，「必漂」无实证标注 |
| SKILL.md:37 | 台词镜先产音频反锁分镜时长，禁先视频后配音；口型不准走后期对口型 | G-B | 无标注 |
| SKILL.md:38 | 一枪一停/原节点重跑/验真只认新产物 | S | 引 shared/hard-gates（实战） |

## skills/video-producer/references/production-workflow.md

| 位置 | 条目 | 级 | 原标注 |
|---|---|---|---|
| production-workflow.md:5-7 | 前置校验清单 3 条（三视图/静态场景优先/LoRA·IP-Adapter「稳定性天花板」） | G-B | 无标注，效果断言无出处 |
| production-workflow.md:13-19 | 单镜隔离生成包结构模板 | G-B | 无标注 |
| production-workflow.md:21 | 禁批量连跑（批量连锁翻车一崩全片废） | G-B | 无标注 |
| production-workflow.md:25-31 | 试产锁参三验证 + 测试不过回分镜层不硬跑 | G-B | 无标注 |
| production-workflow.md:35-38 | 素材入库规范：命名/失败四分类（变脸/肢体崩/场景错/服装串）/保留失败版/崩坏镜只重生成该镜 | G-B | 无标注（四分类无出处） |
| production-workflow.md:42-45 | 后期收口 4 条（统一调色降噪/淡入淡出掩盖闪烁/台词音效字幕全部后期叠加/特写崩坏 3D 数字人补镜） | U（前三条与 manhua §七 用户供同源）；第四条 G-B | 无标注（正文引 manhua「行业标准」） |
| production-workflow.md:49-53 | 三条工具路线 A 图生视频/B 3D/C 混合（推荐 C） | G-B | 无标注，推荐为自定 |
| production-workflow.md:57-62 | 极简 SOP 6 步 | G-B | 无标注 |
| production-workflow.md:65-72 | 高频翻车清单 7 条（画风混搭/超时长/服装版本/参考图过多/无统一负面词/不拆镜/动态模糊+特写） | G-B | 无标注（实战口吻无实证标注） |

## skills/video-producer/references/video-consistency.md

| 位置 | 条目 | 级 | 原标注 |
|---|---|---|---|
| video-consistency.md:7 | 统一角色 ID 命名（Char_A_基础服_正/侧/背）；禁 AI 自动换装 | G-B | 无标注 |
| video-consistency.md:8 | 参考图用量 ≤1 正面主参考+1 侧视；多张三视图=参考冲突崩坏 | G-B | 无标注 |
| video-consistency.md:9 | 两层资产分工（基础三视图管脸型五官头身比/服装三视图只换服饰） | G-B | 无标注 |
| video-consistency.md:10 | 角色参考卡（正面大图+侧背小图合成卡） | G-B | 无标注 |
| video-consistency.md:11 | 同场景多镜共用场景参考+光影四件套逐镜复制 | G-A | 无标注（同 prompt-formula §四/lessons 行业坑，漏标） |
| video-consistency.md:12 | 双保险铁律：@资产引用≠免描述，引用后必须跟完整文字描述 | G-A | 无标注（实源=五律 3/双保险用户令，漏标） |
| video-consistency.md:16-19 | 一致性锁句固定模板（强制保持五官脸型发色身高不变+严格使用服装套名） | G-B | 无标注，模板句自定 |
| video-consistency.md:23-25 | 视频负面黑名单 7 词（五官扭曲/肢体畸形/多余手指/服装错乱/变脸/闪烁/帧间漂移） | G-B | 无标注 |
| video-consistency.md:29-32 | 运镜安全边界：禁高速环绕/大幅摇镜；动态模糊禁配特写；复合动作必拆；说话镜降运镜 | G-B | 无标注 |
| video-consistency.md:36 | 台词镜先产音频反锁时长；音频轨进 shot-timing.md 音频提示列 | G-B | 无标注（shot-timing.md 实际存在于 storyboard-director/references/，引用无路径） |
| video-consistency.md:37-39 | 口型两走法（无台词表演+后期对口型优先/口型驱动+低运镜） | G-B | 无标注 |
| video-consistency.md:40 | 台词逐字来自剧本（零压缩），口型层不改词 | S | 零压缩铁律同源（hard-gates §3） |
| video-consistency.md:44 | 批量期三不改（参数/参考图组合/提示词结构） | G-B | 无标注 |
| video-consistency.md:45 | 每镜 2 版备选、30% 重生成余量 | G-B | 无标注 |
| video-consistency.md:46 | 失败归因四分类入库；重生成前先归因改对应层 | G-B | 无标注 |

## skills/video-producer/references/first-appearance-nametag.md

| 位置 | 条目 | 级 | 原标注 |
|---|---|---|---|
| first-appearance-nametag.md:3 | 首出场名条工艺：首次出场定格+名条，全剧每人一次 | U | 「2026-10-28 用户定」 |
| first-appearance-nametag.md:7-11 | 五步工序（定格/可选抠像描边卡片/名字条「角色名｜身份」圆角矩形+细分割线/入场动画三选一+停留 0.8–1.5 秒/卡点+叮音效） | U | 「2026-10-28 用户定」 |
| first-appearance-nametag.md:15 | 动态人物文字跟踪变通；默认方案仍是定格卡片 | U | 同上 |
| first-appearance-nametag.md:20-22 | 分工链（分镜层标注/后期层制作，收口清单登记） | U | 同上 |
| first-appearance-nametag.md:26-34 | 身份标签命名表（角色甲｜男主 等剧内角色条目） | U（剧内数据） | 「2026-10-28 用户定」；⚠️ 违反 lessons「剧内数据住 assets.json/Notion，skill 只住跨剧方法」（2026-10-31 用户纠正），见矛盾清单 M5 |
| first-appearance-nametag.md:38-41 | 自检 4 条（恰好一次/0.8–1.5 秒+叮音/卡点入画帧/文本逐字一致） | U | 同上 |

## shared/hard-gates.md

| 位置 | 条目 | 级 | 原标注 |
|---|---|---|---|
| hard-gates.md:3-5 | 2026-10-27 定案；规则来自漫剧实战逐条验收；与 skill 文案冲突以本文件为准 | S | 「实战逐条验收过的硬闸」 |
| hard-gates.md:9 | 零容忍：废话词 4K/8K/杰作/超清晰/大师作/wallpaper（「塑料 AI 感」） | G-B | 无出处 |
| hard-gates.md:10 | 零容忍：硬切转场、转场无时空交代 | S | 实战（lessons 8） |
| hard-gates.md:11 | 零容忍：品牌植入三层禁 | S | lessons 9 |
| hard-gates.md:12 | 零容忍：未经批准烧积分；指令压缩/改写后出片 | S | lessons 6/10 |
| hard-gates.md:18 | 花钱门：凡扣积分必过（素材图也不例外） | S | 实战验收语境 |
| hard-gates.md:22-24 | 三步程序（node quote 报价→用户批→--run 带批准人+ceiling，缺批准信息拒绝执行） | G-B | 无标注 |
| hard-gates.md:26 | quote≠run 实测：quote 报 24/镜、run ≥56/镜（模型档位差） | S | 「实测」 |
| hard-gates.md:29 | 超账单必须重新获批，禁拿旧批文硬跑 | G-B | 无标注 |
| hard-gates.md:31 | 职责边界；出片执行=自动为主手动备选 | G-B | 无标注 |
| hard-gates.md:35-37 | Notion 唯一控制面；生成状态=「生成中」才许生成；Schema 沿用不迁移 | G-A | 无标注（实源=CLAUDE.md 工作流规则+五道硬闸 G5 用户令） |
| hard-gates.md:41-42 | 零压缩：Notion 指令=原始数据，逐字搬运 SHA-256 校验 | S | 「历史已犯过，见 lessons」 |
| hard-gates.md:46-49 | 验真只认提交后新 resource；createdAt 比对；自动回填 Notion | S | lessons 7 语境 |
| hard-gates.md:53-55 | 一枪一停/原节点重跑/重制不夹带 | S | 实战验收 |
| hard-gates.md:59-65 | 广告三层禁（真实品牌/品牌感包装/Logo）+ brand-wordlist 词表 + brand_scan 扫描 | S | lessons 9 + 实战 |
| hard-gates.md:71-74 | 转场两件套（时空交代+转场过渡句，明写不硬切）；同场景共用资产 | S | lessons 8（⚠️ 与 shot-qa「三件套」口径不一致，见 M2） |
| hard-gates.md:78-84 | 后端方言规格：≤15s 自动分段/中文≤500 字/每时间片一动作一运镜/写实真人面部转 3D 防拦截/情绪可视化/禁废话词/参考图语义（「当首帧」才首帧；接戏用 first_last_frame，绝不用整条视频做 ref） | G-B | 无标注（数字无官方出处；首尾帧口径与 lessons 5 实证同源但未标） |
| hard-gates.md:88-90 | 留存三主轴（场景转场连贯/剧情分镜/人物建模质量） | G-B | 无标注 |
| hard-gates.md:94-110 | 执行顺序总览（所有内容检查在报价之前，「先检查再花钱」） | G-B | 无标注，流程口径自定 |
| hard-gates.md:112-114 | 出片五律框架+背景（58 积分因提示词压缩改写+漏挂道具参考作废） | U+S | 「2026-10-29 用户令，最高优先级」+烧积分实证 |
| hard-gates.md:116 | 五律 1 分镜即指令四段式逐字节；唯一机械处理=换行归一化+剥离生产数据；超上限回 Notion 设计变更 | U | 「2026-10-30 用户令」；引 manju-pipeline/generation-workflow.md L109 同源 |
| hard-gates.md:117 | 五律 2 付费前 shot_gate.py 全闸+Notion 状态审查 | U | 「2026-10-29 用户令」 |
| hard-gates.md:118 | 五律 3 @素材真实绑定（含状态变体，人物走设定卡唯一入口） | U | 同上 |
| hard-gates.md:119 | 五律 4 素材-分镜数据一致（信物-原色≠信物-浅红；res:/画布 ID 逐个核对） | U | 同上 |
| hard-gates.md:120 | 五律 5 Notion 对齐（本地↔Notion SHA 级一致才准出片） | U | 同上 |
| hard-gates.md:122 | 执行件 shot_gate.py，配置驱动，任一闸 FAIL 拒绝生成无例外 | U | 五律落地 |

## shared/backends.md

| 位置 | 条目 | 级 | 原标注 |
|---|---|---|---|
| backends.md:1-3 | 后端可插拔定位（虚拟导演+提示词工程师，后端无关） | U | 「2026-10-27 用户定」 |
| backends.md:8-10 | 通用核心 vs 后端方言分层（六要素/时间片/转场/情绪可视化/风格库/三层光影/7 项自检） | G-B | 无标注，方法论自定 |
| backends.md:16 | 即梦方言：中文≤500 字/单次≤15s 自动分段/m2v 最多 9 图/`--ref res:<uuid>`/无真负面正向改写/验真 resource get+node find/dreamina+dreamina-canvas 双 CLI 无 MCP | G-B | 无标注（⚠️ 参数应有即梦官方文档可查，缺口主题 K4） |
| backends.md:17 | 可灵：中文≤800 字量级/≤10s/首尾帧+运动笔刷/有负面参数 | G-B | 「（按其文档校准）」= 自认未校准 |
| backends.md:18 | 海螺：中文≤600 字量级/≤10s/部分支持负面 | G-B | 同上 |
| backends.md:19 | 小云雀：默认图模型=智能图片V2.5 Fast | U | 「2026-10-28 用户定」 |
| backends.md:19 | 小云雀参数：--ratio 数字枚举（2=16:9/3=9:16/6=1:1）/--resolution 1K/2K/4K/--effort low→max | S | 「实测」语境（CLI 实际用法） |
| backends.md:19 | 智能图片V2.5 Pro ≈6 积分/张 1K/high；i2i 排版被参考图锚定；query-result 多行 JSON 勿 tail -1 | S | 「实测」 |
| backends.md:20 | Midjourney：仅手动路径（无官方 API）/sref·cref 语义/--no 真负面/人工验图 | G-B | 无标注（行业常识） |
| backends.md:21 | SiliconFlow：REST 端点/模型清单（Qwen-Image、Qwen-Image-Edit、Tongyi-MAI/Z-Image-Turbo、Kwai-Kolors、Wan2.2 T2V/I2V）/图片 URL 时效 24h | G-B | 无标注（应为 API 实测/文档，未标） |
| backends.md:22 | SD/ComfyUI：ControlNet/IP-Adapter/真负面/本地产物 | G-B | 无标注（常识） |
| backends.md:24 | 一致性参数语义（2026-10-27 调研修正）：--seed 不锁人物（MJ 官方明言）；MJ --cref/--cw 75-85+--sref；SD/Flux IP-Adapter/PuLID/InstantID/LoRA；画质词分平台 | C（--seed 断言为 O-间接） | 「2026-10-27 调研修正」「MJ 官方明言」→引 reports/2026-10-27-prompt-optimization-research.md §③（已核实含 MJ 官方 Seeds 文档出处、cw 75-85 出自 PromptMake） |
| backends.md:26 | 「量级数字是起点不是枷锁，按官方文档校准」 | G-B | 免责句 |
| backends.md:28-31 | 即梦计价实测矩阵（2026-10-29 node quote 实测）：seedance_pro_fast 2 积分/秒（单参考，只配无脸/纯手部/空镜）/seedance_2.0_fast_vip 6 积分/秒（m2v≤9 图 4–15s）/mini 6/2.5 20 积分/秒；4s=24、5s=30、10s=60 | S | 「2026-10-29 node quote 实测」 |
| backends.md:30 | 出片提示词零压缩铁律（烧 58 积分实证）+双闸（SHA-256 对账+参考图覆盖校验） | S | 「2026-10-29 烧 58 积分实证」 |
| backends.md:32 | 生成时长下限 4s（--duration min=4），计费按 max(4, 镜时长) | S | 实测/工具行为 |
| backends.md:33 | 上限 15s/次（step 1）；>10s 分段每段独立最短 4s | S | 实测 |
| backends.md:34 | 《实测项目A》计费口径：2310 镜 11166s→≈70314 积分全剧；每集均 ~703 | S | 实算（剧内数据，⚠️ 见 M5） |
| backends.md:35-36 | 三步门（create/quote/confirm+run）；素材挂载/删除三步（delete→confirm 签 token→--delete-token） | S | 工具实测 |
| backends.md:37 | <4s 快切镜口径（2026-10-29）：按 4s 出 24 积分，时间轴 --clip trim=毫秒裁剪；备选 ffmpeg | S | 「2026-10-29」实测口径 |
| backends.md:38 | CLI 能力面↔界面映射；「导演工具箱/导演台」Beta 为界面专属 CLI 无对应 | S | 实测观察 |
| backends.md:42-46 | 使用规则 5 条（项目声明后端/切换重校方言/工具前提检查/花钱门验真后端无关/新后端加一行） | G-B | 无标注 |
| backends.md:50-51 | 命名口径（虚拟导演+提示词工程师；触发词保留平台词） | G-B | 无标注 |

## shared/camera-dictionary.md（聚合）

| 位置 | 条目 | 级 | 原标注 |
|---|---|---|---|
| camera-dictionary.md:4 | 收录原则：全部为视频模型可稳定理解的通用运镜词；生僻词引发画面畸变/主体漂移/构图塌缩 | G-B | 无标注，机理断言无实证 |
| camera-dictionary.md:6 | 每镜 1 条主运镜+至多 1 条景深/焦段修饰，禁堆 3 条以上 | G-B | 无标注，数量参数自定 |
| camera-dictionary.md:7 | 运镜速度必须写明，不写默认匀速 | G-B | 无标注 |
| camera-dictionary.md:8 | 中英括注用法（中文提示词只写中文） | G-B | 无标注 |
| camera-dictionary.md:9 | 甩切/急速变焦仅动作/转场镜，文戏禁用（易抖崩） | G-B | 无标注 |
| camera-dictionary.md:10 | 「本词典全部条目均为安全词（safe），可直接复制进提示词」 | G-B | 无标注（⚠️ 疑似杜撰 D1） |
| camera-dictionary.md:12-138 | 13 节约 80 词条（推拉/摇移/跟拍/升降/环绕/固定长镜头/手持/变焦焦段/角度机位/景别/穿越前景/航拍/节奏修饰），每条=中文名+英文对照+用途 | G-B | 无标注（电影通用术语本体可信，但「安全/用途」断言与 Seedance 实测无对照；缺口主题 K4 运镜词官方全表） |
| camera-dictionary.md:99 | 斜角倾斜角 ≤10° | G-B | 无标注，数字无出处 |
| camera-dictionary.md:100 | 荷兰角倾斜角 10–25°、一镜最多一次 | G-B | 无标注，数字无出处 |

## shared/lighting-system.md

| 位置 | 条目 | 级 | 原标注 |
|---|---|---|---|
| lighting-system.md:3 | 光影三层拼装（环境→主光→情绪），缺层=光影失控 | G-B | 无标注 |
| lighting-system.md:5 | 同场环境层+主光层全镜一致，仅情绪层可逐镜变 | G-B | 无标注 |
| lighting-system.md:6 | 光影段 2–3 句，不超 3 句（写多必糊） | G-B | 无标注，句数参数自定 |
| lighting-system.md:7 | 配方表是起点不是枷锁 | G-B | 无标注 |
| lighting-system.md:8 | 与 director-styles 冲突时风格库光影优先 | G-B | 无标注 |
| lighting-system.md:27 | 一镜只允许 1 个主光 | G-B | 无标注 |
| lighting-system.md:57-127 | 六情绪配方（喜 4500–5200K 暗部<15%/怒 3800–4500K/惊 5600–6500K/悲 6500–8000K/悬疑 6000–7000K 暗部>60%/温馨 3200–4200K），各含光源方向/色温/对比度/阴影质感+提示词句 | G-B | 无标注（⚠️ 色温区间与百分比阈值疑似杜撰 D2；摄影布光资料明显可查，缺口主题 K8） |
| lighting-system.md:131-141 | 三层拼装示例 3 条 | G-B | 无标注，模板句 |

## shared/prompt-formula.md

| 位置 | 条目 | 级 | 原标注 |
|---|---|---|---|
| prompt-formula.md:6-11 | 七要素公式（主体/动作/服装/场景/构图/光影/画质风格） | G-B | 无标注 |
| prompt-formula.md:24 | 七要素顺序即权重顺序，主体永远第一 | G-B | 无标注，机理断言无出处 |
| prompt-formula.md:25 | 逗号分隔短句，忌长从句 | G-B | 无标注 |
| prompt-formula.md:26 | 生图只写固定景别不写运镜 | G-B | 无标注 |
| prompt-formula.md:27 | 中英分流（SD/MJ/Niji 用英文因 CLIP 中文损耗；即梦中文第一梯队；Flux 涉文化用母语） | G-B | 无标注（与调研报告 L153「母语更地道」一致但未标） |
| prompt-formula.md:21 | 画质词分平台：Booru 有效 ≤3 个/SDXL 反噬换相机词/Flux·MJ·GPT·即梦删掉 | C | 「模型相关弱偏置」；同源调研报告（Promgrammer 实测+BFL 官方），本文漏标出处 |
| prompt-formula.md:31-38 | 一致性两层控制模板句（Strictly based on…三视图锁身份 / In the same style as…人物面部光线与环境光一致） | G-B | 无标注，模板句自定 |
| prompt-formula.md:39 | 「两层配合=跨镜同人的行业标准做法」 | G-B | 无标注，「行业标准」自封 |
| prompt-formula.md:41-44 | 三条硬规则（参考图显式输入位/多参考写每图职责/一图一变量） | C | 「2026-10-27 调研修正」（报告含 Seedream 官方指南出处） |
| prompt-formula.md:48-58 | 景别/角度词表 9 条中英对照 | G-B | 无标注（术语常识） |
| prompt-formula.md:66 | 超限先砍内容段修饰词，风格段/构图锁不砍 | G-B | 无标注 |
| prompt-formula.md:67 | 光影段写光影四件套逐镜复制 | G-B | 无标注 |
| prompt-formula.md:68 | 负面段分流：SD 5–15 精准词/MJ --no 3–5 词（without X 被反读）/Flux·GPT·即梦无负面通道正向改写 | C | 「调研实测」（报告 L129-133 有 PromptMake/BFL/Google 官方出处） |
| prompt-formula.md:69 | 风格互斥词分流（cel 系禁写实词；cg-refined 反向禁 cel 词，相机词合法） | C | 调研同源（漏标） |
| prompt-formula.md:70 | 视频负面黑名单 7 词 | G-B | 无标注 |
| prompt-formula.md:71 | 构图锁（禁背景混入/禁多格/禁文字气泡） | G-B | 无标注 |
| prompt-formula.md:73-82 | t2i/i2i 选择表（三视图 t2i/服装表情 i2i 挂主体/场景变体 i2i 挂主图/Q 版显式禁多视图/融合图挂人物基准） | S | 无标注但有 lessons 1/3/11 实证同源（漏标） |

## shared/script-craft.md

| 位置 | 条目 | 级 | 原标注 |
|---|---|---|---|
| script-craft.md:3 | 「剧本是戏不是信息表」总纲 | S | 「2026-10-27 试产翻车根因修复」 |
| script-craft.md:7 | 铁律：读者读不下去=废稿；通读检验四征（卡壳/想跳/无画面/无情绪起伏） | S | 试产翻车修复语境 |
| script-craft.md:12-33 | 好坏对照 4 组（叙事画面戏/情绪可视化/对白两层/节奏呼吸） | S | 校准样例（⚠️ 样例含剧内角色「角色丙」，见 M5） |
| script-craft.md:37-43 | 叙事技法 7 条（五感开场/动作链/物件叙事/对白三条/张弛配方「漫剧特有」/信息投喂/钩子落地须是画面） | G-B | 无标注（编剧方法论自定，「漫剧特有」断言无出处） |
| script-craft.md:47-53 | 三稿制（初稿结构/精修文笔/定稿人读），一稿交付=违规 | S | 试产翻车修复语境 |
| script-craft.md:57-62 | 可读性人读五问 | S | 配套工序 |
| script-craft.md:63 | 一问不过回精修、两问不过重写 | G-B | 无标注，阈值自定 |
| script-craft.md:67-69 | 题材质感提醒（惊悚靠反常细节/规则感靠精确数字/温情恐怖同框） | G-B | 无标注（示例来自剧内） |

## shared/script-standard.md

| 位置 | 条目 | 级 | 原标注 |
|---|---|---|---|
| script-standard.md:3 | 《丧尸清道夫》范本=内核参考非模板；吸收 DNA 不填模板 | U | 「2026-10-27 用户立标」 |
| script-standard.md:7-13 | 内核参照 5 条（内核一句话/反差骨相/幽默温情血肉/电影语言/设定为叙事服务）；判定法=读一遍能放电影 | U | 用户立标语境 |
| script-standard.md:19-29 | 七段式载体（背景/风格核心 3–4 风格词+反差句/内核两段式/人物公式/场景公式+反差句收尾/道具规格/故事内容） | U | 「范本的载体形态，供采用与裁剪」 |
| script-standard.md:33-41 | 叙事语法 9 条（散文体/转场词即镜头语言/动作链/情绪线/黑色幽默落点/状态词点睛/反差写明/伏笔反转/收尾句式「画上圆满句号。至此，影片结束。」） | U | 从范本提炼 |
| script-standard.md:45-48 | 百集落地（每集一份七段式/头部元数据行/集间承接/写作顺序先故事后设定） | U | 用户立标延伸 |
| script-standard.md:46 | 「句号收尾」=单句号禁「。。」重复标点 | S | 「2026-10-28 剧本审查实锤：十集 18 处双句号」 |
| script-standard.md:52-58 | 验收七问（标题写「五问」实列 7 条，⚠️ 见 M3） | U | 用户立标语境 |
| script-standard.md:60 | 一问不过回精修、两问不过重写 | U | 同上 |

## shared/split-methodology.md

| 位置 | 条目 | 级 | 原标注 |
|---|---|---|---|
| split-methodology.md:3-4 | 根原则：由小说出发改编=取尽+补完+扩写，不删不缩水不脱离原著 | U | 「2026-10-27 用户供」 |
| split-methodology.md:9 | 换算锚：微短剧 1 分钟≈200–400 字 | U（数字无外部出处，缺口 K5） | 「用户供」+「参考非定值」 |
| split-methodology.md:10 | 一章 2000–4000 字拆 3–5 集（1–2 分钟/集）或 2–3 集（3–5 分钟/集） | U（同上） | 同上 |
| split-methodology.md:11-12 | 禁按字数硬切；单集 30–120 秒自动，禁硬凑注水 | U | 同上 |
| split-methodology.md:16-21 | 故事单元拆分规则（一集一微事件+起承转合+钩子/1–3 场景/刀口跟转折点/禁一章一集/连贯标题同集/装满容量合并） | U | 同上 |
| split-methodology.md:25-30 | 连贯改编技法 6 条（叙述→视听/结尾钩子调顺序提前冲突/对话立人禁旁白/开头 5 秒抓人/主线贯穿/名台词 ≤20 字照引） | U（≤20 字参数无外部出处） | 同上 |
| split-methodology.md:34-38 | 每集结构模板（首集建置/中间升级/末集高潮） | U | 同上 |
| split-methodology.md:44-50 | 操作步骤 7 步 | U | 同上 |
| split-methodology.md:54-55 | 两核心验收（灵活叙事/剧本理解） | U | 同上 |

## shared/style-library.md

| 位置 | 条目 | 级 | 原标注 |
|---|---|---|---|
| style-library.md:4 | 风格知识按一风格一 skill 深化；本文件只做选择器 | S | 「（2026-10-27）」内部决策 |
| style-library.md:9 | style-cg-refined=主风格「2026-10-27 由 3D 卡通升级」 | S | 日期标注 |
| style-library.md:13 | style-photoreal「即梦链路需转 cel 防拦截」 | G-B | 无标注（拦截口径无实证，同 hard-gates §8） |
| style-library.md:17-20 | 取词规则 4 条（风格段只从 style-profile 取/画质词分平台/cel 系禁写实词/组装见 prompt-formula） | G-B | 无标注 |
| style-library.md:24-26 | 沉淀路由（回写 style-profile/新风格结构/跨风格发现进 shared） | G-B | 无标注 |
| style-library.md:28-34 | 风格索引扩充（2026-10-30）：style-comic/style-fantasy/style-infinite-flow；朋克家族→style-cyberpunk（赛博/蒸汽/柴油三系） | S | 「（2026-10-30）」；三 skill 目录已核实存在；⚠️ 蒸汽/柴油两系与 style-cyberpunk 内容不符，见 M4 |

## shared/director-styles.md（聚合）

| 位置 | 条目 | 级 | 原标注 |
|---|---|---|---|
| director-styles.md:5-8 | 使用规则 4 条（一剧一主风格禁逐镜换/风格段与主体运镜段分离/具体运镜从词典选/提示词不出现导演人名） | G-B | 无标注 |
| director-styles.md:12-64 | 6 个导演风格条目（维伦纽瓦/韦斯·安德森/新海诚/武侠水墨/皮克斯 3D/赛博朋克），各含视觉/光影/运镜/色彩倾向+可复制风格描述句 | G-B | 无标注（电影风格常识性概括；描述句为自撰模板，无来源标注；缺口 K9） |
| director-styles.md:68-77 | 速查对照表 | G-B | 无标注（衍生） |

## shared/output-formats.md

| 位置 | 条目 | 级 | 原标注 |
|---|---|---|---|
| output-formats.md:3-5 | LOCKED 契约声明；字段名唯一真相源；执行顺序=剧本→素材→分镜 | U | 「【执行顺序 2026-10-30 用户重排】」 |
| output-formats.md:10-17 | 剧本条目字段（集数/时长秒 30–120 自动/场景节拍/人物/看点句号收尾/钩子句号收尾） | U | 契约+用户令语境 |
| output-formats.md:22-27 | 节拍字段（目标/冲突 字段名含斜杠照写/起承转合/钩子） | G-B | 无标注，契约自定 |
| output-formats.md:30 | 约束：单集 1–3 场景/一集一微事件/人物逐人可挂资产 | U | split-methodology 用户供同源 |
| output-formats.md:35-48 | 分镜块字段（镜号/时间片格式 `\d+[–-]\d+ 秒`/六要素/转场交代?/素材映射/提示词代码块 ≤500 字） | G-B | 无标注，契约自定（≤500 字=方言 G-B） |
| output-formats.md:52 | 每镜细节 ≥250 字保底、不限上限 | G-A | 无标注（实源=五道硬闸用户令） |
| output-formats.md:54 | 剧本深度标准：分场叙事每场 300–500 字画面叙事，台词带语气、音效逐场标注、末尾转场备注；只有节拍=提纲打回 | U | 「2026-10-27 用户令，最高优先级——「几行节拍不算剧本」」 |
| output-formats.md:59-95 | assets.json 契约（characters/scenes/props；visual_id=node_+10 位；光影锁定；道具造型锚点跨状态复述一字不差；状态=独立素材、状态变体只准 i2i 禁 t2i） | G-B | 无标注（契约自定；i2i 变体有 lessons 实证成分） |
| output-formats.md:98 | 约束：纯空镜/同场景共用资产/每镜按素材映射挂参 | G-A | 无标注（实源=五道硬闸 G4 用户令） |
| output-formats.md:103-119 | 检查报告契约（价格闸/剧情校验/素材校验字段） | G-B | 无标注，契约自定 |
| output-formats.md:122 | 三闸全过才准出片 | S | 实战语境 |

## shared/manhua-production-standard.md

全文件头「行业流水线提炼 · 2026-10-28 用户供」→ 主体 U。逐节：

| 位置 | 条目 | 级 | 原标注 |
|---|---|---|---|
| manhua:3 | 主形态=抖音/快手静态漫画翻页漫剧；核心=资产复用 | U | 「2026-10-28 用户供」 |
| manhua:7-10 | 行业流水线全景 8 步 | U | 同上 |
| manhua:14 | 画幅定版 16:9（竖版致素材生成不全） | U | 「2026-10-28 用户终定」 |
| manhua:15 | 单集 60–90 秒、3–8 镜（参考区间） | U（数字无外部出处） | 「用户供」 |
| manhua:16 | 名条点位策划层标记，非剪辑时临时判断 | U | 同上 |
| manhua:17 | 风格定版三统一（画风/色调/光影规则） | U | 同上 |
| manhua:21 | 剧本=镜头剧本五字段 | U | 同上 |
| manhua:27-33 | 人设卡工艺（外貌固定设定逐项/固定穿搭套装/标志性特征/表情库 6–8 种/三角度参考/禁止项/角色色卡） | U（6–8 种等参数无外部出处） | 同上 |
| manhua:36-39 | 资产库分层复用（表情拆分/配饰图层/分层=不崩脸真正原因） | U | 同上 |
| manhua:42 | 出场规范：配角龙套一般不加名片 | U | 同上 |
| manhua:48-56 | 场景工艺（设定卡/固定物件清单/天气版本/分层前景模糊/常驻复用） | U | 同上（⚠️ L49「竖版 9:16 机位参考」与 16:9 终定矛盾，见 M1） |
| manhua:60-62 | 分镜标注规范（景别运镜转场词/名条点位继承出场表） | U | 同上 |
| manhua:66 | 出图后必须修图（AI 一次全稳不可能） | U | 同上 |
| manhua:71-80 | 后期七条（名条/缩放 0.8–1.5 倍极慢、单镜 2–4 秒/气泡统一样式/音效三分层+不盖台词/整片一个 LUT/转场硬切与闪白黑场） | U（0.8–1.5、2–4s 等参数无外部出处） | 同上 |
| manhua:84 | 审片三级自查（脸/道具穿帮/名片一次/声画同步/版权合规防限流） | U | 同上 |
| manhua:88 | 交互式 AVG 支线（Renpy/NVL/橙光） | U | 同上 |
| manhua:92-94 | 成本核心（20 集剧 5–8 场景 3–6 角色）+常见坑 4 条 | U | 同上 |

## shared/pre-gen-research.md

| 位置 | 条目 | 级 | 原标注 |
|---|---|---|---|
| pre-gen-research.md:3 | 出图前置调研=固定工序（检索→对齐→出指令→沉淀，四步缺一禁出图） | U | 「用户 2026-10-27 强调的固定工序」 |
| pre-gen-research.md:9-11 | 何时做（每批次前/换风格模型重调/重制先查对策） | U | 同上 |
| pre-gen-research.md:15-24 | 检索关键词三轴（风格×资产类型×问题域）×中英双语；每轮覆盖出图要点/提示词写法/翻车点；无资料标「推测」 | U | 同上 |
| pre-gen-research.md:28-36 | 六核心要素对齐清单（主体/三视图/表情/多套服装/风格质感/跨镜一致性） | U | 同上 |
| pre-gen-research.md:37 | 调研不得带偏硬闸（禁废话词/广告闸/情绪可视化） | S | 引 hard-gates |
| pre-gen-research.md:42 | 「10 个针对性词 > 50 词堆砌」 | G-B | 无标注，数量断言无出处（与调研报告负面词策略同向但数字未见） |
| pre-gen-research.md:43 | 出图后按 character/scene-asset-system 验收清单核对；翻车按「停→定位→最小修改重跑」 | G-B | 无标注 |
| pre-gen-research.md:47-50 | 沉淀规则（追加不复述/新实测>旧结论/与硬闸冲突以硬闸为准/未沉淀=工序未完成） | U | 同上 |

## shared/lessons.md（按小节主题）

| 位置 | 主题 | 级 | 原标注 |
|---|---|---|---|
| lessons 1（:7-9） | i2i 锚构图：垫图锚死视角景别，三视图用 t2i、i2i 挂主体+构图硬锁 | S | 「教训/解法」无日期 |
| lessons 2（:11-14） | 显老词：13 词黑名单（御姐/苹果肌饱满/法令纹眼袋等） | S | 教训（18 岁女主画成大妈） |
| lessons 3（:16-19） | 服装漂移：卫衣漂成裙装；服装三视图 i2i 挂主体+逐件写死 | S | 「实测卫衣漂成裙装」 |
| lessons 4（:21-24） | 表情抄外貌：每格只写表情解剖 25–40 字（「表情有效信息仅 2%」⚠️ D3） | S | 教训，数字无出处 |
| lessons 5（:26-29） | video ref 塌缩：m2v 挂 video ref 整集塌缩（002 犯过 7 镜链式重复）；接戏用 first_last_frame | S | 事故实证 |
| lessons 6（:31-34） | quote≠run：24 vs ≥56/镜 | S | 「实测案例」 |
| lessons 7（:36-39） | submission 验真：只认提交后新 resource | S | 事故教训 |
| lessons 8（:41-44） | 转场裸切打回：时间+地点+过渡句 | S | 事故教训 |
| lessons 9（:46-49） | 广告植入三层禁+brand_scan | S | 事故教训 |
| lessons 10（:53-56） | 指令压缩/拼装打回：SHA-256 逐字搬运 | S | 事故教训 |
| lessons 11（:58-61） | Q 版 i2i 锚排版：显式禁多视图/宫格/引线 | S | 事故教训 |
| lessons 12（:63-66） | 表情 6 字碎片：每格 25–40 字写满写差异 | S | 事故教训 |
| lessons 13（:68-71） | 双人镜漏挂对手：逐人挂资产+场景必挂 | S | 事故教训 |
| lessons 行业坑（:73-78） | 人设卡先行/光影四件套锁定/名片恰好一次/音效三分层 | U | 「2026-10-28 用户供」 |
| lessons Notion 接口坑（:80-91） | page_ids/user_confirmed/批量≤10/配额 60min/分页静默漏行 COUNT 复核/view 免配额 | S | 「2026-10-28 实测」 |
| lessons xyq 出图（:93-99） | i2i 排版锚定/画框锁/t2i 显式排版锁一次过/query-result 多行 JSON/6 积分·张 | S | 「2026-10-28 实测」 |
| lessons 品牌语境（:101-104） | 品牌词表误伤普通义/品类词，语境三档处理 | S | 「2026-10-28 剧本机检」 |
| lessons 微恐审核（:106-110） | 惊悚组合被平台拦截（连试 4 次全拦）；中性化词表 | S+U | 「2026-10-28 xyq 倒吊影被拦实测」+「模型纪律（2026-10-28 用户定）」 |
| lessons Notion 建行（:113-117） | parent 顶层参数/状态选项缺失 400/两表状态口径/SSL 重试壳 8×10s | S | 「2026-10-29 实测」 |
| lessons 画布纪律（:119-123） | 临时节点用后即删/删除三步 stderr 取 updateId/批量 target_not_found | S+U | 「2026-10-29 用户发火实测」 |
| lessons G-PARITY（:125-129） | Notion 往返归一化（<br />转义）双向机械还原；--emit-prompt 唯一合法来源 | S | 「2026-10-29 G-PARITY 实测」 |
| lessons 硬闸工具（:131-135） | shot_gate.py 五闸/asset_registry/G-REFBIND 正则 `[^\s。：:]{1,3}`（`[全中近大特]+` 实测翻车） | S | 「2026-10-29 五律落地」+实测 |
| lessons 改 skill 前四步（:137-141） | 记忆摘要不当指令/先读遍机制/先调研/出方案过目才动文件；禁编造剧名示例 | U | 「2026-10-31 用户纠正」 |

---

# 二、各级别计数

（共 283 条；含聚合条目按 1 条计；混合行计入主级别，次级别在备注列写明）

| 级 | 条数 | 占比（约） |
|----|------|-----------|
| U（用户令，有标注） | 67（另 3 条 U+S/S+U 混合：hard-gates:112 五律背景、lessons 微恐、lessons 画布纪律） | 25% |
| S（自测实证/内部决策） | 78 | 28% |
| C（外部调研，有出处） | 5（backends:24 的 --seed 断言为 O-间接——经调研报告引 Midjourney 官方 Seeds 文档，全库唯一接近 O 级） | 2% |
| O（外部官方，直接标注） | 0 | 0% |
| G（无标注） | 130（G-A 漏标可补 19；G-B 无源可考 111） | 46% |

按文件看 G 密度：camera-dictionary（全 G）、lighting-system（全 G）、director-styles（全 G）、video-consistency（15 条中 14 条 G）、production-workflow（9 条中 8 条 G）是重灾区；hard-gates/backends/lessons 的实证链最扎实。

---

# 三、缺口清单

## G 级全部条目

### G-A：漏标可补（实源可考，补日期/出处标注即可，19 条）

1. shot-qa/SKILL.md:46、three-gates.md:69、output-formats.md:52 —— 每镜 ≥250 字（实源：CLAUDE.md 五道硬闸 2026-10-19 用户令）
2. shot-qa/SKILL.md:46、three-gates.md:70 —— 看点/钩子句号收尾+镜内落点（同上，G3 剧情核验）
3. shot-qa/SKILL.md:51、three-gates.md:87-88、output-formats.md:98 —— 场景纯空镜/ref 格式（同上，G4 场景纯净；格式=output-formats 契约）
4. shot-qa/SKILL.md:55、hard-gates.md:35-37 —— Notion 状态=生成中（实源：CLAUDE.md 工作流规则 2026-10-18 + 五道硬闸 G5）
5. shot-qa/SKILL.md:81 —— 五道硬闸 G1–G5 引用（实源同 1）
6. trust-audit.md:12、14、16 —— T2 禁词表/T4 三要素/T6 五要素（应随 2026-10-29 用户令框架一并标）
7. clip-review/SKILL.md:15、20 —— 回流禁擅改/崩坏镜单独重生成（实源：lessons 改 skill 前四步 2026-10-31、hard-gates §5）
8. video-producer/SKILL.md:35 —— 单镜一动作（实源：hard-gates §8）
9. video-consistency.md:11、12 —— 光影四件套逐镜复制/双保险铁律（实源：prompt-formula §四、五律 3 用户令）

### G-B：无源可考（需调研或补实测，111 条，按主题聚类如下）

**K1 短剧 QA/成片核验方法论**
- clip-review 核验体系：五项清单（checklist.md:6-11）、归因矩阵（defect-attribution.md:5-12）、抽帧法（checklist.md:3）——有事故实证但**方法本身**（为什么是这五项、为什么首中尾+接触区）无外部方法论对照
- trust-audit 六维阈值：叙事 35%/25%、相似度 65%/80%、≥3 处污染（trust-audit.md:11、13、15）——无任何实证/来源
- clip-review/SKILL.md:18-19（一次翻车=一条新规、禁积分试错）——纪律无出处

**K2 剪辑节奏与后期方法**
- video-producer/SKILL.md:24 收口工艺包参数、production-workflow.md:42-45 后期收口、manhua:71-80 的 0.8–1.5 倍缩放/2–4 秒单镜/音效三分层/一个 LUT——「用户供」了总纲，但这些具体数值无行业资料对照
- production-workflow.md:49-53 三路线推荐、65-72 翻车清单 7 条
- three-gates.md:17 报价单模板、104-122 检查报告模板（模板自定）

**K3 TTS/配音与口型**
- video-consistency.md:36-39（先产音频反锁时长/口型两走法/台词逐字）、video-producer/SKILL.md:37——整块无任何外部出处（配音/TTS/对口型工具的官方能力口径全缺）

**K4 平台审核/违禁词官方规则**
- 废话词表 6 词（shot-qa/SKILL.md:46、three-gates.md:68、hard-gates.md:9）——社区常见说法但零出处
- 微恐中性化词表（lessons:106-110）有单次实测，但缺平台内容审核**官方规范**对照；「写实真人面部转 3D 防拦截」（hard-gates.md:82）连实测标注都没有
- 品牌扫描机制（hard-gates.md:59-65）缺平台广告合规官方规则
- 后端方言长度/时长上限：即梦 ≤500 字/≤15s/9 图（backends.md:16）、可灵 ≤800 字/≤10s（:17）、海螺 ≤600 字/≤10s（:18）——即梦应有官方参数文档，可灵/海螺自认「按其文档校准」=未校准
- camera-dictionary「安全词」全表（camera-dictionary.md:4-138）——缺 Seedance/即梦官方运镜词表对照

**K5 即梦/小云雀成本与限流官方口径**
- 计价矩阵（backends.md:28-38）全部是 node quote 实测，无官方价目表；小云雀 6 积分/张（backends.md:19、lessons:99）同
- split-methodology 字数换算 200–400 字/分钟、名台词 ≤20 字（split-methodology.md:9、30）；manhua 60–90 秒 3–8 镜——微短剧行业数据明显可查
- 30% 重生成余量、每镜 2 版（video-producer/SKILL.md:23、video-consistency.md:45）

**K6 可灵/Runway 等对照**
- backends.md:17、20（可灵/Midjourney 行）、production-workflow.md:49 表中的 Runway/Pika——只有名字，无能力对照数据

**K7 生图一致性方法论**
- prompt-formula.md:24「顺序即权重」、:31-39 两层控制模板与「行业标准做法」、:48-58 景别表
- video-consistency.md:7-12（ID 命名/参考图 ≤1+1/两层资产分工/合成卡）、:16-25 锁句模板与负面黑名单
- video-producer/SKILL.md:20、production-workflow.md:5-7（LoRA/IP-Adapter「强一档/天花板」效果断言）
- t2i/i2i 选择表（prompt-formula.md:73-82）——有 lessons 实证可补标，但规则整体无外部对照

**K8 光影/摄影参数**
- lighting-system.md 全部（三层语法/1 主光/2–3 句/六情绪配方色温与百分比）——摄影布光资料明显存在
- camera-dictionary.md:6-10 运镜使用规则、:99-100 倾斜角度数

**K9 导演风格库**
- director-styles.md 6 风格条目与速查表——电影风格研究资料明显存在，风格描述句全为自撰

**K10 编剧技法**
- script-craft.md:37-43 叙事技法 7 条、:63 阈值、:67-69 题材质感——编剧/短剧创作方法论资料明显存在

**K11 其余流程规则**
- 花钱门三步/超账单重批/批准话术（hard-gates.md:22-31、three-gates.md:21-28、shot-qa/SKILL.md:61-64）
- 执行顺序总览「先检查再花钱」（hard-gates.md:94-110）
- 留存三主轴（hard-gates.md:88-90）；通用核心七件套（backends.md:8-10）
- prompt-formula.md:66-71（砍词顺序/光影四件套/构图锁）；pre-gen-research.md:42「10>50 词」
- style-library.md:13、17-26；output-formats.md 节拍字段/assets 契约细节

## S 级中「外部资料明显存在但我们没查过」的主题

1. **短剧 QA/成片核验方法论**——clip-review 五项核验、信任度审计阈值全靠自测事故倒推（K1）
2. **剪辑节奏与后期方法**——缩放倍率/单镜秒数/音效分层有「用户供」总纲但无行业教程对照（K2）
3. **TTS/配音与口型**——整块空白（K3）
4. **平台审核/违禁词官方规则**——拦截实测有了（lessons 微恐），官方审核规范没查（K4）
5. **运镜词官方全表**——Seedance/即梦官方提示词指南应含运镜词表（K4）
6. **即梦/小云雀成本与限流官方口径**——计价限流全靠 node quote 实测（K5）
7. **可灵/Runway 对照**——方言表里的「量级」自估（K6）
8. **情绪光影色温配方**——摄影布光标准资料（K8）
9. **短剧字数/节奏换算**（200–400 字/分钟、开头 5 秒抓人）——微短剧行业报告（K5）
10. **LoRA/IP-Adapter 角色一致性效果**——社区实测/论文资料（K7）
11. **显老词黑名单/表情 25–40 字**等参数——美妆/表演/人设资料（lessons 2/12）
12. **广告植入与品牌规避**——平台广告合规规则（K4）

---

# 四、疑似杜撰清单

| # | 位置 | 内容 | 疑点 |
|---|------|---|------|
| D1 | camera-dictionary.md:4、10 | 「全部条目均为安全词（safe），可直接复制进提示词」「生僻词会引发画面畸变、主体漂移、构图塌缩」 | 绝对化断言零实证；且与自家其他文件冲突——video-consistency「禁高速环绕、大幅度摇镜（人脸必漂）」，词典却把「环绕」「剧烈手持」「急速变焦」全标 safe（仅口头「慎用」）。「safe」标记体系像模仿安全词库的包装，实测对照不存在 |
| D2 | lighting-system.md:57-127 | 六情绪配方的精确参数：喜「暗部占比 <15%」、悬疑「画面 60% 以上为暗部」、各档色温区间（3200–4200K 等） | 伪精确数字，无任何摄影资料或实测标注；百分比阈值尤其像编造的「专业感」参数。方向性的布光常识可信，具体数值不可背书 |
| D3 | lessons.md:24 | 「表情有效信息仅 2%」 | 伪精确统计数字，无统计口径、无来源，像修辞包装成数据 |
| D4 | trust-audit.md:11、13、15 | 叙事占比 35%/25%、相似度 65%/80%、≥3 处生产元注释判 C | 阈值精确但零实证记录；框架是用户令（2026-10-29），阈值却不知从哪来——用起来像客观标准，实为拍脑袋值 |
| D5 | backends.md:17、18 | 可灵「中文 ≤800 字量级」、海螺「≤600 字量级」 | 写进「后端方言表」冒充参数口径，虽有「按其文档校准」免责，但从未校准的估计值与实测值（即梦计价）同表并列，读者会同等采信 |
| D6 | production-workflow.md:7、video-producer/SKILL.md:20 | LoRA/IP-Adapter「角色稳定性的天花板」「比纯传参考图强一档」 | 效果排名断言，无对照实验、无外部来源；「天花板」式措辞是营销语言不是实测结论 |
| D7 | prompt-formula.md:39 | 「两层配合 = 跨镜同人的行业标准做法」 | 「行业标准」自封，无标准文件/行业资料佐证（做法本身与调研报告的官方思路接近，问题在包装措辞） |

# 五、附：审计中发现的口径矛盾（顺手记录，非来源问题）

| # | 位置 | 矛盾 |
|---|------|------|
| M1 | manhua-production-standard.md:49 vs :14 | 场景工艺写「构图参考：**竖版 9:16** 机位参考」，与「画幅定版（2026-10-28 用户终定）：统一 16:9」直接冲突——行业原文未消化干净 |
| M2 | hard-gates.md:69-74 vs shot-qa/SKILL.md:44 | 转场交代口径不一：hard-gates=「两件（时空交代+过渡句）」，shot-qa/three-gates=「三件套（时间+地点+过渡句）」 |
| M3 | script-standard.md:50、52 | 标题写「内核五问」，实列 7 条 |
| M4 | style-library.md:34 | 「朋克家族→style-cyberpunk（赛博/蒸汽/柴油三系）」，但 style-cyberpunk 只覆盖赛博朋克；蒸汽/柴油无对应风格段 |
| M5 | first-appearance-nametag.md:26-34、backends.md:34、script-craft.md:26 | 剧内角色名表（角色甲等）、《实测项目A》计费、「角色丙」台词样例写进 skill/shared 正文——与 lessons:141「剧内数据住 assets.json/Notion，skill 只住跨剧可沉淀的方法」（2026-10-31 用户纠正）冲突 |
| M6 | video-consistency.md:36 | 引用 `shot-timing.md` 无路径（实际在 storyboard-director/references/）；`../character-studio/references/character-prompts.md` 等跨 skill 相对路径依赖调用方 cwd |

# 六、结论摘要

- 三条主线（花钱门/零压缩/验真/五律）证据链最硬：用户令（U）+事故实证（S）双背书，核心闸门口径可信。
- 主要风险集中在**「参数型知识」**：运镜安全词表、光影色温配方、信任度阈值、后期倍率、参考图用量上限——全部无来源、无实测标注，是本套件里最像「编出来的专业感」的部分（G-B + 疑似杜撰 D1/D2/D4）。
- 46% 条目（130/283）无标注，其中 19 条是**漏标可补**（用户令散落在 CLAUDE.md 五道硬闸/工作流规则里没引回来），补一轮标注即可显著提升可审计性；其余 111 条需调研或补实测。
- 建议优先补证顺序：K4（官方参数/审核规则）→ K1（QA 方法论阈值）→ K5（成本官方口径）→ K8（光影/运镜参数），其余用「标注推测 + 待实测」处理（pre-gen-research.md:24 本来就规定了「找不到资料标推测」，但这批文件没执行）。
