from pydantic_ai import Agent as PydanticAIAgent

from AgentFramework.AgentFactory.agent_config import AgentDepsT, AgentOutputT
from utils.exception import AgentExecutionError


async def run_agent(
    agent: PydanticAIAgent[AgentDepsT, AgentOutputT],
    user_prompt: str,
    dependency: AgentDepsT,
    user_instruction: str,
) -> AgentOutputT:
    try:
        result = await agent.run(
            user_prompt=user_prompt, deps=dependency, instructions=user_instruction
        )

    except Exception as e:
        raise AgentExecutionError("Agent execution failed") from e
    return result.output
