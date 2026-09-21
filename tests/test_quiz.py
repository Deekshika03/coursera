"""Unit tests for quiz interaction and question type detection."""

from unittest.mock import MagicMock, patch

from coursera_automation.config import Settings
from coursera_automation.items.quiz import _detect_type, handle_quiz


def test_detect_type() -> None:
    """Verify _detect_type returns multiselect for checkboxes, selection otherwise."""
    mock_multi = MagicMock()
    mock_multi.locator.return_value.count.return_value = 2
    assert _detect_type(mock_multi) == "multiselect"

    mock_single = MagicMock()
    mock_single.locator.return_value.count.return_value = 0
    assert _detect_type(mock_single) == "selection"


def test_handle_quiz_flow() -> None:
    """Verify handle_quiz solves questions, checks agreement, and submits."""
    page = MagicMock()
    cfg = Settings()
    q_loc = MagicMock()
    q_loc.inner_text.return_value = "What is 2+2?"
    opt = MagicMock()
    opt.inner_text.return_value = "4"
    q_loc.locator.return_value.all.return_value = [opt]
    q_loc.locator.return_value.count.return_value = 0

    agree_mock = MagicMock(is_visible=MagicMock(return_value=True))
    submit_mock = MagicMock(is_visible=MagicMock(return_value=True))

    def mock_loc(sel: str) -> MagicMock:
        if "understand and agree" in sel:
            return MagicMock(first=agree_mock)
        return MagicMock(all=lambda: [q_loc], first=MagicMock(is_visible=lambda timeout=0: False))

    page.locator.side_effect = mock_loc

    def mock_role(role: str, **kwargs: object) -> MagicMock:
        name = str(kwargs.get("name", ""))
        if "submit" in name.lower():
            return MagicMock(first=submit_mock)
        return MagicMock(first=MagicMock(is_visible=lambda timeout=0: False))

    page.get_by_role.side_effect = mock_role

    with patch("coursera_automation.items.quiz.solve_quiz_with_llm", return_value={0: ["4"]}):
        handle_quiz(page, cfg)

    agree_mock.click.assert_called_once_with(force=True)
    submit_mock.click.assert_called_once()
