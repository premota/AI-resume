from typing import Literal

from pydantic import BaseModel, Field, model_validator


class DimensionResult(BaseModel):
    score: float = Field(
        ge=0.0,
        le=1.0,
        description="Match score for this dimension from 0.0 (no match) to 1.0 (perfect match).",
    )
    matched: list[str] = Field(
        description="Specific JD requirements this candidate clearly satisfies."
    )
    missing: list[str] = Field(
        description="Specific JD requirements this candidate does not satisfy."
    )
    reasoning: str = Field(
        description="1–2 sentences explaining the score with direct reference to the input data."
    )


FitVerdict = Literal["strong_fit", "good_fit", "partial_fit", "weak_fit"]

_DIMENSION_WEIGHTS: dict[str, float] = {
    "skills": 35.0,
    "experience": 25.0,
    "responsibilities": 20.0,
    "education": 10.0,
    "certifications": 10.0,
}


class MatchOutputSchema(BaseModel):
    overall_score: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description=(
            "Weighted overall match score 0–100. "
            "Computed automatically from dimension scores — any placeholder value is accepted."
        ),
    )
    recommendation: FitVerdict = Field(
        default="partial_fit",
        description=(
            "Fit verdict derived from overall_score. "
            "Computed automatically — any valid value is accepted as a placeholder."
        ),
    )
    skills: DimensionResult = Field(
        description="Technical and domain skill coverage against JD requirements."
    )
    experience: DimensionResult = Field(
        description="Years of experience and seniority level alignment."
    )
    responsibilities: DimensionResult = Field(
        description="Alignment of past work responsibilities to the role's responsibilities."
    )
    education: DimensionResult = Field(
        description="Education level and field of study match against JD requirements."
    )
    certifications: DimensionResult = Field(
        description="Coverage of mandatory certifications required by the JD."
    )
    strengths: list[str] = Field(
        min_length=2,
        max_length=5,
        description="Top strengths of this candidate for the role, grounded in the data.",
    )
    gaps: list[str] = Field(
        min_length=2,
        max_length=5,
        description="Top actionable gaps relative to the JD, specific enough to act on.",
    )
    summary: str = Field(
        description="2–3 sentence plain-language fit verdict a hiring manager could act on."
    )

    @model_validator(mode="after")
    def _compute_derived_fields(self) -> "MatchOutputSchema":
        self.overall_score = round(
            self.skills.score * _DIMENSION_WEIGHTS["skills"]
            + self.experience.score * _DIMENSION_WEIGHTS["experience"]
            + self.responsibilities.score * _DIMENSION_WEIGHTS["responsibilities"]
            + self.education.score * _DIMENSION_WEIGHTS["education"]
            + self.certifications.score * _DIMENSION_WEIGHTS["certifications"],
            1,
        )
        score = self.overall_score
        if score >= 80:
            self.recommendation = "strong_fit"
        elif score >= 65:
            self.recommendation = "good_fit"
        elif score >= 45:
            self.recommendation = "partial_fit"
        else:
            self.recommendation = "weak_fit"
        return self
