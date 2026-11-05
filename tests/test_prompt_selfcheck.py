"""prompt_selfcheck 提示词合规闸测试（6 项机检——只拦合规风险，不拦创作发挥）。"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import prompt_selfcheck  # noqa: E402

# 合格样例：中文、含时间片、无违禁词、无裸英文运镜、refs 少、≥250 字（每镜保底）
GOOD_PROMPT = (
    "0–3 秒：都市雨夜街道，女主林晚（18 岁，黑色长直发，米色风衣）站在霓虹灯下，"
    "泪水滑落、嘴唇微颤，双手攥紧衣角。夜色深蓝底调，主光为街灯暖光侧打，"
    "低对比低调影调冷蓝阴影。缓推近景，雨声与远处车流声。"
    "3–8 秒：她抬手抹去泪水，深吸一口气，缓缓抬头看向写字楼顶层，"
    "眼神由悲伤转为坚定，冷蓝逆光勾勒轮廓，缓移跟拍，雨水顺风衣下摆滴落，"
    "指尖松开衣角改攥拳，呼吸由浅转深，雨声渐弱，远处车流一层底噪压住呼吸声。"
    "8–12 秒：她松开攥拳的右手，掌心向上接住雨滴，随后转身走向写字楼大门，"
    "背影没入门廊暖光，风衣下摆带起一排水雾，固定机位目送，环境声只剩檐下滴水。"
)


def test_video_no_upper_limit():
    # 2026-11-05 用户令：废除字数上限红线（苗疆合集实证 seedance_2.5 出片 917–1288 字）
    prompt = ("她泪水滑落、嘴唇微颤，攥紧衣角。" * 60) + "0–3 秒：缓推近景，雨声。"
    problems = prompt_selfcheck.check(prompt, [], mode="video")
    assert problems == [], f"视频 prompt 无字数上限，长 prompt 不得报长度问题: {problems}"


def test_image_no_upper_limit():
    # 同令废除出图字数上限；上限属后端方言（backends.md），不做红线
    prompt = ("她泪水滑落、嘴唇微颤，攥紧衣角。" * 30) + "0–3 秒：缓推近景，雨声。"
    problems = prompt_selfcheck.check(prompt, [], mode="image")
    assert not any("字" in p and "①" in p for p in problems), f"图像 prompt 不得报字数上限: {problems}"


def test_invalid_mode_rejected():
    try:
        prompt_selfcheck.check(GOOD_PROMPT, [], mode="gif")
    except ValueError:
        return
    raise AssertionError("非法 mode 必须抛 ValueError")


def test_banned_word():
    prompt = "0–3 秒：女主站在街头抬头，缓推近景，8K 超清晰画质，雨声。"
    problems = prompt_selfcheck.check(prompt, [])
    assert any("违禁" in p for p in problems), f"违禁词必须报: {problems}"


def test_bare_english_camera():
    prompt = "0–3 秒：女主站在街头抬头望向天台，zoom 推近，雨声。"
    problems = prompt_selfcheck.check(prompt, [])
    assert any("运镜" in p for p in problems), f"裸英文运镜词必须报: {problems}"


def test_bare_english_camera_no_space():
    # 中文与英文无空格混排（中文行文常态）不得漏检
    for prompt in (
        "0–3 秒：女主站在街头抬头望向天台，用zoom推近，雨声。",
        "0–3 秒：女主站在街头抬头望向天台，缓zoom推近，雨声。",
    ):
        problems = prompt_selfcheck.check(prompt, [])
        assert any("运镜" in p for p in problems), f"无空格混排裸英文运镜词必须报: {prompt} -> {problems}"


def test_missing_time_slice():
    # 多镜指令（含镜号标记）缺时间码必须报
    problems = prompt_selfcheck.check("镜头1：女主抬头看向天台。镜头2：她转身离开，缓推近景，雨声。", [])
    assert any("时间片" in p for p in problems), f"多镜缺时间码必须报: {problems}"


def test_free_form_single_shot_exempt_from_timecode():
    # 无镜号自由段落单镜写法（样本实证变体）豁免时间码检查
    prompt = (
        "手持（镜头晃动）近景：浓烟滚滚从舞台侧门涌出，少女抱着教案退到墙根，"
        "睫毛沾灰、呼吸急促，暗红裙摆在烟里晃，远处火光映亮半边脸，衣料窸窣、咳嗽声压着喊声。"
    )
    problems = prompt_selfcheck.check(prompt, [])
    assert not any("时间片" in p for p in problems), f"单镜自由段不得报时间码缺失: {problems}"


def test_too_many_refs():
    refs = [f"node_ref{i:02d}" for i in range(10)]
    problems = prompt_selfcheck.check(GOOD_PROMPT, refs)
    assert any("9" in p for p in problems), f"refs 超 9 个必须报: {problems}"


def test_good_prompt_passes():
    problems = prompt_selfcheck.check(GOOD_PROMPT, ["node_abc123def0"])
    assert problems == [], f"合格样例必须返回 []，实际: {problems}"


def test_duplicate_block():
    # 规格块拼装手误：【光线】重复两次（苗疆样本实证）必须报
    prompt = "【光线】\n阳光从窗户照进来，主光 4600K 暖金色，照亮发丝额角睫毛鼻梁颧骨唇峰。\n【光线】\n阳光从窗户照进来，主光 4600K 暖金色，照亮发丝额角睫毛鼻梁颧骨唇峰。"
    problems = prompt_selfcheck.check(prompt, [])
    assert any("⑥" in p for p in problems), f"重复块必须报: {problems}"


def test_timecode_format_accepted():
    # mm:ss 时间码式（2026-11-05 样本口径）不得报时间片缺失
    prompt = (
        "镜头 1｜01:49.90—01:51.90｜2.00 秒｜教室：少女突然头晕，一只手抬起摸了摸额头，"
        "指尖发白、呼吸变浅，肩上的生物顺着肩线慢慢往脖颈方向爬，动作很慢，她还在硬撑。"
        "镜头 2｜01:51.90—01:53.10｜1.20 秒｜教室：她腿一软开始往后倒，生物仍贴着肩头，"
        "随她后倒身体微倾，衣料摩擦，怀里的表格还抱着，过道光线照亮发丝。"
    )
    problems = prompt_selfcheck.check(prompt, [])
    assert not any("时间片" in p for p in problems), f"时间码式不得报时间片缺失: {problems}"


def test_color_temp_k_not_banned():
    # 色温「4800K」与 node ID 子串（实证 node_5298y8kbk7 曾误触 8K）不得误杀——独立词+字母数字边界匹配
    prompt = GOOD_PROMPT + "头部侧后方 4800K 条形柔光灯勾出轮廓，引用 {{node:node_5298y8kbk7}} 反打画面。"
    problems = prompt_selfcheck.check(prompt, [])
    assert not any("③" in p for p in problems), f"色温/node ID 子串不得误报违禁词: {problems}"


def test_resolution_4k_in_frame_line_ok():
    # 「画幅：16:9，4K」是分辨率声明不是废话词
    prompt = GOOD_PROMPT + "\n**画幅：**\n16:9，4K，电影级真人实拍质感。"
    problems = prompt_selfcheck.check(prompt, [])
    assert not any("4K" in p for p in problems), f"画幅行 4K 不得误报: {problems}"


def test_per_shot_limit_repeat_ok():
    # 「本镜限制」逐镜重复是设计（防漂移），不是拼装手误
    prompt = GOOD_PROMPT + "\n本镜限制：生物巴掌大，在她身上慢慢爬。\n本镜限制：生物巴掌大，在她身上慢慢爬。"
    problems = prompt_selfcheck.check(prompt, [])
    assert not any("⑥" in p for p in problems), f"本镜限制重复不得误报: {problems}"
