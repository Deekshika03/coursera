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
