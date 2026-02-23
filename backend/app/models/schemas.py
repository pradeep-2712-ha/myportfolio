from pydantic import BaseModel, Field


class SkillOut(BaseModel):
    name: str
    level: str
    category: str


class ProjectOut(BaseModel):
    id: int
    title: str
    summary: str
    stack: list[str]
    link: str


class ExperienceOut(BaseModel):
    id: int
    role: str
    company: str
    period: str
    highlights: list[str]


class EducationOut(BaseModel):
    degree: str
    institution: str
    year: str


class CertificationOut(BaseModel):
    name: str
    issuer: str
    year: str


class PortfolioOut(BaseModel):
    name: str
    title: str
    tagline: str
    about: str
    contact_email: str
    phone: str
    location: str
    linkedin_url: str
    github_url: str
    skills: list[SkillOut]
    projects: list[ProjectOut]
    experience: list[ExperienceOut]
    education: list[EducationOut]
    certifications: list[CertificationOut]


class ChatMessage(BaseModel):
    role: str = Field(pattern="^(user|assistant)$")
    content: str = Field(min_length=1, max_length=2000)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    history: list[ChatMessage] = Field(default_factory=list)


class ChatResponse(BaseModel):
    answer: str
