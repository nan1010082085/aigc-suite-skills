"""brand_scan 广告植入闸测试（三层：画面/语音/字幕）。"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import brand_scan  # noqa: E402


def test_brand_hit_in_dialogue():
    hits = brand_scan.scan_shot(
        "都市街道，女主走在人行道上。",
        "女主旁白：我打开高德地图导航去公司。",
    )
    words = [h["word"] for h in hits]
    assert "高德地图" in words, "台词含「高德地图」必报"
    hit = next(h for h in hits if h["word"] == "高德地图")
    assert hit["layer_guess"] == "语音"


def test_brand_hit_in_visual():
    hits = brand_scan.scan_shot(
        "女主坐在星巴克里喝咖啡，桌上放着笔记本电脑。",
        "女主说：今天天气不错。",
    )
    words = [h["word"] for h in hits]
    assert "星巴克" in words, "画面含「星巴克」必报"
    hit = next(h for h in hits if h["word"] == "星巴克")
    assert hit["layer_guess"] == "画面"


def test_clean_text_empty():
    assert brand_scan.scan_text("女主抬头看向窗外，阳光洒在桌面上。") == []


def test_brand_ambiguous_generic_not_flagged():
    """歧义通用词后接通用后缀字是普通用法：苹果汁/小米粥/百事通不得报。"""
    hits = brand_scan.scan_shot(
        "桌上放着一杯苹果汁和一碗小米粥。",
        "女主说：她是个百事通，什么都知道。",
    )
    words = [h["word"] for h in hits]
    assert "苹果" not in words, "苹果汁是普通用法，不得误伤"
    assert "小米" not in words, "小米粥是普通用法，不得误伤"
    assert "百事" not in words, "百事通是普通用法，不得误伤"


def test_brand_ambiguous_still_flagged():
    """裸歧义通用词（品牌用法）照样命中：台词里的苹果/小米必报。"""
    hits = brand_scan.scan_shot(
        "女主走进数码店。",
        "女主说：我买了苹果和小米。",
    )
    words = [h["word"] for h in hits]
    assert "苹果" in words, "裸「苹果」必报"
    assert "小米" in words, "裸「小米」必报"
