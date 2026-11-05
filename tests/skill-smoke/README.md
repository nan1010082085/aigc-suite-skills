# skill-smoke —— skill → 指令 全指令验证

目的：验证 **skills 出指令**链路（不调生成后端、不烧积分），且校验**不拦创作**（2026-11-05 用户令：检查=合规，不是限制模型/发挥/创作）。另实证指令**随剧本千变万化**，不是死模板。

## 全指令矩阵（两套不同剧本）

| 文件 | 来源 skill | 剧本 | 模式 | 生成时长 |
|---|---|---|---|---|
| `sample-character-instruction.md` | character-studio（基础形象设定卡·七视图） | A 现代雨夜·情绪戏 | image | — |
| `sample-scene-instruction.md` | scene-studio（空镜+光影锁定） | A 现代雨夜·情绪戏 | image | — |
| `sample-prop-instruction.md` | prop-studio（道具人物名片·传世做旧档） | A 现代雨夜·情绪戏 | image | — |
| `sample-storyboard-instruction.md` | storyboard-director（三大项格式） | A 现代雨夜·情绪戏 | video | 8s |
| `sample-video-instruction.md` | live-action-instruction-spec（多镜单视频） | A 现代雨夜·情绪戏 | video | 8s |
| `sample-b-storyboard-instruction.md` | storyboard-director（三大项格式） | B 古装追逃·动作戏 | video | 6s |
| `sample-b-video-instruction.md` | live-action-instruction-spec（多镜单视频） | B 古装追逃·动作戏 | video | 6s |

两套剧本题材、风格段（写实摄影 / 半写实精致 CG）、镜头结构（静态情绪 / 追逃动作）、时长档（8s / 6s）全不同——产出全不一样，但过**同一套**合规闸。质量保证来自硬要求（每镜≥250 字保底、身份锚写死左右、轮廓分离、时间轴对时±0.5s、逐镜限制防漂移）+ 合规闸，不来自固定内容。

## 运行

```bash
./run.sh
```

预期：7 行 PASS + 「全指令验证 PASS（7/7）」，退出码 0。任一份有问题则输出问题清单并退出码 1。

样本均为通用占位内容（无剧名、无真实资产），节点引用用 `{{node:node_char01}}` 一类占位符。

## 合规闸拦什么 / 不拦什么

- 拦（合规风险）：平台审核违禁词、裸英文运镜（后端不识别）、多镜缺时间码（机器不可读）、refs>9（素材挂载风险）、重复块（拼装手误）、每镜 <250 字（信息量保底）、时间轴不对时（内容被模型压缩/砍=翻车重烧积分）
- 不拦（创作自由）：字数无上限、题材/风格/叙事/镜头语言任意发挥
