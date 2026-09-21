"""Video playback automation: 2x speed adjustment and duration waiting."""

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
    """Keep video playing at 2x speed and wait for computed duration."""
    logger.info("Handling video item...")
    page.evaluate("() => document.querySelector('video')?.play()")

    # Click 1x speed button 4 times to reach 2x
    speed_btn = page.locator('button:has-text("1x"), button[aria-label*="speed" i]').first
    if speed_btn.is_visible(timeout=3000):
        for _ in range(4):
            speed_btn.click()
            page.wait_for_timeout(300)

    # Ensure playbackRate is 2.0
    page.evaluate(
        "() => { const v = document.querySelector('video'); if (v) v.playbackRate = 2.0; }"
    )

    duration = float(
        page.evaluate("() => document.querySelector('video')?.duration || 0")
    )
    wait_secs = calculate_video_wait(duration) if duration > 0 else 60
    logger.info("Video duration: %.1fs. Waiting %ds at 2x...", duration, wait_secs)
    time.sleep(wait_secs)
