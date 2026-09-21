"""Dialogue item automation: click Start dialogue and End dialogue."""

import logging
import re

from playwright.sync_api import Page

from coursera_automation.config import Settings

logger = logging.getLogger(__name__)


def handle_dialogue(page: Page, cfg: Settings) -> None:
    """Handle dialogue item: Start dialogue -> End dialogue."""
    logger.info("Handling dialogue item...")
    start_btn = (
        page.get_by_role("button", name=re.compile(r"start dialogue", re.IGNORECASE))
        .or_(page.get_by_text(re.compile(r"start dialogue", re.IGNORECASE)))
        .first
    )
    if start_btn.is_visible(timeout=cfg.timeout_ms):
        start_btn.click()
        logger.info("Clicked 'Start dialogue'.")
        page.wait_for_timeout(2000)

    end_btn = (
        page.get_by_role("button", name=re.compile(r"end dialogue", re.IGNORECASE))
        .or_(page.get_by_text(re.compile(r"end dialogue", re.IGNORECASE)))
        .first
    )
    if end_btn.is_visible(timeout=cfg.timeout_ms):
        end_btn.click()
        logger.info("Clicked 'End dialogue'.")
        page.wait_for_timeout(2000)
