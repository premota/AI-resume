from typing import Generic
from dataclasses import dataclass

from pydantic import Json
from pydantic_ai import Agent as PydanticAIAgent

from AgentFramework.AgentFactory.agent_config import ( 
    AgentDeps,
    AgentDepsT,
    AgentOutputT
)
from AgentFramework.JD_Parser.schemas.jd_schema import JDOutputSchema
from pydantic_ai import RunContext


@dataclass
class JDDeps(AgentDeps):
    job_description: str


class JobAdsLLM(Generic[AgentDepsT, AgentOutputT]):
    """
    The aim of this class is to manage how an already created agent would be
    used for breaking down job description into very meaningful chunks.

    It would take in the agent and JD dependency clas through DI and use the JD dependency class to
    create a new run time dependency for the agent
    """

    def __init__(
        self,
        job_description: str,
        agent: PydanticAIAgent[JDDeps, JDOutputSchema],
        jd_dependency: JDDeps,
        run_time_prompt: str,
    ):
        self.job_description = job_description
        self.agent = agent
        self.jd_dependency = jd_dependency
        self.run_time_prompt = run_time_prompt

    def _get_dependency(self) -> JDDeps:
        return JDDeps(job_description=self.job_description)

    def _create_run_time_prompt(self, ctx: RunContext[JDDeps]) -> str:
        return f"""{self.run_time_prompt}.
        
        JOB DESCRIPTION:
        {ctx.deps.job_description}"""

    def _get_prompt(self) -> None:
        self.agent.system_prompt(self._create_run_time_prompt)

    async def run_agent(self)->Json:
        self._get_prompt()
        result = await self.agent.run(user_prompt="", deps=self._get_dependency())
        result_json = result.output.model_dump_json(indent=2)
        return result_json