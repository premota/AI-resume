# Matcher

Compares a parsed CV against a parsed job description and produces a scored, evidence-based match report.

---

## What it does

Takes the structured outputs of the CV and JD parsers, sends them to a Claude Haiku agent, and returns a `MatchOutputSchema` — a detailed report showing how well the candidate fits the role across five dimensions, with matched/missing items and reasoning for each.

```
CVOutputSchema  ──┐
                   ├──► Matcher Agent (Claude Haiku) ──► MatchOutputSchema
JDOutputSchema  ──┘
```

The overall score and fit verdict are **computed by Python** from the dimension scores — not by the LLM — so they are always consistent and auditable.

---

## Key files

| File | What it does |
|---|---|
| `schemas/match_schema.py` | Defines `DimensionResult` and `MatchOutputSchema`; contains the scoring weights and the validator that computes `overall_score` and `recommendation` |
| `core/matcher_llm.py` | `match_cv_to_jd()` — async function that runs the matcher agent; accepts an optional `temperature` override |
| `core/matcher_factory.py` | `create_matcher_agent()` — builds the pydantic-ai agent using AgentFactory |

---

## Scoring

Five dimensions are evaluated, each scored 0.0 – 1.0 by the LLM:

| Dimension | Weight | What is evaluated |
|---|---|---|
| Skills | 35% | `cv.skill_sets` vs `jd.professional_skills` + `jd.domain_skills` |
| Experience | 25% | Years of experience and seniority level |
| Responsibilities | 20% | Past work alignment to the role's responsibilities |
| Education | 10% | Degree level vs requirement |
| Certifications | 10% | Mandatory certs held vs required |

`overall_score = skills×35 + experience×25 + responsibilities×20 + education×10 + certifications×10`

| Score range | Verdict |
|---|---|
| 80 – 100 | `strong_fit` |
| 65 – 79 | `good_fit` |
| 45 – 64 | `partial_fit` |
| 0 – 44 | `weak_fit` |

---

## Output schema

```python
MatchOutputSchema(
    overall_score     # float 0–100, computed from dimension scores
    recommendation    # "strong_fit" | "good_fit" | "partial_fit" | "weak_fit"
    skills            # DimensionResult(score, matched, missing, reasoning)
    experience        # DimensionResult(...)
    responsibilities  # DimensionResult(...)
    education         # DimensionResult(...)
    certifications    # DimensionResult(...)
    strengths         # list[str] — top 2–5 reasons this candidate is strong for the role
    gaps              # list[str] — top 2–5 actionable gaps
    summary           # str — 2–3 sentence plain-language verdict
)
```

---

## Usage

```python
from AgentFramework.Matcher.core.matcher_factory import create_matcher_agent
from AgentFramework.Matcher.core.matcher_llm import match_cv_to_jd

matcher_agent = create_matcher_agent()

result = await match_cv_to_jd(
    agent=matcher_agent,
    cv=parsed_cv,    # CVOutputSchema from the CV parser
    jd=parsed_jd,    # JDOutputSchema from the JD parser
)

print(result.overall_score)    # e.g. 72.5
print(result.recommendation)  # e.g. "good_fit"
print(result.gaps)             # list of specific gaps to address
```

**Adjusting temperature** — lower for more consistent scores, higher for more varied reasoning:
```python
result = await match_cv_to_jd(agent=matcher_agent, cv=parsed_cv, jd=parsed_jd, temperature=0.0)
```

Temperature defaults to `matcher_temperature` in `settings.py` (currently `0.1`).

---

## Adding tools

Because the matcher is built on AgentFactory, tools can be plugged in at creation time:

```python
from AgentFramework.AgentFactory.agent_config import AgentConfig
from AgentFramework.AgentFactory.agent import Agent

def normalise_skill(ctx, skill: str) -> str:
    # e.g. map "k8s" → "Kubernetes"
    ...

config = AgentConfig(
    model=settings.matcher_model_name,
    prompt=MATCHER_SYSTEM_PROMPT,
    output=MatchOutputSchema,
    dep_types=MatcherDeps,
    tool=[normalise_skill],
)
matcher_agent = Agent(config).get_agent()
```
