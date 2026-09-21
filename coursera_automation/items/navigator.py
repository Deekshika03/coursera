"""Navigation controls: resume, next item progression, and dialog dismissal."""

import logging
import re

from playwright.sync_api import Page

from coursera_automation.config import Settings

logger = logging.getLogger(__name__)


def dismiss_dialogs(page: Page) -> None:
    """Dismiss transient modals, popups, and sound effects prompts."""
    sound = page.locator('div:has-text("sound effects") button').first
    if sound.is_visible(timeout=400):
        sound.click(force=True)
    for sel in ('.ab-close-button', 'button[aria-label*="close" i]', 'button:has-text("Got it")'):
        btn = page.locator(sel).first
        if btn.is_visible(timeout=300):
            btn.click(force=True)
            break


def click_resume(page: Page, cfg: Settings) -> None:
    """Scroll vertically and click Resume button on course view."""
    dismiss_dialogs(page)
    lbl = page.locator("span.cds-button-label", has_text=re.compile(r"resume", re.IGNORECASE))
    btn = page.locator('button, [role="button"]').filter(has=lbl).first
    for _ in range(8):
        if btn.is_visible():
            break
        page.mouse.wheel(0, 500)
        page.wait_for_timeout(400)
    btn.wait_for(state="visible", timeout=cfg.timeout_ms)
    logger.info("Clicking course resume/start CTA...")
    btn.click()
    page.wait_for_timeout(3000)


def click_next_item(page: Page, cfg: Settings) -> bool:
    """Locate and click 'Go to next item' or video end-card button."""
    sel = 'button:has-text("next item"), a:has-text("next item"), [data-testid*="next-item"], div[class*="ItemCard"] button'
    for _ in range(5):
        dismiss_dialogs(page)
        btn = page.locator(sel).first
        if btn.is_visible(timeout=1000):
            logger.info("Advancing via next item button...")
            btn.click(force=True)
            page.wait_for_timeout(3000)
            return True
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(1000)
    logger.warning("'Go to next item' button was not visible.")
    return False
