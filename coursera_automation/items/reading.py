"""Reading item automation: click Mark as completed."""

import logging
import re

from playwright.sync_api import Page

from coursera_automation.config import Settings

logger = logging.getLogger(__name__)


def handle_reading(page: Page, cfg: Settings) -> None:
    """Mark reading item as completed."""
    logger.info("Handling reading item...")
    mark_btn = (
        page.get_by_role("button", name=re.compile(r"mark as completed", re.IGNORECASE))
        .or_(page.get_by_text(re.compile(r"mark as completed", re.IGNORECASE)))
        .first
    )

    if mark_btn.is_visible(timeout=cfg.timeout_ms):
        mark_btn.click()
        logger.info("Clicked 'Mark as completed'.")
        page.wait_for_timeout(2000)
    else:
        logger.info("'Mark as completed' button already completed or not present.")
