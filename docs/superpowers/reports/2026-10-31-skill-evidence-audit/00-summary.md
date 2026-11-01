# skill 证据来源审计·汇总矩阵（2026-10-31）

四路审计合计 822 条硬要求（素材 130 / 编剧分镜 225 / 风格 184 / 质检共享 283）。
分级：U=用户令（不缺料）· O=外部官方有源 · C=外部调研有源 · S=自测孤证 · G=无标注/推测/引用错位。

## 一、总矩阵

| 域 | 条目 | U | O | C | S | G | G 占比 |
|---|---|---|---|---|---|---|---|
| 素材侧（character/scene/prop） | 130 | 54 | 0 | 0 | 22 | 54 | 42% |
| 编剧分镜（idea/novel/storyboard） | 225 | 54 | 1 | 0 | 16 | 154 | **68%** |
| 风格（style-* 九个） | 184 | 20 | 14 | 75 | 12 | 63 | 34% |
| 质检共享（shot-qa/clip-review/video-producer/shared） | 283 | 67 | 0* | 5 | 78 | 130 | 46% |
| **合计** | **822** | **195** | **15** | **80** | **128** | **401** | **49%** |

*qa-shared 域唯一 O-间接：backends.md:24 `--seed` 断言经 2026-10-27 报告引 Midjourney 官方 Seeds 文档。全库外部官方来源仅 15 条（13 条集中在 style-photoreal）。

## 二、三个全库性结论

1. **近半条目（401/822）无来源**；外部来源几乎只覆盖「风格词库 + 图像平台提示词」（10-27 调研落点），编剧方法论/分镜工艺/素材工艺/质检阈值四大域长期零调研。
2. **疑似杜撰合计 32 条**（style 9 / assets 8 / script 8 / qa 7）+ 引用错位 5 处 + 引用不存在文件 1 处。共性：真实做法 + 自造精确参数/绝对化断言/假出处/自我包装。
3. **口径矛盾与污染 10+ 条**：画幅 9:16 残留×2（撞 10-28 用户终定 16:9）、镜长三方矛盾（4–8s vs 1–4s vs 1.5–4s）、时长-质量伪机制撞后端真实 4–30s、转场两件套 vs 三件套、实测项目B/实测项目A剧内数据污染×4（角色甲名条表/信物/角色丙/331章）。

## 三、最硬资产（不缺料，可作基准）

- 出片五律 / 花钱门 / 零压缩 / 验真：U+S 双背书
- 2026-10-27 调研报告：C 级条目抽查全部对得上来源
- MJ `--seed` 官方语义（director-brief/backends）：全库唯一近 O 级
- storyboard-director 硬要求清单（用户令+事故回流双标注）：U=54+S=16

## 四、P0 修复清单（内部矛盾/已证伪/污染——修法明确，不需补料）

| # | 位置 | 问题 | 修法 |
|---|---|---|---|
| 1 | scene-studio/SKILL.md:18、manhua-production-standard L49 | 「竖版 9:16」撞用户终定 16:9 | 改 16:9 或删竖版口径 |
| 2 | character-asset-system.md:30 | 「忽略参考图排版」已被 10-28 xyq 实测证伪 | 删该句，指向画框锁 |
| 3 | camera-dictionary.md | 「全部安全词」绝对化，且与 video-consistency「禁高速环绕/大幅摇镜」矛盾 | 撤绝对化标注，矛盾词降级 |
| 4 | shot-timing.md:3 | 「时长与质量反比」伪机制 +「10s+高风险」撞 backends 4–30s | 改为后端官方时长口径 |
| 5 | shot-timing/director-brief/idea-workflow | 「黄金配比 40/50/10」「⭐星级表」伪精确 | 标【推测】或删数字 |
| 6 | 镜长三方矛盾（selfcheck-7/shot-timing/pacing-templates） | 4–8s / 1–4s / 1.5–4s 至少两处凑数 | 统一为单一口径并标源 |
| 7 | style-fantasy（Greg Rutkowski、D&D）、style-cyberpunk L60（Blade Runner） | IP/商标词+同文件自禁矛盾 | 删 |
| 8 | style-anime/pixar 假出处×3、qa「表情仅2%」、backends 可灵/海螺字数 | 假出处/伪统计/未校准混实测表 | 删或改标【未校准】 |
| 9 | first-appearance-nametag §四/pacing-templates/selfcheck-7/browser-dump | 实测项目B剧内数据污染（角色甲名条表/信物/331章） | 迁出至项目侧，skill 留占位 |
| 10 | video-consistency 引 shot-timing.md 无路径；prop-studio 引 §3.4；director-brief 章节倒置 | 引用坏链/错位 | 修正 |

## 五、补料批次（按审计 G 占比修订优先级）

| 批 | 内容 | 目标域 | 依据 |
|---|---|---|---|
| 1 | 出视频官方补遗：sd2-pe SKILL.md 下载解析、运镜词官方全表、即梦 Web 教程、时长-质量官方口径 | storyboard/video-producer/camera-dictionary | P0-3/4 的正解来源 |
| 2 | 图像侧官方机制：即梦/Seedream 图像官方指南（出图参数/负面词/seed 支持） | character/scene/prop | 素材域 O=C=0 |
| 3 | 编剧市场域：爆款冲突结构/分集节奏/完播率行业报告（DataEye/云合/艺恩/抖音白皮书）+ 编剧教科书通识 | idea/novel-to-drama | **G=68% 最大盲区** |
| 4 | 质检/后期/审核：短剧 QA 方法论、剪辑节奏参数、平台审核违禁词规范、TTS/口型 | shot-qa/clip-review/video-producer | G=46% 且多伪精确参数 |
| 5 | 风格词效实证：Booru 词效对照、边界词社区实证、SSS 材质词效 | style-comic/fantasy/infinite-flow/3d-anime | 四个零来源 skill |

每批纪律不变：搜索 → 标源报告 → 用户过目 → 才入库。
