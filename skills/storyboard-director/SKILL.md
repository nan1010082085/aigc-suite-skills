---
name: storyboard-director
description: 虚拟导演——剧本改编为可出片分镜/出视频锁版。红线：禁止压缩；锁版须写满调度机位运镜动作声音对话；prompt_selfcheck≥1000中文字且含机位运镜锚否则禁止出片。
---

# storyboard-director（虚拟导演）

## 红线（先读·违反即停｜2026-11-24）

全文命令式见 `shared/red-lines.md`。本 skill 落地三条：

1. **禁止压缩** skill 产出；不得交情节提纲让生成模型自由发挥。
2. 每条出视频锁版必须写满：**调度 · 机位 · 运镜/固定 · 动作链 · 声音 · 对话**。
3. 交付锁版后**立刻**跑  
   `python3 tools/prompt_selfcheck.py --mode video [--duration N] <锁版>`  
   exit≠0 = **未完成**，禁止交给 video-producer / 禁止报价。①≥**1000** 中文字；⑧六类写作锚可检出。

## 职责

剧本 → 分镜指令 →（后置）导演出片。**改编，不是照抄**：取尽+补完+扩写成可拍画面。  
总序：剧情 > 素材 > 导演出片（`shared/production-priority.md`）。

**专章**：
- `director-natural-language.md` — 出视频正文写法
- `director-camera-craft.md` — 调度→机位→推进→覆盖→避坑
- `fight-action-boarding.md` / `director-audio-visual.md` / `still-preview-and-dsl-entry.md`
- `live-action-instruction-spec.md` — 真人多镜时间码变体

画幅默认 **16:9**。

## 出视频写法

先调度人物与轴线，再写机位（侧/高/过肩哪侧肩），再写动或明示固定，再写硬切与入点。景别·机位·运镜·切换独立织入时间线——禁五段公文硬绑、禁构图占比工程段。

可保留块：【基础设定】【氛围】【导演时间线】【声音】。缺运镜（或未写锁定）或缺切换/入点 = 不合格。

## 工作流

剧本拆解→导演策略→镜头拆分表→逐镜锁版（过红线机检）→素材映射→人检。

静帧预演入口见 `still-preview-and-dsl-entry.md`。打斗先过 `fight-action-boarding.md`。

## 硬要求（用户原话）

- 薄=打回；观感须强于剧本原文
- 每集背景介绍+开场引入
- 首登场全身亮相；双主体轮廓分离；位移写死谁动/方向（默认同速跟拍）
- 禁：参考图文字描述/括号标注/标签句/名条入画/文学修辞
- 台词唯一出处；声音绑动作
- 道具材质/颜色/结构无歧义
- 模型不锁；方言见 `shared/backends.md`
