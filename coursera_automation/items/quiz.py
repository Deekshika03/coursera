"""Quiz interaction: extract questions, apply LLM answers, agree, and submit."""

import logging
import re
from typing import Any

from playwright.sync_api import Page

from coursera_automation.config import Settings
from coursera_automation.items.quiz_solver import solve_quiz_with_llm

logger = logging.getLogger(__name__)


def handle_quiz(page: Page, cfg: Settings) -> None:
    """Handle complete quiz lifecycle: launch, solve, agree, and submit."""
    logger.info("Handling quiz assignment...")
    start_btn = page.get_by_role(
        "button", name=re.compile(r"(start|resume) assignment", re.IGNORECASE)
    ).first
    if start_btn.is_visible(timeout=cfg.timeout_ms):
        start_btn.click()
        page.wait_for_timeout(3000)

    # Extract questions and choices
    q_locators = page.locator('fieldset, [data-testid*="question"]').all()
    questions: list[dict[str, Any]] = []
    for idx, q_loc in enumerate(q_locators):
        text = q_loc.inner_text().strip()
        opts = [o.inner_text().strip() for o in q_loc.locator("label").all()]
        questions.append({"index": idx, "text": text, "options": opts})

    answers = solve_quiz_with_llm(questions, cfg)
    for idx, q_loc in enumerate(q_locators):
        selected = answers.get(idx, [])
        for opt_text in selected:
            btn = q_loc.locator("label").filter(has_text=opt_text).first
            if btn.is_visible():
                btn.click()

    # Agree to honor code & submit
    agree = (
        page.get_by_label(re.compile(r"understand and agree", re.IGNORECASE))
        .or_(page.locator('input[type="checkbox"]'))
        .last
    )
    if agree.is_visible() and not agree.is_checked():
        agree.check()

    submit_btn = page.get_by_role("button", name=re.compile(r"^submit", re.IGNORECASE)).first
    if submit_btn.is_visible(timeout=cfg.timeout_ms):
        submit_btn.click()
        page.wait_for_timeout(3000)
