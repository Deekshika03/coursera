"""Quiz interaction: extract questions, apply LLM answers, agree, and submit."""

import logging
import re
from typing import Any

from playwright.sync_api import Locator, Page

from coursera_automation.config import Settings
from coursera_automation.items.quiz_solver import solve_quiz_with_llm

logger = logging.getLogger(__name__)


def _detect_type(q_loc: Locator) -> str:
    """Classify question as selection or multiselect."""
    return "multiselect" if q_loc.locator('input[type="checkbox"], [role="checkbox"]').count() else "selection"


def handle_quiz(page: Page, cfg: Settings) -> None:
    """Handle complete quiz lifecycle: launch, solve, agree, and submit."""
    logger.info("Handling quiz assignment...")
    start_btn = page.get_by_role("button", name=re.compile(r"(start|resume) assignment", re.IGNORECASE)).first
    if start_btn.is_visible(timeout=cfg.timeout_ms):
        start_btn.click()
        page.wait_for_timeout(3000)

    q_locators = page.locator('fieldset, [data-testid*="question"]').all()
    questions: list[dict[str, Any]] = []
    for idx, q_loc in enumerate(q_locators):
        text, q_type = q_loc.inner_text().strip(), _detect_type(q_loc)
        opts = [o.inner_text().strip() for o in q_loc.locator("label").all() if o.inner_text().strip()]
        logger.info("Question %d [%s]: %s | Options: %s", idx + 1, q_type, text, opts)
        questions.append({"index": idx, "text": text, "options": opts, "type": q_type})

    answers = solve_quiz_with_llm(questions, cfg)
    logger.info("Quiz answers received: %s", answers)

    for idx, q_loc in enumerate(q_locators):
        for opt_text in answers.get(idx, []):
            btn = q_loc.locator("label").filter(has_text=opt_text).first
            if btn.is_visible():
                btn.scroll_into_view_if_needed()
                btn.click()
                logger.info("Question %d: checked '%s'", idx + 1, opt_text)

    sel = 'label:has-text(", understand and agree."), [aria-label*="understand and agree" i]'
    agree = page.locator(sel).first
    if agree.is_visible(timeout=cfg.timeout_ms):
        agree.scroll_into_view_if_needed()
        agree.click(force=True)
        logger.info("Clicked checkbox matching ', understand and agree.'")

    submit_btn = page.get_by_role("button", name=re.compile(r"^submit", re.IGNORECASE)).first
    if submit_btn.is_visible(timeout=cfg.timeout_ms):
        submit_btn.scroll_into_view_if_needed()
        submit_btn.click()
        logger.info("Submitted quiz assignment.")
        page.wait_for_timeout(3000)
