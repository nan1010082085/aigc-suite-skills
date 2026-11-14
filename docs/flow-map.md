# AIGC Suite Skills 流程总览（单一流程并排 × 串联流程）

> 2026-10-29 增补版（基线 2026-10-27 全量复审）。14 skill = 8 个主链 skill + 6 个风格 skill + 共享底座（shared/ 规则词典 + tools/ 机器闸门）。

## 一、单一流程并排（每个 skill 独立跑起来长什么样）

| Skill | 触发 | 输入 | 单一流程 | 输出 | 下游 |
|-------|------|------|---------|------|------|
| **novel-to-drama** 小说改编 | 小说链接/文本要改编 | 小说 | 抽正文（OCR/直取）→ 拆解（人物/伏笔/名场面/爽点）→ 分集（30–120s 自动、故事单元、禁一章一集）→ 分集剧本（灵活叙事+剧本理解） | 剧本条目（LOCKED） | 剧本 skill 出口 → storyboard/character/scene |
| **idea-to-drama** 想法创作 | 一句话想法要原创 | 想法 | 澄清 ≤2 问 → 搜索同类冲突结构 → logline→多集结构→人物小传 → 分集剧本（想法命中率 100%） | 剧本条目（LOCKED） | 同上 |
| **storyboard-director** 分镜创作 | 有剧本要出分镜/提示词 | 剧本条目 | 导演 Brief 五要素（双帽第一顶）→ 时间轴（时长 40/50/10 配比【推测·未验证】）→ 六要素/四段式提示词 → 7 项自检 | 分镜块（LOCKED）+ 出视频指令 | character/scene（素材映射）、shot-qa |
| **character-studio** 人物出图 | 有人物要出资产 | 剧本人物清单 | 前置调研 → 基础形象设定卡（三视图+表情板+服饰道具特写合一身份锚，A 站姿硬锁，随剧本阶段演进）→ 服装/表情模块（i2i 同机位）→ 验收清单 | assets.json `characters[]/outfits[]` | video-producer（参考图）、shot-qa |
| **scene-studio** 场景出图 | 有场景要出资产 | 剧本场景清单 | 前置调研 → 场景主图（t2i 空镜）→ 镜头变体×光影配套（改正文、贴人五条）→ 光影四件套锁定 | assets.json `scenes[]` | 同上 |
| **prop-studio** 道具出图 | 有道具要出资产 | 剧本道具清单 | 剧本拆解表 → 分类判定（单独出图 vs 场景装饰）→ 透明底分层 + 造型锁定 → 状态变体随剧情演进 + 特写/远景双版 | assets.json `props[]` | 同上 |
| **video-producer** 出视频执行 | 过检后要真出片 | 分镜块 + assets.json | 资产预检 → 单镜隔离生成包 → 试产 2–3 镜锁参 → 批量+素材入库（失败归因）→ 后期统一收口 | 视频素材库 + 成片 | 交付 |
| **shot-qa** 出片检查 | 生成前/后要过闸 | 分镜+素材+计划 | 五道硬闸预检（pre_gen_gate：分镜细节/素材关联/剧情核验/场景纯净/Notion 先行）→ 价格闸（报价→批→跑）→ 剧情校验（逐字/转场/品牌/违禁）→ 素材校验（挂载/格式/验真） | 检查报告（LOCKED） | 放行 → video-producer |
| **style-cg-refined**（主风格） | 剧目风格锁 | — | 取风格锁模板（中英）→ 按后端方言调词 → 翻车点自检 | 风格段文本 | 被四个内容 skill 引用 |
| **style-3d-anime / anime / pixar / cyberpunk / photoreal** | 同上 | — | 同上 | 风格段文本 | 同上 |

## 二、串联流程（全链路，一部剧怎么跑）

```
                     【IP 选择】（用户人工，不做 skill）
                              │
              ┌───────────────┴───────────────┐
              ▼ 小说                            ▼ 想法
     novel-to-drama                    idea-to-drama
     抽正文→拆解→分集→剧本               澄清→搜索→结构→剧本
              └───────────────┬───────────────┘
                              ▼ 剧本条目（LOCKED 字段契约）
        ┌─────────────────────┼─────────────────────┐
        ▼                     │                     ▼
 storyboard-director          │              character-studio
 导演Brief→时间轴→提示词→自检   │              + scene-studio
        │                     │              + prop-studio
        │                     │              设定卡锚点/服装/表情/场景/道具
        │   〔风格段 ← style-* skill（剧目锁 1 种，默认 style-cg-refined）〕
        ▼                     │                     ▼
     分镜块（LOCKED）          │              assets.json（LOCKED）
        └───────────────┬─────┴─────────────┬───────┘
                        ▼                   │
                shot-qa 三道闸+五道硬闸      │
      五道硬闸预检→价格闸→剧情校验→素材校验    │
                        │ 全过放行           │
                        ▼                   ▼
                    video-producer（出视频执行）
       资产预检 → 单镜隔离 → 试产锁参 → 批量入库 → 后期收口
                        │
                        ▼
                      成片交付
        （崩坏镜 → 归因后回对应 skill 修 → 单镜重跑）
```

**横向供给**：style-\* 风格 skill 给 storyboard-director / character-studio / scene-studio / prop-studio / video-producer 供风格段；shared/（硬闸/公式/契约/词典/品牌词/教训）是所有 skill 的底座；tools/（lint/花钱门/品牌扫/提示词自检/OCR/pre_gen_gate/notion 客户端）是机器闸门。

**回路**：shot-qa 打回按层路由——分镜回 storyboard-director、素材回 character/scene/prop-studio、剧本回剧本 skill、生成崩坏回 video-producer（归因四分类：变脸/肢体崩/场景错/服装串）。

## 三、复审结论（2026-10-27）

- **机械层**：lint 12/12 ✓、pytest 25/25 ✓、路径引用 55 处核验（3 处真悬空已修：install.md 的 Codex 路由旧名、两处裸 references/ 路径；plan 历史文档留档不动）
- **契约层**：output-formats 四类 LOCKED 契约（剧本条目/分镜块/assets.json/检查报告）全链逐字引用，零漂移
- **方法论层**：双帽协作（导演 Brief→工程翻译）、分类合成时长（40/50/10【推测·未验证】）、一致性双轴（人不能变×画风不能变）、双保险（@引用+完整描述）、出视频四段式全部入规
- **2026-11-14 更正**：此前“style-photoreal 在即梦链路需转风格化防拦截”缺少官方或实测依据，现不再作为生成规则；风格按项目目标图确定，内容审核按服务端实际结果处理。plans 为历史文档含旧名属正常留档。

## 四、增补记录（2026-10-29）

- **prop-studio 入列**（e62c8bf/c26900d/79417d3）：道具成为与人物、场景并列的独立第三类素材（`assets.json props[]` 契约），透明底分层、造型锁定防穿帮、状态变体随剧情演进；二版方法论含剧本拆解表四类信息、手掌比例基准、刻字不进 AI、试嵌入校验、特写远景双版；调研提炼原画三原则（轮廓优先/功能先于装饰/蓝图属性）+ 三视同轴对齐 + 材质倒角标注
- **style-3d-anime 入列**（ccf9245）：精致 3D 日漫 CG 风格锁（日漫的脸 × 3D 的质感），填补 style-cg-refined 与 style-anime 之间的第三种风格位
- **character-studio 设定卡锚点制**（d24e3a2）：基础形象设定卡=三视图+表情板+服饰道具特写合一，A 站姿硬锁，设定卡=角色参考图唯一入口
- **scene-studio 镜头变体纪律**（ccf9245/9b6ceb3）：镜头变体×光影配套×贴人五条；变体必须改正文（前缀无效实测）；微恐描述审核中性化词表
- **shot-qa 五道硬闸**：`tools/pre_gen_gate.py` 预检五闸（分镜细节≥250字/素材关联/剧情核验/场景纯净/Notion 先行），任一 FAIL 拒绝生成；生成后端默认 xyq V2.5 Fast
