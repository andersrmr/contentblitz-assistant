from pydantic import BaseModel, Field


class Source(BaseModel):
    title: str = ""
    url: str
    snippet: str = ""
    retrieved_at: str
    source_type: str = "serp"


class Citation(BaseModel):
    url: str
    supporting_claim: str
    source_title: str = ""


class ResearchPacket(BaseModel):
    user_query: str
    search_queries: list[str] = Field(default_factory=list)
    sources: list[Source] = Field(default_factory=list)
    key_findings: list[str] = Field(default_factory=list)
    angles: list[str] = Field(default_factory=list)
    stats_or_quotes: list[str] = Field(default_factory=list)
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
