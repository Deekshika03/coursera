"""Unit tests for item calculation and logic."""

from coursera_automation.items.video import calculate_video_wait


def test_video_duration_exact() -> None:
    """Verify video wait calculation uses exact duration / 2.0 without ceiling."""
    # 7 minutes = 420 seconds -> 210.0 seconds
    assert calculate_video_wait(420.0) == 210.0

    # 5 minutes = 300 seconds -> 150.0 seconds
    assert calculate_video_wait(300.0) == 150.0

    # 75 seconds -> 37.5 seconds
    assert calculate_video_wait(75.0) == 37.5

    # Minimum threshold (0.5 seconds) -> min 1.0 second
    assert calculate_video_wait(0.5) == 1.0


def test_dispatch_item_assignment() -> None:
    """Verify dispatch_item identifies assignment via .first and delegates to handle_quiz."""
    from unittest.mock import MagicMock, patch

    from coursera_automation.config import Settings
    from coursera_automation.items.dispatcher import dispatch_item

    mock_page = MagicMock()
    mock_page.url = "https://www.coursera.org/learn/example/lecture/abc"
    cfg = Settings()

    def mock_locator(selector: str) -> MagicMock:
        loc = MagicMock()
        loc.first.is_visible.return_value = "assignment" in selector
        loc.filter.return_value.first.is_visible.return_value = False
        return loc

    mock_page.locator.side_effect = mock_locator

    with (
        patch("coursera_automation.items.dispatcher.dismiss_dialogs"),
        patch("coursera_automation.items.dispatcher.handle_quiz") as mock_quiz,
    ):
        dispatch_item(mock_page, cfg)
        mock_quiz.assert_called_once_with(mock_page, cfg)
