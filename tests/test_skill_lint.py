"""skill_lint 结构契约测试。"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import skill_lint  # noqa: E402

FIXTURES = REPO_ROOT / "tests" / "fixtures"


def test_ok_fixture_passes():
    problems = skill_lint.lint(FIXTURES / "skill_ok")
    assert problems == []


def test_bad_fixture_reports_sections():
    problems = skill_lint.lint(FIXTURES / "skill_bad")
    assert any("缺标题" in p for p in problems)


def test_description_needs_trigger_words(tmp_path):
    skill_dir = tmp_path / "skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        "---\n"
        "name: demo-skill\n"
        "description: 这是一段足够长的描述文本，但完全不含任何领域触发词，专门用于验证触发词检查逻辑是否正确生效并给出报告。\n"
        "---\n"
        "\n"
        "## 何时使用\n\n任意。\n"
        "## 流程\n\n任意。\n"
        "## 硬闸与自检\n\n任意。\n"
        "## 产出与格式\n\n任意。\n",
        encoding="utf-8",
    )
    problems = skill_lint.lint(skill_dir)
    assert any("触发词" in p for p in problems)
