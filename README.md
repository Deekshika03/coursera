# Coursera Playwright Automation

Automated workflow for logging into Coursera and navigating to the Generative AI for Software Developers specialization using Playwright and `uv`.

## Architecture Overview

Built following NASA JPL Rule 4 (Single Sheet of Paper Architecture, ≤ 60 lines per module):

- `coursera_automation/config.py`: Environment-aware settings and credentials.
- `coursera_automation/auth.py`: Coursera authentication steps (email, Continue, password, Next).
- `coursera_automation/course.py`: Specialization navigation and CTA interaction.
- `coursera_automation/main.py`: Browser lifecycle and orchestration.
- `main.py`: Top-level CLI entry point.
- `docs/ARCHITECTURE.md`: Detailed architectural design and sequence diagrams.

## Prerequisites

- Python `>=3.14`
- [uv](https://docs.astral.sh/uv/)

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Install Playwright browser binaries:
   ```bash
   uv run playwright install chromium
   ```

## Configuration

Environment variables (with sensible defaults):

| Variable | Description | Default |
|---|---|---|
| `COURSERA_EMAIL` | Account email | `24bai70310@cuchd.in` |
| `COURSERA_PASSWORD` | Account password | `Lakshya.24AI` |
| `COURSERA_LOGIN_URL` | Login URL | `https://www.coursera.org/#authMode=login` |
| `COURSERA_COURSE_URL` | Target course URL | `https://www.coursera.org/specializations/generative-ai-for-software-developers` |
| `COURSERA_HEADLESS` | Run browser in headless mode | `false` |
| `COURSERA_TIMEOUT_MS` | Action timeout in milliseconds | `30000` |

## Usage

Run the automation with:
```bash
uv run python -m coursera_automation.main
```
Or:
```bash
uv run python main.py
```

## Quality & Verification Gates

The 3 mandatory quality commands:
```bash
uv run ruff check --fix
uv run ty check
uv run pytest
```
