from dataclasses import dataclass
from typing import TypeVar, Callable, Any, Type, Generic

from pydantic_xml import BaseXmlModel


# class ManagePrompt:

#     def get_prompt(self):
#         return 'promopt'


@dataclass
class AgentDeps:
    """
    will be used at runtime to create dependencies that would be injected 
    at execution
    """
    caller_id: int | None = None
    db_connection: str | None = None
    api_key: str | None = None
    


AgentDepsT = TypeVar("AgentDepsT", bound=AgentDeps)
AgentOutputT = TypeVar("AgentOutputT")
Tool = Callable[..., Any]


@dataclass
class AgentConfig(Generic[AgentDepsT, AgentOutputT]):
    """
    Used during Agent definition to create contract for agent
    """
    model: str
    tool: list[Tool]
    persona: str
    prompt: str
    dep_types : Type[AgentDepsT]
    output: Type[AgentOutputT]


# class ResumeStructureConfig(BaseXmlModel):
#     header: str
#     education: str
#     experience: str
#     skills: str
#     projects: str
#     certifications: str
#     publications: str
#     patents: str
#     awards: str
#     memberships: str
#     languages: str
#     interests: str



