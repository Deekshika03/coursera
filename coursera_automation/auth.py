"""Coursera login automation steps."""

import logging

from playwright.sync_api import Page

from coursera_automation.config import Settings

logger = logging.getLogger(__name__)


def login(page: Page, cfg: Settings) -> None:
    """Perform authentication flow on Coursera."""
    logger.info("Opening login URL: %s", cfg.login_url)
    page.goto(cfg.login_url, wait_until="networkidle")

    # Locate and fill email
    email_input = page.locator('input[placeholder="name@email.com"]')
    email_input.wait_for(state="visible", timeout=cfg.timeout_ms)
    email_input.fill(cfg.email)

    # Click Continue button
    continue_btn = page.get_by_role("button", name="Continue", exact=True).first
    continue_btn.wait_for(state="visible", timeout=cfg.timeout_ms)
    continue_btn.click()

    # Locate and fill password
    pwd_input = page.locator('input[type="password"]')
    pwd_input.wait_for(state="visible", timeout=cfg.timeout_ms)
    pwd_input.fill(cfg.password)

    # Click Next button
    next_btn = page.get_by_role("button", name="Next", exact=True).first
    next_btn.wait_for(state="visible", timeout=cfg.timeout_ms)
    next_btn.click()

    logger.info("Credentials submitted. Waiting for authentication state...")
    page.wait_for_timeout(6000)
