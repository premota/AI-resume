from AgentFramework.AgentFactory.agent import Agent
from AgentFramework.AgentFactory.agent_config import AgentConfig
from AgentFramework.CV_parser.core.cv_llm import CVDeps
from AgentFramework.CV_parser.schemas.cv_schema import CVOutputSchema
from AgentFramework.prompt import CV_SYSTEM_PROMPT
from pydantic_ai import Agent as PydanticAIAgent
from utils.settings import settings

def create_cv_agent()->PydanticAIAgent[CVDeps, CVOutputSchema]:
    config = AgentConfig(
        model=settings.model_name,
        prompt=CV_SYSTEM_PROMPT,
        output=CVOutputSchema,
        dep_types=CVDeps,
    )
    return Agent(config).get_agent()