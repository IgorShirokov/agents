# Job Hunter Agent (DeepSeek / CrewAI)

Мультиагентный пайплайн на [CrewAI](https://docs.crewai.com/), который автоматизирует поиск
работы: находит вакансии, оценивает их соответствие резюме, выбирает лучшую,
переписывает резюме под неё, исследует компанию и готовит к собеседованию.

## Как это работает

Пять агентов выполняют шесть задач последовательно:

| # | Задача | Агент | Результат |
|---|--------|-------|-----------|
| 1 | `job_extraction_task` | Job Search Specialist | Список вакансий (`JobList`) |
| 2 | `job_matching_task` | Job Matching Expert | Вакансии с оценкой 1–5 (`RankedJobList`) |
| 3 | `job_selection_task` | Job Matching Expert | Лучшая вакансия (`ChosenJob`) |
| 4 | `resume_rewriting_task` | Resume Optimization Specialist | `output/rewritten_resume.md` |
| 5 | `company_research_task` | Company Research Strategist | `output/company_research.md` |
| 6 | `interview_prep_task` | Interview Prep Coach | `output/interview_prep.md` |

Поиск вакансий и исследование компании выполняются через веб-поиск
([Firecrawl](https://www.firecrawl.dev/)). Резюме пользователя из
`knowledge/resume.txt` подключается как knowledge source для агентов, чтобы
оценивать соответствие, переписывать резюме и готовить к интервью.

## Структура проекта

```
deep-seek/
├── main.py              # Определение crew (агенты, задачи) и точка входа
├── models.py            # Pydantic-схемы: Job, JobList, RankedJob, ChosenJob и др.
├── tools.py             # web_search_tool на базе Firecrawl
├── config/
│   ├── agents.yaml      # Роли, цели, backstory и LLM каждого агента
│   └── tasks.yaml       # Описания задач и ожидаемые результаты
├── knowledge/
│   └── resume.txt       # Резюме пользователя (knowledge source)
├── output/              # Сгенерированные markdown-файлы
└── pyproject.toml       # Зависимости (управляются через uv)
```

## Технологии и сервисы

- **[CrewAI](https://docs.crewai.com/)** — оркестрация агентов
- **[Firecrawl](https://www.firecrawl.dev/)** — веб-поиск и скрапинг (`FIRECRAWL_API_KEY`)
- **[Serper](https://serper.dev/)** — поисковый API (`SERPER_API_KEY`)
- **DeepSeek / OpenAI-совместимый API** — LLM-провайдер

## Настройка

Создайте файл `.env` в корне проекта:

```env
OPENAI_API_KEY=your_key
API_BASE_URL=https://api.deepseek.com/v1
API_MODEL=deepseek-v4-flash
FIRECRAWL_API_KEY=your_key
```

Поместите своё резюме в `knowledge/resume.txt`.

> Примечание: модель LLM для агентов задаётся в `config/agents.yaml` (поле `llm`).
> Чтобы использовать DeepSeek для всех агентов, обновите там значение `llm`.

## Запуск

```bash
uv sync       # установка зависимостей
uv run main.py
```

Параметры поиска задаются в `main.py` (вызов `kickoff`):

```python
inputs={
    "level": "Senior",
    "position": "Golang Developer",
    "location": "Netherlands",
}
```

После выполнения результаты появятся в каталоге `output/`.

## Требования

- Python >= 3.13
- [uv](https://docs.astral.sh/uv/) для управления зависимостями
