from typing import Generic
from dataclasses import dataclass

from AgentFramework.JD_Parser.prompt import RUN_TIME_PROMPT
from pydantic import Json
from pydantic_ai import Agent as PydanticAIAgent

from AgentFramework.AgentFactory.agent_config import AgentDeps
from AgentFramework.JD_Parser.schemas.jd_schema import JDOutputSchema
from pydantic_ai import RunContext


@dataclass(kw_only=True)
class JDDeps(AgentDeps):
    job_description: str


class JobAdsLLM:
    """
    The aim of this class is to manage how an already created agent would be
    used for breaking down job description into very meaningful chunks.

    It would take in the agent and JD dependency clas through DI and use the JD dependency class to
    create a new run time dependency for the agent
    """

    def __init__(
        self,
        job_description: str,
        agent: PydanticAIAgent[JDDeps, JDOutputSchema]
    ):
        self.job_description = job_description
        self.agent = agent
        self.run_time_prompt = RUN_TIME_PROMPT

    def _get_dependency(self) -> JDDeps:
        return JDDeps(job_description=self.job_description)

    def _create_run_time_prompt(self, ctx: RunContext[JDDeps]) -> str:
        return f"""{self.run_time_prompt}.
    
        JOB DESCRIPTION:
        {ctx.deps.job_description}"""

    def _get_prompt(self) -> None:
        self.agent.system_prompt(self._create_run_time_prompt)

    async def run_agent(self) -> Json:
        self._get_prompt()
        result = await self.agent.run(
            user_prompt="Execute", deps=self._get_dependency()
        )
        result_json = result.output.model_dump_json(indent=2)
        return result_json
