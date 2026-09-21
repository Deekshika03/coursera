# Architecture & Design

This project automates Coursera workflows using Playwright in Python, strictly adhering to NASA JPL Rule 4 and the 3-step verification loop.

## Architecture

```mermaid
sequenceDiagram
    autonumber
    participant Main as coursera_automation.main
    participant Auth as coursera_automation.auth
    participant Course as coursera_automation.course
    participant Disp as items.dispatcher
    participant Item as Video/Lab/Reading/Quiz/Dialogue/Discussion
    participant LLM as NVIDIA GLM-5.3
    participant Nav as items.navigator

    Main->>Auth: login(page, config)
    Main->>Course: open_course(page, config)
    Course->>Nav: click_resume(page, config)
    Course->>Disp: process_items(page, config)
    loop Up to max_items
        Disp->>Item: dispatch_item(page, config)
        opt Quiz Item
            Item->>LLM: solve_quiz_with_llm(questions)
            LLM-->>Item: JSON answers
            Item->>Item: Check honor code & submit
        end
        Disp->>Nav: click_next_item(page, config)
    end
```

## Modular Decomposition (NASA JPL Rule 4)

- `coursera_automation/config.py`: Environment configuration and typed dataclass.
- `coursera_automation/auth.py`: Authentication interactions and modal orchestration.
- `coursera_automation/course.py`: Specialization navigation and course entry.
- `coursera_automation/items/video.py`: Speed 2x and ceiling wait calculation.
- `coursera_automation/items/lab.py`: Lab agreement and app launch.
- `coursera_automation/items/reading.py`: Reading completion.
- `coursera_automation/items/dialogue.py`: Dialogue start and finish.
- `coursera_automation/items/discussion.py`: Discussion response input.
- `coursera_automation/items/quiz_solver.py`: NVIDIA LLM API integration.
- `coursera_automation/items/quiz.py`: Quiz interaction, honor code, submission.
- `coursera_automation/items/navigator.py`: Resume and next item navigation.
- `coursera_automation/items/dispatcher.py`: Item detection and iteration loop.
- `coursera_automation/main.py`: Browser lifecycle management.
