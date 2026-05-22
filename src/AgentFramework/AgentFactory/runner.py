from typing import Any
from pydantic import Json

from pydantic_ai import Agent as PydanticAIAgent
from AgentFramework.AgentFactory.agent_config import AgentDepsT


async def run_agent(
    agent: PydanticAIAgent[AgentDepsT, Any], user_prompt: str, dependency: AgentDepsT
)->Json:
    result = await agent.run(user_prompt=user_prompt, deps=dependency)
    result_json = result.output.model_dump_json(indent=2)
    return result_json
