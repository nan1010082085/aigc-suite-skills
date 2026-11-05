#!/bin/sh
# skill 出指令冒烟测试：对样本指令跑合规闸，通过=退出码 0
cd "$(dirname "$0")" || exit 2
exec python3 ../../tools/prompt_selfcheck.py --mode video --duration 8 sample-video-instruction.md
