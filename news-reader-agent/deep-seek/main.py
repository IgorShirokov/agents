import os
import sys

# Принудительно UTF-8 для консоли (иначе на Windows cp1251 ломает эмодзи в логах crewai).
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

import dotenv

dotenv.load_dotenv()

from crewai import Crew, Agent, Task, LLM
from crewai.project import CrewBase, agent, task, crew
from tools import search_tool, scrape_tool

# DeepSeek через OpenAI-совместимый эндпоинт (litellm маршрут "openai/...").
deepseek_llm = LLM(
    model=f"openai/{os.getenv('API_MODEL', 'deepseek-chat')}",
    base_url=os.getenv("API_BASE_URL", "https://api.deepseek.com/v1"),
    api_key=os.getenv("OPENAI_API_KEY"),
)


@CrewBase
class NewsReaderAgent:
    @agent
    def news_hunter_agent(self):
        return Agent(
            config=self.agents_config["news_hunter_agent"],
            tools=[search_tool, scrape_tool],
            llm=deepseek_llm,
        )

    @agent
    def summarizer_agent(self):
        return Agent(
            config=self.agents_config["summarizer_agent"],
            tools=[
                scrape_tool,
            ],
            llm=deepseek_llm,
        )

    @agent
    def curator_agent(self):
        return Agent(
            config=self.agents_config["curator_agent"],
            llm=deepseek_llm,
        )

    @task
    def content_harvesting_task(self):
        return Task(
            config=self.tasks_config["content_harvesting_task"],
        )

    @task
    def summarization_task(self):
        return Task(
            config=self.tasks_config["summarization_task"],
        )

    @task
    def final_report_assembly_task(self):
        return Task(
            config=self.tasks_config["final_report_assembly_task"],
        )

    @crew
    def crew(self):
        return Crew(
            tasks=self.tasks,
            agents=self.agents,
            verbose=True,
        )


if __name__ == "__main__":
    result = NewsReaderAgent().crew().kickoff(inputs={"topic": "Cambodia Thailand War."})

    for task_output in result.tasks_output:
        print(task_output)
