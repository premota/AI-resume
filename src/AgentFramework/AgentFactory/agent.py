from typing import Generic
import logging

from pydantic_ai import Agent as PydanticAIAgent
from AgentFramework.AgentFactory.agent_config import (
    AgentConfig,
    AgentOutputT,
    AgentDepsT,
)
from AgentFramework.AgentFactory.tool_registry import ToolRegistry
from utils.exception import AgentInitializationError, ToolRegistryError

logger = logging.getLogger(__name__)

class Agent(Generic[AgentDepsT, AgentOutputT]):
    def __init__(self, config: AgentConfig):
        self._agent: PydanticAIAgent[AgentDepsT, AgentOutputT] | None = None
        self.config = config

    @property
    def initialized(self) -> bool:
        return self._agent is not None

    def _instantiate_agent(self) -> PydanticAIAgent[AgentDepsT, AgentOutputT]:
        if self._agent is not None:
            return self._agent
        logger.info("Instantiating pydantic Agent with model config: %s", self.config)
        try:
            temp_agent = PydanticAIAgent(
                model=self.config.model,
                system_prompt=self.config.prompt,
                output_type=self.config.output,
                deps_type=self.config.dep_types,
            )
        except Exception as e:
            logger.exception("Agent initialization failed")
            raise AgentInitializationError("Agent failed to initialize") from e

        # register tools to agent
        self._register_tools(temp_agent)
        logger.info("Agent initialization complete")
        self._agent = temp_agent
        return self._agent

    def _register_tools(self, agent: PydanticAIAgent) -> None:
        try:
            logger.info("Registering tools %s", self.config.tool)
            ToolRegistry(agent=agent, tool_list=self.config.tool).register_tools()
        except Exception as e:
            logger.exception("Tool registration failed")
            raise ToolRegistryError("Tools failed to register") from e
        logger.info("Tool registration complete")

    def get_agent(self) -> PydanticAIAgent[AgentDepsT, AgentOutputT]:
        if self._agent is None:
            return self._instantiate_agent()
        return self._agent
