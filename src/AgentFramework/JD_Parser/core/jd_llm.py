# from typing import Generic
from dataclasses import dataclass

from AgentFramework.prompt import RUN_TIME_PROMPT

# from pydantic import Json
from pydantic_ai import Agent as PydanticAIAgent

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
)->JDOutputSchema:
    jd_deps = JDDeps(job_description=jd)

    instruction = _construct_full_prompt(jd, run_time_prompt=run_time_prompt)

    return await run_agent(
        agent=agent,
        user_prompt="execute",
        dependency=jd_deps,
        user_instruction=instruction,
    )


# class JobAdsLLM:

#     def __init__(
#         self,
#         job_description: str,
#         agent: PydanticAIAgent[JDDeps, JDOutputSchema]
#     ):
#         self.job_description = job_description
#         self.agent = agent
#         self.run_time_prompt = RUN_TIME_PROMPT

#     def _get_dependency(self) -> JDDeps:
#         return JDDeps(job_description=self.job_description)

#     def _create_run_time_prompt(self, ctx: RunContext[JDDeps]) -> str:
#         return f"""{self.run_time_prompt}.

#         JOB DESCRIPTION:
#         {ctx.deps.job_description}"""

#     def _get_prompt(self) -> None:
#         self.agent.system_prompt(self._create_run_time_prompt)

#     async def run_agent(self) -> Json:
#         self._get_prompt()
#         result = await self.agent.run(
#             user_prompt="Execute", deps=self._get_dependency()
#         )
#         result_json = result.output.model_dump_json(indent=2)
#         return result_json
