"""Video playback automation: play click, 2x speed, duration wait."""

import logging
import math
import time

from playwright.sync_api import Page

from coursera_automation.config import Settings

logger = logging.getLogger(__name__)


def calculate_video_wait(duration_seconds: float) -> int:
    """Calculate wait time in seconds: ceil(duration_minutes / 2) * 60."""
    duration_minutes = duration_seconds / 60.0
    wait_minutes = max(1, math.ceil(duration_minutes / 2.0))
    return int(wait_minutes * 60)


def handle_video(page: Page, cfg: Settings) -> None:
    """Start video, reveal controls, set 2x speed, and wait."""
    logger.info("Handling video item...")
    play_btn = page.locator(
        '.rc-VideoControlsContainer button, button[aria-label*="play" i], .rc-VideoControlsContainer'
    ).first
    if play_btn.is_visible(timeout=cfg.timeout_ms):
        play_btn.click(force=True)
        page.wait_for_timeout(1000)

    page.evaluate("() => document.querySelector('video')?.play()")

    box = page.locator("video, .rc-VideoControlsContainer").first.bounding_box()
    if box:
        page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        page.wait_for_timeout(500)

    speed_btn = page.locator(
        'button[aria-label="Video playback rate switcher"]'
    ).or_(page.locator('[aria-label*="playback rate" i]')).first

    if speed_btn.is_visible(timeout=3000):
        for _ in range(4):
            speed_btn.click(force=True)
            page.wait_for_timeout(300)

    page.evaluate(
        "() => { const v = document.querySelector('video'); if (v) { v.playbackRate = 2.0; v.play(); } }"
    )
    duration = float(
        page.evaluate("() => document.querySelector('video')?.duration || 0")
    )
    wait_secs = calculate_video_wait(duration) if duration > 0 else 60
    logger.info("Video duration: %.1fs. Waiting %ds at 2x...", duration, wait_secs)
    time.sleep(wait_secs)
