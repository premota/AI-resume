from dataclasses import dataclass

from pydantic_ai import Agent as PydanticAIAgent

from AgentFramework.prompt import RUN_TIME_PROMPT
from AgentFramework.AgentFactory.agent_config import AgentDeps
from AgentFramework.JD_Parser.schemas.jd_schema import JDOutputSchema
from AgentFramework.AgentFactory.runner import run_agent


@dataclass(kw_only=True)
class JDDeps(AgentDeps):
    job_description: str


def _construct_full_prompt(job_description: str, run_time_prompt: str) -> str:
    return f""" 
    {run_time_prompt}

    JOB DESCRIPTION:
    {job_description}
    """


async def parse_jd(
    agent: PydanticAIAgent[JDDeps, JDOutputSchema],
    jd: str,
    run_time_prompt: str = RUN_TIME_PROMPT,
) -> JDOutputSchema:
    jd_deps = JDDeps(job_description=jd)

    instruction = _construct_full_prompt(jd, run_time_prompt=run_time_prompt)

    return await run_agent(
        agent=agent,
        user_prompt="execute",
        dependency=jd_deps,
        user_instruction=instruction,
    )
