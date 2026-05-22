from AgentFramework.AgentFactory.agent import Agent
from AgentFramework.AgentFactory.agent_config import AgentConfig
from AgentFramework.JD_Parser.core.jd_llm import JDDeps
from AgentFramework.prompt import JD_SYSTEM_PROMPT
from AgentFramework.JD_Parser.schemas.jd_schema import JDOutputSchema
from pydantic_ai import Agent as PydanticAIAgent
from utils.config import Settings


def create_jd_agent() -> PydanticAIAgent[JDDeps, JDOutputSchema]:
    config = AgentConfig(
        model=Settings().model_name,
        prompt=JD_SYSTEM_PROMPT,
        output=JDOutputSchema,
        dep_types=JDDeps,
    )
    return Agent(config).get_agent()
