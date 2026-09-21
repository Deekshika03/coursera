"""Lab automation handler: agree checkbox and launch app interaction."""

import logging
import re

from playwright.sync_api import Page

from coursera_automation.config import Settings

logger = logging.getLogger(__name__)


def handle_lab(page: Page, cfg: Settings) -> None:
    """Check I agree, launch app, and prepare for next item."""
    logger.info("Handling lab item...")

    agree_box = (
        page.get_by_label(re.compile(r"agree", re.IGNORECASE))
        .or_(page.locator('input[type="checkbox"]'))
        .first
    )
    if (
        agree_box.is_visible(timeout=cfg.timeout_ms)
        and not agree_box.is_checked()
    ):
        agree_box.check()
        logger.info("Checked 'I agree' checkbox.")

    launch_btn = page.get_by_role(
        "button", name=re.compile(r"launch app", re.IGNORECASE)
    ).first
    launch_btn.wait_for(state="visible", timeout=cfg.timeout_ms)
    launch_btn.click()
    logger.info("Clicked 'Launch app'.")
    page.wait_for_timeout(3000)
