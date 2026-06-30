# Job Hunter Agent (OpenAI)

Мультиагентный пайплайн на **CrewAI**, который ищет вакансии, сопоставляет их с вашим
резюме, выбирает наиболее подходящую и готовит вас к собеседованию — от начала до конца.

Это **OpenAI**-версия агента (модель `openai/o4-mini-2025-04-16`).

## Как это работает

Команда состоит из пяти агентов и шести последовательных задач:

| # | Задача | Агент | Результат |
|---|--------|-------|-----------|
| 1 | `job_extraction_task` | Job Search Agent | `JobList` — вакансии, собранные из веба |
| 2 | `job_matching_task` | Job Matching Agent | `RankedJobList` — оценка 1–5 относительно резюме |
| 3 | `job_selection_task` | Job Matching Agent | `ChosenJob` — единственная лучшая вакансия |
| 4 | `resume_rewriting_task` | Resume Optimization Agent | `output/rewritten_resume.md` |
| 5 | `company_research_task` | Company Research Agent | `output/company_research.md` |
| 6 | `interview_prep_task` | Interview Prep Agent | `output/interview_prep.md` |

Ваше резюме (`knowledge/resume.txt`) загружается как источник знаний CrewAI, поэтому
агенты сопоставления, переписывания резюме, исследования компании и подготовки к
собеседованию рассуждают на основе вашего реального опыта. Веб-поиск работает через
**Firecrawl** (`tools.py`).

## Структура проекта

```
openai/
├── main.py              # Определение Crew + запуск (kickoff)
├── models.py            # Pydantic-схемы (Job, JobList, RankedJob, ChosenJob...)
├── tools.py             # web_search_tool на базе Firecrawl
├── config/
│   ├── agents.yaml      # Роли, цели, бэкграунд и LLM агентов
│   └── tasks.yaml       # Описания задач и ожидаемые результаты
├── knowledge/
│   └── resume.txt       # Ваше резюме (источник знаний)
└── output/              # Сгенерированные резюме, исследование компании, подготовка
```

## Требования

- Python >= 3.13
- [uv](https://docs.astral.sh/uv/)
- API-ключ OpenAI и API-ключ Firecrawl

## Настройка

Создайте файл `.env` в этой папке:

```
OPENAI_API_KEY=
FIRECRAWL_API_KEY=
```

## Запуск

```
uv sync
uv run main.py
```

Параметры поиска задаются в `main.py` через входные данные `kickoff`:

```python
inputs={
    "level": "Senior",
    "position": "Golang Developer",
    "location": "Netherlands",
}
```

Измените эти значения, чтобы настроить поиск под себя. Результаты выводятся в консоль
и записываются в каталог `output/`.

## Ссылки

- CrewAI — https://docs.crewai.com/
- Firecrawl — https://www.firecrawl.dev/
- OpenAI — https://platform.openai.com/
