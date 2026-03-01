from pydantic import BaseModel, Field


class Source(BaseModel):
    title: str
    url: str
    summary: str


class Citation(BaseModel):
    source_title: str
    source_url: str
    note: str


class ResearchPacket(BaseModel):
    topic: str
    audience: str
    summary: str
    key_points: list[str] = Field(default_factory=list)
    sources: list[Source] = Field(default_factory=list)
    citations: list[Citation] = Field(default_factory=list)


class ContentBrief(BaseModel):
    topic: str
    audience: str
    objective: str
    channel: str
    angle: str
    outline: list[str] = Field(default_factory=list)
    cta: str


class Draft(BaseModel):
    channel: str
    headline: str
    body: str
    cta: str
    citations: list[Citation] = Field(default_factory=list)


class QualityReport(BaseModel):
    passed: bool
    score: int
    checks: dict[str, bool]
    feedback: list[str] = Field(default_factory=list)
