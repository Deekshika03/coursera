"""Navigation controls: resume, next item progression, and dialog dismissal."""

import logging
import re

from playwright.sync_api import Page

from coursera_automation.config import Settings

logger = logging.getLogger(__name__)


def dismiss_dialogs(page: Page) -> None:
    """Dismiss transient modals, in-app messages, or notification dialogues."""
    btn = page.locator(
        '.ab-close-button, button:has-text("Got it"), button[aria-label="Close"]'
    ).first
    if btn.is_visible(timeout=1000):
        btn.click()
        page.wait_for_timeout(500)


def click_resume(page: Page, cfg: Settings) -> None:
    """Scroll vertically and click Resume button on course view."""
    dismiss_dialogs(page)
    lbl = page.locator("span.cds-button-label", has_text=re.compile(r"resume", re.IGNORECASE))
    resume_btn = page.locator('button, [role="button"]').filter(has=lbl).or_(
        page.get_by_role("button", name=re.compile(r"resume|start", re.IGNORECASE))
    ).first

    for _ in range(8):
        if resume_btn.is_visible():
            break
        page.mouse.wheel(0, 500)
        page.wait_for_timeout(400)

    resume_btn.wait_for(state="visible", timeout=cfg.timeout_ms)
    resume_btn.scroll_into_view_if_needed()
    logger.info("Clicking course resume/start CTA...")
    resume_btn.click()
    page.wait_for_timeout(3000)


def click_next_item(page: Page, cfg: Settings) -> bool:
    """Locate and click 'Go to next item' or 'Next item'."""
    dismiss_dialogs(page)
    next_btn = page.get_by_role(
        "button", name=re.compile(r"(go to )?next item", re.IGNORECASE)
    ).or_(
        page.get_by_role("link", name=re.compile(r"(go to )?next item", re.IGNORECASE))
    ).or_(page.locator('[data-testid*="next-item"]')).first

    if next_btn.is_visible(timeout=cfg.timeout_ms):
        logger.info("Advancing via 'Go to next item'...")
        next_btn.click()
        page.wait_for_timeout(3000)
        return True
    logger.warning("'Go to next item' button was not visible.")
    return False
