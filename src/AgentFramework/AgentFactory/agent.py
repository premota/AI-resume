from typing import Generic

from pydantic_ai import Agent as PydanticAIAgent
from AgentFramework.AgentFactory.agent_config import (
    AgentConfig,
    AgentOutputT,
    AgentDepsT,
)
from AgentFramework.AgentFactory.tool_registry import ToolRegistry
from utils.exception import AgentInitializationError, ToolRegistryError


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
        try:
            temp_agent = PydanticAIAgent(
                model=self.config.model,
                system_prompt=self.config.prompt,
                output_type=self.config.output,
                deps_type=self.config.dep_types,
            )
        except Exception as e:
            raise AgentInitializationError("Agent failed to initialize") from e

        # register tools to agent
        self._register_tools(temp_agent)

        self._agent = temp_agent
        return self._agent

    def _register_tools(self, agent: PydanticAIAgent) -> None:
        try:
            ToolRegistry(agent=agent, tool_list=self.config.tool).register_tools()
        except Exception as e:
            raise ToolRegistryError("Tools failed to register") from e

    def get_agent(self) -> PydanticAIAgent[AgentDepsT, AgentOutputT]:
        if self._agent is None:
            return self._instantiate_agent()
        return self._agent
