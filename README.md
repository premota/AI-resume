# Job AI

Flexible, extensible AI-assisted flows for resume/JD parsing, matching, and targeted resume suggestions (Python, pydantic-ai).

## Architecture diagrams

Diagrams live in the repo root as SVG (renders in GitHub and most browsers). Mermaid sources (`.mmd`) are included if you want PNG/PDF via [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli) or [Kroki](https://kroki.io/).

| Diagram | SVG (primary) | Mermaid source |
|--------|-----------------|----------------|
| High-level system | [high-level-system.svg](./high-level-system.svg) | [high-level-system.mmd](./high-level-system.mmd) |
| Low-level packages | [low-level-system.svg](./low-level-system.svg) | [low-level-system.mmd](./low-level-system.mmd) |
| MVP extraction sequence | [mvp-sequence.svg](./mvp-sequence.svg) | [mvp-sequence.mmd](./mvp-sequence.mmd) |

![High-level system](./high-level-system.svg)

![Low-level packages](./low-level-system.svg)

![MVP extraction sequence](./mvp-sequence.svg)

## Execution tickets (MVP backlog)

| ID | Title | Description | Acceptance criteria |
|----|--------|-------------|---------------------|
| **T1** | Pin package layout and fix test mocks | Choose one import root under `src` and ensure pytest patches use the real module path (`AgentFramework.AgentFactory.agent`, not `src.AgentFactory...`). Align `PYTHONPATH` / packaging if needed. | `pytest` passes; mocks attach to imported symbols. |
| **T2** | Sample fixtures | Add `fixtures/resume_sample.txt` and `fixtures/jd_sample.txt` with minimal realistic content. | Fixtures committed; referenced by tests or smoke script. |
| **T3** | Resume extraction | Implement thin helper using `Agent` with `output_type=ResumeStructureConfig` and a dedicated extraction prompt. | Tests mock LLM / validate structured output parsing. |
| **T4** | JD extraction | Same pattern for `JobDescriptionStructureConfig`; optional public entry `JD_Parser/read_jd.py` delegating to the agent. | Same as T3 for JD model. |
| **T5** | Matching preprocessor | `normalize_for_matching(text: str) -> str` wrapping `CleanText`; document case-folding policy for scoring vs display. | Unit tests + documented behavior. |
| **T6** | MVP matcher | Pure functions: structured resume + JD → `{score, matched_terms, missing_terms}` without embeddings. | Deterministic tests on fixed structures. |
| **T7** | Suggestions model | Return structured edit proposals (section, rationale, suggested text), not full DOCX rewrite in MVP. | Pydantic-validated output; mock-friendly tests. |
| **T8** | End-to-end driver | CLI entry (e.g. `python -m ...` or `scripts/run_mvp.py`): fixtures → normalize → extract → match → JSON stdout. | One command prints full pipeline output. |
| **T9** | Optional HTTP API | FastAPI `POST /analyze` with `{resume_text, jd_text}` returning JSON bundle. | Works locally via curl; auth out of scope. |

**Suggested order:** T1 → T2 → (T3 ∥ T4) → T5 → T6 → T7 → T8 → T9.

## Development

- Python: see `.python-version` and `pyproject.toml`.
- Install: use `uv sync` (or your preferred env manager).
- Tests: `pytest`.
