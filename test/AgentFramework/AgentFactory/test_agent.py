import pytest
from unittest.mock import patch, MagicMock

from AgentFramework.AgentFactory.agent import Agent
from AgentFramework.AgentFactory.agent_config import AgentConfig, AgentDeps


class TestAgentFactory:
    @pytest.fixture
    def get_agent_config(self):
        def dummy_tool():
            pass

        return AgentConfig(
            model="gpt-4o",
            tool=[dummy_tool],
            persona="Travis agent",
            prompt="prompt",
            dep_types=AgentDeps,
            output=str,
        )

    @pytest.fixture
    def get_agent_class(self, get_agent_config):
        return Agent(config=get_agent_config)

    @patch("AgentFramework.AgentFactory.agent.PydanticAIAgent")
    def test_get_agent_initializes_agent_on_first_call(
        self, mock_pydantic_cls, get_agent_class
    ):
        inner = MagicMock()
        mock_pydantic_cls.return_value = inner

        agent = get_agent_class
        assert agent.initialized is False
        returned_agent = agent.get_agent()
        assert agent.initialized is True
        assert returned_agent is inner
        mock_pydantic_cls.assert_called_once()

    @patch("AgentFramework.AgentFactory.agent.PydanticAIAgent")
    def test_pydantic_ai_agent_receives_expected_constructor_kwargs(
        self, mock_pydantic_cls, get_agent_class
    ):
        mock_pydantic_cls.return_value = MagicMock()

        agent = get_agent_class
        agent.get_agent()

        mock_pydantic_cls.assert_called_once()
        kwargs = mock_pydantic_cls.call_args.kwargs
        assert kwargs["model"] == agent.config.model
        assert kwargs["deps_type"] == AgentDeps
        assert kwargs["output_type"] is str
        assert agent.config.persona in kwargs["system_prompt"]
        assert agent.config.prompt in kwargs["system_prompt"]

    @patch("AgentFramework.AgentFactory.agent.PydanticAIAgent")
    def test_get_agent_reuses_existing_initialized_agent(
        self, mock_pydantic_cls, get_agent_class
    ):
        inner = MagicMock()
        mock_pydantic_cls.return_value = inner

        agent = get_agent_class
        assert agent.initialized is False
        first_agent = agent.get_agent()
        assert agent.initialized is True

        second_agent = agent.get_agent()
        assert first_agent is second_agent
        assert first_agent is inner
        mock_pydantic_cls.assert_called_once()

    def test_get_agent_raises_when_config_missing(self):
        agent = Agent(None)  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="Agent config must be set before instantiating"):
            agent.get_agent()

    def test_instantiate_agent_raises_when_config_missing(self):
        agent = Agent(None)  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="Agent config must be set before instantiating"):
            agent._instantiate_agent()

    def test_register_tools_raises_when_agent_not_initialized(self, get_agent_config):
        agent = Agent(config=get_agent_config)
        with pytest.raises(RuntimeError, match="Agent must be initialized first"):
            agent._register_tools()

    @patch("AgentFramework.AgentFactory.agent.PydanticAIAgent")
    @patch("AgentFramework.AgentFactory.agent.ToolRegistry")
    def test_tool_registry_calls_register_tools(
        self, mock_tool_registry_cls, mock_pydantic_agent_cls, get_agent_class
    ):
        mock_inner_agent = MagicMock()
        mock_pydantic_agent_cls.return_value = mock_inner_agent
        mock_registry = MagicMock()
        mock_tool_registry_cls.return_value = mock_registry

        agent = get_agent_class
        agent.get_agent()
        mock_tool_registry_cls.assert_called_once_with(
            agent=mock_inner_agent,
            tool_list=agent.config.tool,
        )
        mock_registry.register_tools.assert_called_once()
