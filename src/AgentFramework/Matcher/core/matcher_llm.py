import logging
from dataclasses import dataclass

from pydantic_ai import Agent as PydanticAIAgent
from pydantic_ai.settings import ModelSettings

from AgentFramework.AgentFactory.agent_config import AgentDeps
from AgentFramework.CV_parser.schemas.cv_schema import CVOutputSchema
from AgentFramework.JD_Parser.schemas.jd_schema import JDOutputSchema
from AgentFramework.Matcher.schemas.match_schema import MatchOutputSchema
from AgentFramework.prompt import MATCHER_RUNTIME_PROMPT
from utils.exception import AgentExecutionError
from utils.settings import settings

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class MatcherDeps(AgentDeps):
    cv: CVOutputSchema
    jd: JDOutputSchema


def _build_instruction(cv: CVOutputSchema, jd: JDOutputSchema, runtime_prompt: str) -> str:
    return f"""{runtime_prompt}

CANDIDATE PROFILE:
{cv.model_dump_json(indent=2)}

JOB DESCRIPTION:
{jd.model_dump_json(indent=2)}
"""


async def match_cv_to_jd(
    agent: PydanticAIAgent[MatcherDeps, MatchOutputSchema],
    cv: CVOutputSchema,
    jd: JDOutputSchema,
    runtime_prompt: str = MATCHER_RUNTIME_PROMPT,
    temperature: float = settings.matcher_temperature,
) -> MatchOutputSchema:
    deps = MatcherDeps(cv=cv, jd=jd)
    instruction = _build_instruction(cv=cv, jd=jd, runtime_prompt=runtime_prompt)

    try:
        logger.info(
            "Starting match evaluation — candidate: %s | role: %s",
            cv.candidate_name,
            jd.job_title,
        )
        result = await agent.run(
            user_prompt="execute",
            deps=deps,
            instructions=instruction,
            model_settings=ModelSettings(temperature=temperature),
        )
    except Exception as e:
        logger.exception(
            "Match evaluation failed — candidate: %s | role: %s",
            cv.candidate_name,
            jd.job_title,
        )
        raise AgentExecutionError("Match evaluation failed") from e

    output = result.output
    logger.info(
        "Match evaluation complete — candidate: %s | role: %s | score: %.1f | verdict: %s",
        cv.candidate_name,
        jd.job_title,
        output.overall_score,
        output.recommendation,
    )
    return output
