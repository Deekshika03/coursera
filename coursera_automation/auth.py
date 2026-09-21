"""Coursera login automation steps."""

import logging
import re

from playwright.sync_api import Page

from coursera_automation.config import Settings

logger = logging.getLogger(__name__)


def wait_for_auth_complete(page: Page) -> None:
    """Wait for manual puzzle resolution and verified authenticated session."""
    logger.info("Waiting for puzzle completion and login verification...")
    for _ in range(120):
        cookies = [c["name"] for c in page.context.cookies()]
        has_auth = any(k in cookies for k in ("CAUTH", "c_user", "__204u"))
        has_prof = page.locator(
            'button[data-e2e="header-profile-menu"], button[aria-label*="profile" i]'
        ).first.is_visible()
        if has_auth or has_prof:
            logger.info("Authentication verified! Proceeding to course...")
            return
        page.wait_for_timeout(1000)
    logger.warning("Auth wait timeout reached. Continuing...")


def login(page: Page, cfg: Settings) -> None:
    """Navigate to coursera.org and authenticate only if not already logged in."""
    logger.info("Opening home URL: %s", cfg.login_url)
    page.goto(cfg.login_url, wait_until="networkidle")

    login_btn = (
        page.get_by_role("button", name=re.compile(r"^log in$", re.IGNORECASE))
        .or_(page.get_by_role("link", name=re.compile(r"^log in$", re.IGNORECASE)))
        .first
    )
    if not login_btn.is_visible(timeout=4000):
        logger.info("Already authenticated. Skipping login modal.")
        return

    logger.info("Clicking Log In...")
    login_btn.click()
    email_in = page.locator('input[placeholder="name@email.com"]')
    email_in.wait_for(state="visible", timeout=cfg.timeout_ms)
    email_in.fill(cfg.email)
    page.get_by_role("button", name="Continue", exact=True).first.click()

    pwd_in = page.locator('input[type="password"]')
    pwd_in.wait_for(state="visible", timeout=cfg.timeout_ms)
    pwd_in.fill(cfg.password)
    page.get_by_role("button", name="Next", exact=True).first.click()

    wait_for_auth_complete(page)
    page.wait_for_timeout(2000)
