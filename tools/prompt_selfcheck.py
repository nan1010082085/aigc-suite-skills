"""prompt_selfcheck —— 提示词 5 项机检（storyboard-director 自检闸）。

检查项：
① 中文提示词长度双轨（mode 区分，2026-10-31 用户批）：
   - image（出图 prompt）≤300 字（火山官方，2026-10-31 批2 报告：超长易忽略细节/缺元素）
   - video（出视频分镜 prompt）[250, 500] 字（≥250=每镜保底用户令；≤500=现口径，
     ⚠ 待核（批1 调研校准）；超上限回 Notion 设计变更，禁删改压缩）
② 时间片格式：至少一处「\\d+[–-]\\d+ ?秒」（如 0–3 秒）
③ 违禁废话词：4K / 8K / 杰作 / 超清晰 / 大师作 / wallpaper（拉丁词忽略大小写）
④ 裸英文运镜词：pan / zoom / dolly / tilt / crane / tracking shot 以独立词形态
   出现即报（ASCII 字母数字边界，中英无空格混排同样命中；panorama/company 等不误报；
   中文提示词只写中文运镜名，英文运镜词必须中译；词表见 shared/camera-dictionary.md）
⑤ 素材映射 refs 数量 ≤9

用法：
- 函数：prompt_selfcheck.check(prompt: str, refs: list[str], mode: str = "video") -> list[str]
  （mode：video=出视频分镜 prompt（默认）/ image=出图 prompt；返回问题清单，空 = 通过）
- 命令行：python3 tools/prompt_selfcheck.py [--mode image|video] <prompt_file> [ref ...]
  问题非空则 exit 1。

仅用 stdlib。
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path
from typing import Dict, List

MIN_PROMPT_CHARS = 250  # 每镜 ≥250 字保底（五道硬闸 1 用户令；出视频分镜适用）
MAX_PROMPT_CHARS_BY_MODE: Dict[str, int] = {
    "image": 300,  # 火山官方（2026-10-31 批2 报告 H1）：中文 ≤300 字防元素缺失
    "video": 500,  # 现口径（backends.md 即梦方言 ≤500 字）；⚠ 待核（批1 调研校准）
}
TIME_SLICE_PATTERN = re.compile(r"\d+[–-]\d+ ?秒")
BANNED_WORDS = ["4K", "8K", "杰作", "超清晰", "大师作", "wallpaper"]
BARE_ENGLISH_CAMERA_WORDS = ["pan", "zoom", "dolly", "tilt", "crane"]
BARE_ENGLISH_CAMERA_PHRASES = ["tracking shot"]
MAX_REFS = 9


def _prompt_length(text: str) -> int:
    """提示词长度：中文字符（CJK 表意文字）+ 标点，其余不计。"""
    count = 0
    for ch in text:
        if "一" <= ch <= "鿿" or "㐀" <= ch <= "䶿":
            count += 1
        elif unicodedata.category(ch).startswith("P"):
            count += 1
    return count


def check(prompt: str, refs: List[str], mode: str = "video") -> List[str]:
    """5 项机检，返回问题清单（空 = 通过）。mode：video（默认）/ image。"""
    if mode not in MAX_PROMPT_CHARS_BY_MODE:
        raise ValueError(f"mode 仅支持 {sorted(MAX_PROMPT_CHARS_BY_MODE)}，收到 {mode!r}")
    problems: List[str] = []

    # ① 长度双轨：image ≤300 / video [250, 500] 中文字符（mode 区分）
    max_chars = MAX_PROMPT_CHARS_BY_MODE[mode]
    length = _prompt_length(prompt)
    if length > max_chars:
        if mode == "image":
            problems.append(
                f"① 图像提示词超过 {max_chars} 中文字符（当前 {length} 字）——火山官方：超长易忽略细节、缺元素"
            )
        else:
            problems.append(
                f"① 提示词超过 {max_chars} 中文字符（当前 {length} 字）——回 Notion 设计变更，禁止删改压缩"
            )
    if mode == "video" and length < MIN_PROMPT_CHARS:
        problems.append(f"① 提示词不足 {MIN_PROMPT_CHARS} 中文字符（当前 {length} 字）——补细节")

    # ② 时间片格式
    if not TIME_SLICE_PATTERN.search(prompt):
        problems.append("② 时间片格式缺失：至少一处「数字–数字 秒」（如 0–3 秒）")

    # ③ 违禁词（拉丁词忽略大小写）
    lowered = prompt.lower()
    for word in BANNED_WORDS:
        if word.lower() in lowered:
            problems.append(f"③ 含违禁废话词「{word}」，改用物理材质词描述质感")

    # ④ 裸英文运镜词（不区分大小写；英文运镜词必须中译）
    # 边界用 ASCII 字母数字界定（不用 \b——Python \w 含 CJK，中英无空格混排时
    # 汉字与英文之间没有 word boundary，会漏检「用zoom推近」这类最常见形态）
    bare_hits: List[str] = []
    for word in BARE_ENGLISH_CAMERA_WORDS:
        if re.search(rf"(?<![A-Za-z0-9]){word}(?![A-Za-z0-9])", lowered):
            bare_hits.append(word)
    for phrase in BARE_ENGLISH_CAMERA_PHRASES:
        if re.search(rf"(?<![A-Za-z0-9]){phrase}(?![A-Za-z0-9])", lowered):
            bare_hits.append(phrase)
    if bare_hits:
        problems.append(
            f"④ 裸英文运镜词未中译：{'、'.join(bare_hits)}"
            "（改用 shared/camera-dictionary.md 的中文运镜名）"
        )

    # ⑤ refs 数量 ≤9
    if len(refs) > MAX_REFS:
        problems.append(f"⑤ 素材映射 refs 超过 {MAX_REFS} 个（当前 {len(refs)}）")

    return problems


def main(argv: List[str]) -> int:
    args = argv[1:]
    mode = "video"
    if args and args[0] == "--mode":
        if len(args) < 2:
            print("用法: python3 tools/prompt_selfcheck.py [--mode image|video] <prompt_file> [ref ...]", file=sys.stderr)
            return 2
        mode = args[1]
        args = args[2:]
    if not args:
        print("用法: python3 tools/prompt_selfcheck.py [--mode image|video] <prompt_file> [ref ...]", file=sys.stderr)
        return 2
    prompt = Path(args[0]).read_text(encoding="utf-8").strip()
    try:
        problems = check(prompt, args[1:], mode=mode)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    for problem in problems:
        print(problem)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
