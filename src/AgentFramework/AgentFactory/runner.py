import logging

from pydantic_ai import Agent as PydanticAIAgent

from AgentFramework.AgentFactory.agent_config import AgentDepsT, AgentOutputT
from utils.exception import AgentExecutionError

logger = logging.getLogger(__name__)

async def run_agent(
    agent: PydanticAIAgent[AgentDepsT, AgentOutputT],
    user_prompt: str,
    dependency: AgentDepsT,
    user_instruction: str,
) -> AgentOutputT:
    try:
        logger.info("Running agent with dependencies %s", dependency)
        result = await agent.run(
            user_prompt=user_prompt, deps=dependency, instructions=user_instruction
        )

    except Exception as e:
        logger.exception("Agent run failed")
        raise AgentExecutionError("Agent execution failed") from e
    logger.info("Agent run successful")
    return result.output
