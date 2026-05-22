from dataclasses import dataclass, field
from typing import TypeVar, Callable, Any, Type, Generic


@dataclass(kw_only=True)
class AgentDeps:
    """
    will be used at runtime to create dependencies that would be injected
    at execution
    """

    # caller_id: int | None = None
    # db_connection: str | None = None
    # api_key: str | None = None


AgentDepsT = TypeVar("AgentDepsT", bound=AgentDeps)
AgentOutputT = TypeVar("AgentOutputT")
Tool = Callable[..., Any]


@dataclass
class AgentConfig(Generic[AgentDepsT, AgentOutputT]):
    """
    Used during Agent definition to create contract for agent
    """

    model: str
    prompt: str
    output: Type[AgentOutputT]
    dep_types: Type[AgentDepsT]
    tool: list[Tool] = field(default_factory=list)
