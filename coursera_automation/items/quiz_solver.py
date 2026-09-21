"""LLM-based quiz question solver using NVIDIA GLM-5.3 via OpenAI SDK."""

import json
import logging
import re
from typing import Any

from openai import OpenAI

from coursera_automation.config import Settings

logger = logging.getLogger(__name__)


def solve_quiz_with_llm(
    questions: list[dict[str, Any]], cfg: Settings
) -> dict[int, list[str]]:
    """Query NVIDIA LLM with questions and parse selected answer options."""
    client = OpenAI(base_url=cfg.nvidia_base_url, api_key=cfg.nvidia_api_key)
    prompt = (
        "Answer these quiz questions. For type 'selection', choose exactly one option. "
        "For 'multiselect', choose all correct options.\n"
        "Respond ONLY in valid JSON matching:\n"
        '{"answers": [{"index": 0, "selected": ["option text"]}]}\n\n'
        f"Questions:\n{json.dumps(questions, indent=2)}"
    )

    resp = client.chat.completions.create(
        model=cfg.nvidia_model,
        messages=[
            {"role": "system", "content": "You are an expert exam solver."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=1024,
    )
    raw = resp.choices[0].message.content or "{}"
    clean = re.sub(r"```json|```", "", raw).strip()

    result: dict[int, list[str]] = {}
    try:
        data = json.loads(clean)
        for item in data.get("answers", []):
            result[item["index"]] = item.get("selected", [])
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as err:
        logger.warning("Failed parsing LLM answer: %s. Raw: %s", err, raw)
    return result
