# JD Parser

Turns a raw job description into a structured, typed set of hiring requirements ready for candidate evaluation.

---

## What it does

Takes a job posting as plain text, sends it to an LLM agent, and returns a `JDOutputSchema` — a validated Pydantic model with every requirement normalised: required skills, experience threshold, seniority level, education, certifications, and more.

```
Job posting text ──► JD Agent ──► JDOutputSchema
```

---

## Key files

| File | What it does |
|---|---|
| `schemas/jd_schema.py` | Defines `JDOutputSchema` — the typed output the agent must produce |
| `core/jd_llm.py` | `parse_jd()` — async function that runs the JD agent and returns `JDOutputSchema` |
| `core/jd_factory.py` | `create_jd_agent()` — builds the pydantic-ai agent using AgentFactory |

---

## Output schema

```python
JDOutputSchema(
    job_title                  # str
    alternate_job_titles       # list[str]
    seniority_level            # Literal["intern" | "junior" | "mid" | "senior" | "lead" | ...]
    industry                   # str | None
    employment_type            # Literal["full_time" | "part_time" | "contract" | ...] | None
    work_arrangement           # Literal["onsite" | "hybrid" | "remote"] | None
    responsibilities           # list[str] — what the person will do
    professional_skills        # list[str] — required technical skills and tools, normalised
    domain_skills              # list[str] — required industry or domain knowledge
    soft_skills                # list[str]
    nice_to_have_skills        # list[str] — preferred but not required
    years_of_experience        # int | None — minimum years required
    education_requirement      # EducationRequirement(degree_level, field_of_study) | None
    mandatory_certifications   # list[str] — required certs
    nice_to_have_certifications  # list[str]
    location                   # list[str]
)
```

---

## Usage

```python
from AgentFramework.JD_Parser.core.jd_factory import create_jd_agent
from AgentFramework.JD_Parser.core.jd_llm import parse_jd

jd_agent = create_jd_agent()

parsed_jd = await parse_jd(agent=jd_agent, jd="...raw job description text...")

print(parsed_jd.job_title)
print(parsed_jd.seniority_level)
print(parsed_jd.professional_skills)
print(parsed_jd.years_of_experience)
```
