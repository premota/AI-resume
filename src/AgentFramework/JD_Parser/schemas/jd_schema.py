from typing import Literal

from pydantic import BaseModel, Field


SeniorityLevel = Literal[
    "intern",
    "junior",
    "mid",
    "senior",
    "lead",
    "principal",
    "manager",
    "director",
    "other",
]

EmploymentType = Literal[
    "full_time",
    "part_time",
    "contract",
    "temporary",
    "internship",
    "other",
]

WorkArrangement = Literal[
    "onsite",
    "hybrid",
    "remote",
]

EducationLevel = Literal[
    "high_school",
    "associate",
    "bachelor",
    "master",
    "mba",
    "phd",
    "other",
]


class EducationRequirement(BaseModel):
    degree_level: EducationLevel = Field(
        description="Minimum degree level required."
    )
    field_of_study: str | None = Field(
        default=None,
        description="Required field of study. Null if any field is acceptable.",
    )


class JDOutputSchema(BaseModel):
    job_title: str = Field(description="The primary title of the job position.")
    alternate_job_titles: list[str] = Field(
        description="Common alternative titles used for the same role e.g. 'Software Engineer' for 'Software Developer'. Empty list if none.",
        default_factory=list,
    )
    seniority_level: SeniorityLevel = Field(
        description=(
            "Seniority level of the position. "
            "Infer from title and requirements if not explicitly stated."
        )
    )
    industry: str | None = Field(
        default=None,
        description="Industry or sector the role belongs to e.g. 'FinTech', 'Healthcare', 'E-commerce'. Null if not determinable.",
    )
    employment_type: EmploymentType | None = Field(
        default=None,
        description="Type of employment contract. Null if not specified.",
    )
    work_arrangement: WorkArrangement | None = Field(
        default=None,
        description="Work location arrangement. Null if not specified.",
    )
    responsibilities: list[str] = Field(
        description="Key responsibilities of the role. One action-verb sentence per item."
    )
    professional_skills: list[str] = Field(
        description=(
            "Required technical skills, tools, frameworks, and technologies. "
            "Expand all abbreviations to their full standard form e.g. 'ML' → 'Machine Learning', "
            "'k8s' → 'Kubernetes', 'JS' → 'JavaScript'."
        )
    )
    domain_skills: list[str] = Field(
        description="Required domain or industry-specific knowledge e.g. 'Financial Modelling', 'Clinical Trials'."
    )
    soft_skills: list[str] = Field(
        description="Required or strongly preferred soft skills and behavioural competencies e.g. 'Communication', 'Team Leadership'. Empty list if none.",
        default_factory=list,
    )
    nice_to_have_skills: list[str] = Field(
        description="Preferred but not required skills. Empty list if none.",
        default_factory=list,
    )
    years_of_experience: int | None = Field(
        default=None,
        description="Minimum years of professional experience required. Null if not specified.",
    )
    education_requirement: EducationRequirement | None = Field(
        default=None,
        description="Minimum education level and optional field of study required. Null if not specified.",
    )
    mandatory_certifications: list[str] = Field(
        description="Certifications explicitly required for the role. Empty list if none.",
        default_factory=list,
    )
    nice_to_have_certifications: list[str] = Field(
        description="Certifications that are preferred but not required. Empty list if none.",
        default_factory=list,
    )
    location: list[str] = Field(
        description="Locations where the job is available. Empty list if fully remote with no location constraint."
    )
    
