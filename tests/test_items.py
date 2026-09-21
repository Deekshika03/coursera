"""Unit tests for item calculation and logic."""

from coursera_automation.items.video import calculate_video_wait


def test_video_duration_ceil() -> None:
    """Verify video wait calculation matches user rules."""
    # 7 minutes = 420 seconds -> 3.5 mins -> ceil to 4 mins = 240 seconds
    assert calculate_video_wait(420.0) == 240

    # 5 minutes = 300 seconds -> 2.5 mins -> ceil to 3 mins = 180 seconds
    assert calculate_video_wait(300.0) == 180

    # 10 minutes = 600 seconds -> 5 mins -> ceil to 5 mins = 300 seconds
    assert calculate_video_wait(600.0) == 300

    # Short video (30 seconds) -> min 1 minute = 60 seconds
    assert calculate_video_wait(30.0) == 60
