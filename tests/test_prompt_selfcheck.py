"""prompt_selfcheck 提示词自检闸测试（5 项机检）。"""

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


def test_over_500_chars_video():
    # 出视频 prompt 上限 500 字（现口径，⚠ 待核（批1 调研校准））
    prompt = ("她泪水滑落、嘴唇微颤，攥紧衣角。" * 32) + "0–3 秒：缓推近景，雨声。"
    problems = prompt_selfcheck.check(prompt, [], mode="video")
    assert any("500" in p for p in problems), f"视频 prompt 超过 500 字必须报长度问题: {problems}"


def test_over_300_chars_image():
    # 出图 prompt 上限 300 字（火山官方，批2 报告）
    prompt = ("她泪水滑落、嘴唇微颤，攥紧衣角。" * 20) + "0–3 秒：缓推近景，雨声。"
    problems = prompt_selfcheck.check(prompt, [], mode="image")
    assert any("300" in p for p in problems), f"图像 prompt 超过 300 字必须报长度问题: {problems}"


def test_thresholds_differ_by_mode():
    # 300–500 字区间：video 过、image 报——双轨生效，不写死单一值
    prompt = ("她泪水滑落、嘴唇微颤，攥紧衣角。" * 20) + "0–3 秒：缓推近景，雨声。"
    problems_video = prompt_selfcheck.check(prompt, [], mode="video")
    assert problems_video == [], f"视频 prompt 300–500 字区间应通过: {problems_video}"
    problems_image = prompt_selfcheck.check(prompt, [], mode="image")
    assert any("300" in p for p in problems_image), f"同长度图像 prompt 必须报: {problems_image}"


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
    problems = prompt_selfcheck.check("女主抬头看向天台，缓推近景，雨声。", [])
    assert any("时间片" in p for p in problems), f"缺时间片格式必须报: {problems}"


def test_too_many_refs():
    refs = [f"node_ref{i:02d}" for i in range(10)]
    problems = prompt_selfcheck.check(GOOD_PROMPT, refs)
    assert any("9" in p for p in problems), f"refs 超 9 个必须报: {problems}"


def test_good_prompt_passes():
    problems = prompt_selfcheck.check(GOOD_PROMPT, ["node_abc123def0"])
    assert problems == [], f"合格样例必须返回 []，实际: {problems}"
