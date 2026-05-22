from typing import Generic

from pydantic_ai import Agent as PydanticAIAgent
from AgentFramework.AgentFactory.agent_config import (
    AgentConfig,
    AgentOutputT,
    AgentDepsT,
)
from AgentFramework.AgentFactory.tool_registry import ToolRegistry


class Agent(Generic[AgentDepsT, AgentOutputT]):
    def __init__(self, config: AgentConfig):
        self._agent: PydanticAIAgent[AgentDepsT, AgentOutputT] | None = None
        self.config = config

    @property
    def initialized(self) -> bool:
        return self._agent is not None

    def _instantiate_agent(self) -> PydanticAIAgent[AgentDepsT, AgentOutputT]:
        if self.initialized:
            # agent has been initialized before
            if self._agent is not None:
                return self._agent

        self._agent = PydanticAIAgent(
            model=self.config.model,
            system_prompt=self.config.prompt,
            output_type=self.config.output,
            deps_type=self.config.dep_types,
        )
        # register tools to agent
        self._register_tools()
        return self._agent

    def _register_tools(self) -> None:
        if not self.initialized:
            raise RuntimeError(
                "Agent must be initialized first before registering tool"
            )
        if self._agent is not None:
            ToolRegistry(agent=self._agent, tool_list=self.config.tool).register_tools()  # type: ignore

    def get_agent(self) -> PydanticAIAgent[AgentDepsT, AgentOutputT]:
        if not self.initialized:
            # instantiate the agent
            return self._instantiate_agent()

        if self._agent is not None:
            return self._agent

        raise RuntimeError("Agent initialization invariant broken")