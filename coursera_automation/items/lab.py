"""Lab automation handler: agree checkbox and launch app interaction."""

import logging
import re

from playwright.sync_api import Page

from coursera_automation.config import Settings

logger = logging.getLogger(__name__)


def handle_lab(page: Page, cfg: Settings) -> None:
    """Check I agree, launch app, and prepare for next item."""
    logger.info("Handling lab item...")
    page.wait_for_load_state("domcontentloaded")

    # Locate 'I agree' checkbox
    agree = (
        page.get_by_label(re.compile(r"agree", re.IGNORECASE))
        .or_(page.locator('input[type="checkbox"]'))
        .first
    )
    if agree.is_visible(timeout=3000) and not agree.is_checked():
        agree.check(force=True)
        logger.info("Checked 'I agree' checkbox.")
        page.wait_for_timeout(500)

    # Locate Launch App button or link
    launch = (
        page.get_by_role("button", name=re.compile(r"launch (app|lab)", re.IGNORECASE))
        .or_(page.get_by_role("link", name=re.compile(r"launch (app|lab)", re.IGNORECASE)))
        .or_(
            page.locator('button, a, [role="button"]').filter(
                has_text=re.compile(r"launch (app|lab)", re.IGNORECASE)
            )
        )
        .first
    )

    for _ in range(6):
        if launch.is_visible():
            break
        page.mouse.wheel(0, 300)
        page.wait_for_timeout(300)

    launch.wait_for(state="visible", timeout=cfg.timeout_ms)
    launch.scroll_into_view_if_needed()
    launch.click(force=True)
    logger.info("Clicked 'Launch App'.")
    page.wait_for_timeout(3000)
