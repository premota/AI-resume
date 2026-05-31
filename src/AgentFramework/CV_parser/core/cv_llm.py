from dataclasses import dataclass

from AgentFramework.AgentFactory.agent_config import AgentDeps
from AgentFramework.AgentFactory.runner import run_agent
from AgentFramework.CV_parser.schemas.cv_schema import CVOutputSchema
from AgentFramework.prompt import CV_RUNTIME_PROMPT
from pydantic_ai import Agent as PydanticAIAgent


@dataclass(kw_only=True)
class CVDeps(AgentDeps):
    cv_text: str


def _construct_full_prompt(cv_text: str, run_time_prompt: str) -> str:
    return f"""
    {run_time_prompt}

    CV INFORMATION:
    {cv_text}
    """


async def parse_cv(
    agent: PydanticAIAgent[CVDeps, CVOutputSchema],
    cv_text: str,
    cv_runtime_prompt: str = CV_RUNTIME_PROMPT,
) -> CVOutputSchema:
    cv_deps = CVDeps(cv_text=cv_text)

    cv_instructions = _construct_full_prompt(
        cv_text=cv_text, run_time_prompt=cv_runtime_prompt
    )

    return await run_agent(
        agent=agent,
        user_prompt="execute",
        dependency=cv_deps,
        user_instruction=cv_instructions,
    )
