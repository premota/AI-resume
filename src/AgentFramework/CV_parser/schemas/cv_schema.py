from typing import Literal

from pydantic import BaseModel, Field


EducationLevel = Literal[
    "high_school",
    "associate",
    "bachelor",
    "master",
    "mba",
    "phd",
    "other",
]


class ExperienceEntry(BaseModel):
    job_title: str = Field(description="Job title held in this role.")
    company: str = Field(description="Company or organisation name.")
    duration_months: int = Field(
        description="Duration of employment in months. Compute from start and end dates."
    )
    responsibilities: list[str] = Field(
        description="Key responsibilities, contributions, and measurable achievements in this role."
    )


class EducationEntry(BaseModel):
    institution: str = Field(description="Name of the institution.")
    degree: str = Field(
        description="Full degree name e.g. 'Bachelor of Science in Computer Science'."
    )
    degree_level: EducationLevel = Field(
        description="Normalised degree level. Use 'other' if it does not fit standard levels."
    )
    field_of_study: str = Field(
        description="Field or major e.g. 'Computer Science', 'Business Education'."
    )


class CVOutputSchema(BaseModel):
    candidate_name: str = Field(description="Full name of the candidate.")
    professional_summary: str = Field(
        description="A concise 2–4 sentence summary of the candidate's background, strengths, and career focus."
    )
    professional_experience: list[ExperienceEntry] = Field(
        description="All work experience entries in reverse chronological order."
    )
    total_years_experience: float = Field(
        description="Total years of professional experience derived from all experience entries. Round to one decimal place."
    )
    job_titles: list[str] = Field(
        description="All distinct job titles held across the candidate's career."
    )
    skill_sets: list[str] = Field(
        description=(
            "Exhaustive list of all technical skills, tools, frameworks, and methodologies. "
            "Expand all abbreviations to their full standard form e.g. 'ML' → 'Machine Learning', "
            "'k8s' → 'Kubernetes', 'JS' → 'JavaScript'."
        )
    )
    education: list[EducationEntry] = Field(
        description="All education entries in reverse chronological order."
    )
    highest_education_level: EducationLevel = Field(
        description="The single highest education level achieved across all education entries."
    )
    certifications: list[str] = Field(
        description="All professional certifications, licences, and credentials. Empty list if none.",
        default_factory=list,
    )
    location: str | None = Field(
        default=None,
        description="Candidate's current location or stated location preference. Null if not mentioned.",
    )
