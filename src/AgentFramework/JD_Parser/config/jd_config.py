from pydantic_xml import BaseXmlModel


class JobDescriptionStructureConfig(BaseXmlModel):
    job_header: str
    job_description: str
    job_main_requirements: str
    job_nice_to_have: str | None = None
    job_technical_skill: str
    job_responsibilities: str
    job_qualifications: str
    job_location: str
    job_about_company: str | None = None
