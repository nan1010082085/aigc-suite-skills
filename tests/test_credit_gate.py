"""credit_gate 花钱门测试（可注入 runner，不触达真实 CLI）。"""

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import credit_gate  # noqa: E402


class FakeResult:
    """模拟 subprocess.run 的返回对象。"""

    def __init__(self, returncode=0, stdout=""):
        self.returncode = returncode
        self.stdout = stdout


def test_run_without_approval_raises():
    calls = []

    def fake_executor(cmd, **kwargs):
        calls.append(cmd)
        return FakeResult()

    try:
        credit_gate.run(
            ["dreamina-canvas", "node", "create"], approved_by=None, max_credits=100,
            executor=fake_executor,
        )
    except PermissionError:
        pass
    else:
        raise AssertionError("approved_by=None 必须抛 PermissionError")

    assert calls == [], "未获批准时执行器不得被调用"


def test_run_with_approval_passes_ceiling():
    calls = []

    def fake_executor(cmd, **kwargs):
        calls.append(cmd)
        return FakeResult(returncode=0)

    rc = credit_gate.run(
        ["dreamina-canvas", "node", "create"], approved_by="user:张三", max_credits=80,
        executor=fake_executor,
    )

    assert rc == 0
    assert len(calls) == 1
    cmd = calls[0]
    assert "--credit-ceiling" in cmd, "批准后必须把 credit ceiling 传给执行器"
    idx = cmd.index("--credit-ceiling")
    assert cmd[idx + 1] == "80"


def test_quote_parses_total_and_items():
    payload = (
        '{"data": {"items": [{"name": "图1", "maxCredits": 30},'
        ' {"name": "图2", "maxCredits": 50}], "totalMaxCredits": 80}}'
    )

    def fake_runner(cmd, **kwargs):
        return FakeResult(stdout=payload)

    result = credit_gate.quote(["dreamina-canvas", "node", "quote"], runner=fake_runner)

    assert result["total_max_credits"] == 80
    assert result["items"] == [
        {"name": "图1", "maxCredits": 30},
        {"name": "图2", "maxCredits": 50},
    ]


def test_quote_failure_raises():
    """非零 returncode 的报价必须抛错，禁止静默返回 None 上限。"""

    def fake_runner(cmd, **kwargs):
        return FakeResult(returncode=1, stdout='{"error": "boom"}')

    with pytest.raises(RuntimeError):
        credit_gate.quote(["dreamina-canvas", "node", "quote"], runner=fake_runner)


def test_quote_invalid_total_raises():
    """totalMaxCredits 缺失或非 int 一律抛错，不得产出 None/无效上限。"""

    for bad in ('{"data": {"items": []}}', '{"error": "x"}'):
        def fake_runner(cmd, _bad=bad, **kwargs):
            return FakeResult(returncode=0, stdout=_bad)

        with pytest.raises(ValueError):
            credit_gate.quote(
                ["dreamina-canvas", "node", "quote"], runner=fake_runner
            )


def test_run_strips_preexisting_ceiling():
    """花钱门独占 ceiling：cmd 里预置的 --credit-ceiling 必须被剥离，只留批准值。"""
    calls = []

    def fake_executor(cmd, **kwargs):
        calls.append(cmd)
        return FakeResult(returncode=0)

    credit_gate.run(
        ["dreamina-canvas", "node", "create", "--credit-ceiling", "99999"],
        approved_by="user:张三",
        max_credits=80,
        executor=fake_executor,
    )

    cmd = calls[0]
    flags = [tok for tok in cmd if tok == "--credit-ceiling"]
    assert flags == ["--credit-ceiling"], f"最终命令必须恰好一个 --credit-ceiling，得到 {cmd}"
    idx = cmd.index("--credit-ceiling")
    assert cmd[idx + 1] == "80"
    assert "99999" not in cmd


def test_blank_approval_raises():
    """approved_by 为空串等假值一律拒绝，且不调用执行器。"""
    calls = []

    def fake_executor(cmd, **kwargs):
        calls.append(cmd)
        return FakeResult()

    with pytest.raises(PermissionError):
        credit_gate.run(
            ["dreamina-canvas", "node", "create"], approved_by="", max_credits=100,
            executor=fake_executor,
        )
    assert calls == [], "空批准不得调用执行器"


def test_whitespace_approval_raises():
    """approved_by 为纯空白（如 " "）也必须拒绝，不得当有效批文。"""
    calls = []

    def fake_executor(cmd, **kwargs):
        calls.append(cmd)
        return FakeResult()

    with pytest.raises(PermissionError):
        credit_gate.run(
            ["dreamina-canvas", "node", "create"], approved_by=" ", max_credits=100,
            executor=fake_executor,
        )
    assert calls == [], "纯空白批文不得调用执行器"


def test_run_rejects_non_int_max_credits():
    """max_credits 非 int（如 None）直接拒绝，禁止 --credit-ceiling None。"""
    calls = []

    def fake_executor(cmd, **kwargs):
        calls.append(cmd)
        return FakeResult()

    with pytest.raises(ValueError):
        credit_gate.run(
            ["dreamina-canvas", "node", "create"], approved_by="user:张三",
            max_credits=None, executor=fake_executor,
        )
    assert calls == []


def test_run_rejects_bool_max_credits():
    """max_credits 是 bool（int 子类）也算非法——type() 才是真 int。"""
    calls = []

    def fake_executor(cmd, **kwargs):
        calls.append(cmd)
        return FakeResult()

    with pytest.raises(ValueError):
        credit_gate.run(
            ["dreamina-canvas", "node", "create"], approved_by="user:张三",
            max_credits=True, executor=fake_executor,
        )
    assert calls == [], "bool 上限不得调用执行器"
