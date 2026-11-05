#!/bin/sh
# skill → 指令 全指令验证：七份指令逐份过合规闸，全过=退出码 0
# 不调生成后端、不烧积分——只验证「skills 出指令」链路
cd "$(dirname "$0")" || exit 2
SC="../../tools/prompt_selfcheck.py"
fail=0
check() {
  label="$1"; shift
  if python3 "$SC" "$@" > /tmp/skill-smoke.out 2>&1; then
    echo "PASS  $label"
  else
    echo "FAIL  $label"; sed 's/^/      /' /tmp/skill-smoke.out; fail=1
  fi
}
check "A1 人物指令    character-studio        image" --mode image sample-character-instruction.md
check "A2 场景指令    scene-studio            image" --mode image sample-scene-instruction.md
check "A3 道具指令    prop-studio             image" --mode image sample-prop-instruction.md
check "A4 分镜指令    storyboard-director     video" --mode video --duration 8 sample-storyboard-instruction.md
check "A5 出视频指令  live-action-instruction video" --mode video --duration 8 sample-video-instruction.md
check "B4 分镜指令    storyboard-director     video" --mode video --duration 6 sample-b-storyboard-instruction.md
check "B5 出视频指令  live-action-instruction video" --mode video --duration 6 sample-b-video-instruction.md
[ "$fail" = 0 ] && echo "全指令验证 PASS（7/7）"
exit $fail
