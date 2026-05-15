from pydantic import BaseModel, Field

class JDOutputSchema(BaseModel):
    job_title: str = Field(description="The title of the job position.")
    job_level: str = Field(description="The level of the job position.")
    responsibility: str = Field(description="The responsibilities of the job position.")
    professional_skills: list[str] = Field(description="The professional skills required for the job position.")
    domain_skills: list[str] = Field(description="The domain skills required for the job position.")
    nice_to_have_skills: list[str] = Field(description="The nice-to-have skills for the job position.") 
    years_of_experience: int | None = Field(description="The number of years of experience required for the job position.")
    location: list[str] = Field(description="The locations where the job is available.")
    educational_qualification: str = Field(description="The educational qualification required for the job position.")
    mandatory_certifications: list[str] = Field(description="The mandatory certifications required for the job position.")
    nice_to_have_certifications: list[str] = Field(description="The nice-to-have certifications for the job position.")