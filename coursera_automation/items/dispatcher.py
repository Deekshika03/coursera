"""Item dispatcher: identifies item type and coordinates sequential execution."""

import logging

from playwright.sync_api import Page

from coursera_automation.config import Settings
from coursera_automation.items.dialogue import handle_dialogue
from coursera_automation.items.discussion import handle_discussion
from coursera_automation.items.lab import handle_lab
from coursera_automation.items.navigator import click_next_item, dismiss_dialogs
from coursera_automation.items.quiz import handle_quiz
from coursera_automation.items.reading import handle_reading
from coursera_automation.items.video import handle_video

logger = logging.getLogger(__name__)


def dispatch_item(page: Page, cfg: Settings) -> None:
    """Detect current item type and execute corresponding handler."""
    dismiss_dialogs(page)
    if page.locator("video").is_visible(timeout=2000):
        handle_video(page, cfg)
    elif page.locator('button:has-text("Launch app")').is_visible(timeout=1000):
        handle_lab(page, cfg)
    elif page.locator('button:has-text("Start dialogue")').is_visible(
        timeout=1000
    ):
        handle_dialogue(page, cfg)
    elif page.locator('button:has-text("Reply")').is_visible(timeout=1000):
        handle_discussion(page, cfg)
    elif page.locator('button:has-text("assignment")').is_visible(timeout=1000):
        handle_quiz(page, cfg)
    else:
        handle_reading(page, cfg)


def process_items(page: Page, cfg: Settings) -> None:
    """Iterate through course items up to max_items limit."""
    for step in range(cfg.max_items):
        logger.info("Processing learning item %d of %d...", step + 1, cfg.max_items)
        dispatch_item(page, cfg)
        if not click_next_item(page, cfg):
            logger.info("Item sequence concluded.")
            break
