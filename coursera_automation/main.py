"""Entry point for Coursera Playwright automation."""

import logging

from playwright.sync_api import sync_playwright

from coursera_automation.auth import login
from coursera_automation.config import Settings, config
from coursera_automation.course import open_course

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def run(cfg: Settings = config) -> None:
    """Run the complete Coursera automation workflow."""
    logger.info("Launching Chromium (headless=%s)...", cfg.headless)
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=cfg.headless,
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        logger.info("Executing login flow for %s...", cfg.email)
        login(page, cfg)

        logger.info("Navigating to course...")
        open_course(page, cfg)

        page.screenshot(path="coursera_result.png")
        logger.info("Screenshot saved to coursera_result.png")
        browser.close()


if __name__ == "__main__":
    run()
