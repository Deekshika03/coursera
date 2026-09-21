"""Specialization and course navigation steps."""

import logging
import re

from playwright.sync_api import Page

from coursera_automation.config import Settings
from coursera_automation.items.dispatcher import process_items
from coursera_automation.items.navigator import click_resume

logger = logging.getLogger(__name__)


def open_course(page: Page, cfg: Settings) -> None:
    """Navigate to specialization, click Go to course, resume, and process items."""
    logger.info("Navigating to course page: %s", cfg.course_url)
    page.goto(cfg.course_url, wait_until="networkidle")

    cta = (
        page.get_by_role("link", name=re.compile(r"go to course", re.IGNORECASE))
        .or_(page.get_by_role("button", name=re.compile(r"go to course", re.IGNORECASE)))
        .or_(page.get_by_role("button", name=re.compile(r"enroll", re.IGNORECASE)))
        .first
    )

    cta.wait_for(state="visible", timeout=cfg.timeout_ms)
    logger.info("Clicking course CTA: %s", cta.inner_text().strip())
    cta.click()
    page.wait_for_timeout(3000)

    click_resume(page, cfg)
    process_items(page, cfg)
