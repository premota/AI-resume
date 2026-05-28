from pydantic_ai import Agent as PydanticAIAgent

from AgentFramework.AgentFactory.agent import Agent
from AgentFramework.AgentFactory.agent_config import AgentConfig
from AgentFramework.Matcher.core.matcher_llm import MatcherDeps
from AgentFramework.Matcher.schemas.match_schema import MatchOutputSchema
from AgentFramework.prompt import MATCHER_SYSTEM_PROMPT
from utils.settings import settings


def create_matcher_agent() -> PydanticAIAgent[MatcherDeps, MatchOutputSchema]:
    config = AgentConfig(
        model=settings.matcher_model_name,
        prompt=MATCHER_SYSTEM_PROMPT,
        output=MatchOutputSchema,
        dep_types=MatcherDeps,
    )
    return Agent(config).get_agent()
