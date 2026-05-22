from pydantic import BaseModel


class CVOutputSchema(BaseModel):
    candidate_name: str
    professional_summary: str
    professional_experience: str
    job_title: list[str]
    skill_sets: list[str]
    education: str
