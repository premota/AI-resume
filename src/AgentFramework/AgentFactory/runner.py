from pydantic_ai import Agent as PydanticAIAgent
from AgentFramework.AgentFactory.agent_config import AgentDepsT, AgentOutputT


async def run_agent(
    agent: PydanticAIAgent[AgentDepsT, AgentOutputT],
    user_prompt: str,
    dependency: AgentDepsT,
    user_instruction: str,
) -> AgentOutputT:
    result = await agent.run(
        user_prompt=user_prompt, deps=dependency, instructions=user_instruction
    )
    agent_result = result.output
    return agent_result
