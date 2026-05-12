from pydantic_ai import Agent as PydanticAIAgent

from AgentFramework.AgentFactory.agent_config import AgentConfig
from AgentFramework.AgentFactory.tool_registry import ToolRegistry
from AgentFramework.AgentFactory.agent_config import AgentOutputT, AgentDepsT


class Agent:
    def __init__(self, config: AgentConfig):
        self._agent: PydanticAIAgent[AgentDepsT, AgentOutputT] | None = None  # type: ignore
        self.config = config

    @property
    def initialized(self) -> bool:
        return self._agent is not None

    def _instantiate_agent(self) -> PydanticAIAgent[AgentDepsT, AgentOutputT]:  # type: ignore
        if self.initialized:
            # agent has been initialized before
            assert self._agent is not None
            return self._agent  # type: ignore
        if not self.config:
            raise ValueError("Agent config must be set before instantiating")
        # create pydantic_ai Agent
        self._agent = PydanticAIAgent(
            model=self.config.model,
            system_prompt=self._system_prompt(),
            deps_type=self.config.dep_types,
            output_type=self.config.output,
        )
        # register tools to agent
        self._register_tools()
        return self._agent  # type: ignore

    def _register_tools(self) -> None:
        if not self.initialized:
            raise RuntimeError(
                "Agent must be initialized first before registering tool"
            )

        assert self._agent is not None
        ToolRegistry(agent=self._agent, tool_list=self.config.tool).register_tools()  # type: ignore

    def _system_prompt(self) -> str:
        return f"""
            persona: {self.config.persona}

            Instruction:
            {self.config.prompt}
        """

    def get_agent(self) -> PydanticAIAgent:
        if not self.initialized:
            # instantiate the agent
            self._instantiate_agent()

        assert self._agent is not None
        return self._agent  # type: ignore
