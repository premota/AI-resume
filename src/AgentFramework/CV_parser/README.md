# CV Parser

Turns raw CV text into a structured, typed candidate profile ready for downstream matching and evaluation.

---

## What it does

Takes a CV as plain text (or extracts text from a PDF/DOCX), sends it to an LLM agent, and returns a `CVOutputSchema` — a validated Pydantic model with every meaningful signal from the CV normalised and typed.

```
CV bytes (PDF/DOCX)  ──► CVTextExtractor ──► plain text ──► CV Agent ──► CVOutputSchema
CV plain text        ─────────────────────────────────────► CV Agent ──► CVOutputSchema
```

---

## Key files

| File | What it does |
|---|---|
| `schemas/cv_schema.py` | Defines `CVOutputSchema` — the typed output the agent must produce |
| `core/text_extractor.py` | `CVTextExtractor` — converts a PDF or DOCX binary into markdown text using Docling |
| `core/cv_llm.py` | `parse_cv()` — async function that runs the CV agent and returns `CVOutputSchema` |
| `core/cv_factory.py` | `create_cv_agent()` — builds the pydantic-ai agent using AgentFactory |

---

## Output schema

```python
CVOutputSchema(
    candidate_name        # str
    professional_summary  # str — 2–4 sentence summary
    professional_experience  # list of ExperienceEntry (title, company, duration_months, responsibilities)
    total_years_experience   # float — derived from all experience entries
    job_titles            # list[str] — all distinct titles held
    skill_sets            # list[str] — every technical skill, tool, and framework, normalised
    education             # list of EducationEntry (institution, degree, level, field)
    highest_education_level  # Literal["high_school" | "bachelor" | "master" | "phd" | ...]
    certifications        # list[str]
    location              # str | None
)
```

---

## Usage

```python
from AgentFramework.CV_parser.core.cv_factory import create_cv_agent
from AgentFramework.CV_parser.core.cv_llm import parse_cv

cv_agent = create_cv_agent()

parsed_cv = await parse_cv(agent=cv_agent, cv_text="...raw CV text...")

print(parsed_cv.candidate_name)
print(parsed_cv.skill_sets)
print(parsed_cv.total_years_experience)
```

**From a PDF file:**
```python
from docling.document_converter import DocumentConverter
from AgentFramework.CV_parser.core.text_extractor import CVTextExtractor

extractor = CVTextExtractor(converter=DocumentConverter())
cv_text = extractor.extract_in_markdown(cv_bytes)  # cv_bytes = open("cv.pdf", "rb").read()

parsed_cv = await parse_cv(agent=cv_agent, cv_text=cv_text)
```
