# Job AI

An AI-powered pipeline that reads a CV and a job description, extracts structured data from both, and tells you how well the candidate fits the role — with traceable reasoning, not just a number.

---

## What it does

```
CV (PDF / text)  ──► CV Agent  ──► structured candidate profile  ──┐
                                                                     ├──► Matcher Agent ──► fit score + gaps + strengths
JD (text)        ──► JD Agent  ──► structured job requirements   ──┘
```

1. **CV Agent** — reads raw CV text and extracts skills, experience, education, certifications, and a professional summary into a typed schema.
2. **JD Agent** — reads a raw job posting and extracts required skills, experience threshold, seniority level, education requirement, and certifications into a typed schema.
3. **Matcher Agent** — compares the two schemas and produces a match score (0–100), a fit verdict, per-dimension reasoning, the candidate's top strengths, and their top gaps.

---

## Project layout

```
src/
└── AgentFramework/
    ├── AgentFactory/    # Base building block — creates and runs pydantic-ai agents
    ├── CV_parser/       # Extracts structured data from a CV
    ├── JD_Parser/       # Extracts structured data from a job description
    └── Matcher/         # Compares CV output vs JD output and scores the match
```

---

## Setup

**1. Install dependencies**
```bash
uv sync
```

**2. Add API keys to `.env` in the project root**
```
MODEL_NAME=groq:openai/gpt-oss-120b   # model used by CV + JD agents
GROQ_API_KEY=...                       # key for the model above
ANTHROPIC_API_KEY=...                  # used by the Matcher agent (Claude Haiku)
```

---

## Components

| Component | README |
|---|---|
| AgentFactory | [AgentFactory/README.md](src/AgentFramework/AgentFactory/README.md) |
| CV Parser | [CV_parser/README.md](src/AgentFramework/CV_parser/README.md) |
| JD Parser | [JD_Parser/README.md](src/AgentFramework/JD_Parser/README.md) |
| Matcher | [Matcher/README.md](src/AgentFramework/Matcher/README.md) |
