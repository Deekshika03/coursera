# Coursera Playwright Automation

Automated workflow for logging into Coursera, navigating to the Generative AI Specialization, resuming courses, and progressing through learning items using Playwright and `uv`.

## Supported Learning Items

| Item | Automated Behavior |
|---|---|
| **Video** | Plays at $2\times$ speed (clicks $1\times$ 4 times) and waits for `ceil(duration/120)` minutes before advancing |
| **Lab** | Checks "I agree" checkbox, clicks "Launch app", and advances |
| **Reading** | Clicks "Mark as completed" and advances |
| **Dialogue** | Clicks "Start dialogue" $\to$ "End dialogue" and advances |
| **Discussion** | Types `"ok"` into chatbox, clicks "Reply", and advances |
| **Quiz** | Clicks Start/Resume assignment, queries NVIDIA LLM (`z-ai/glm-5.3`) for answers, checks honor code agreement, submits, and advances |

## Architecture Overview

Adheres to NASA JPL Rule 4 (≤ 60 lines per module):
- `coursera_automation/config.py`: Environment configuration and credentials.
- `coursera_automation/auth.py`: Authentication steps.
- `coursera_automation/course.py`: Specialization navigation & course entry.
- `coursera_automation/items/video.py`: Video playback and ceiling-wait logic.
- `coursera_automation/items/lab.py`: Lab agreement and app launch.
- `coursera_automation/items/reading.py`: Reading completion.
- `coursera_automation/items/dialogue.py`: Dialogue start and finish.
- `coursera_automation/items/discussion.py`: Discussion response input.
- `coursera_automation/items/quiz_solver.py`: NVIDIA LLM API integration.
- `coursera_automation/items/quiz.py`: Quiz interaction and submission.
- `coursera_automation/items/navigator.py`: Resume and next item navigation.
- `coursera_automation/items/dispatcher.py`: Item detection and iteration loop.
- `coursera_automation/main.py`: Browser orchestration.

## Configuration

| Variable | Description | Default |
|---|---|---|
| `COURSERA_EMAIL` | Account email | `24bai70310@cuchd.in` |
| `COURSERA_PASSWORD` | Account password | `Lakshya.24AI` |
| `COURSERA_HEADLESS` | Run in headless mode | `false` |
| `COURSERA_MAX_ITEMS` | Maximum items to process | `25` |
| `NVIDIA_API_KEY` | NVIDIA API Key for LLM solver | *(configured)* |
| `NVIDIA_BASE_URL` | NVIDIA API Base URL | `https://integrate.api.nvidia.com/v1` |
| `NVIDIA_MODEL` | Model for quiz solving | `z-ai/glm-5.3` |

## Usage & Quality Gates

Run automation:
```bash
uv run python -m coursera_automation.main
```

Verification:
```bash
uv run ruff check --fix
uv run ty check
uv run pytest
```
