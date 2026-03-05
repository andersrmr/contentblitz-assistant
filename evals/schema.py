from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, model_validator


class EvalCaseInputs(BaseModel):
    intent: str
    topic: str | None = None
    user_query: str | None = None
    audience: str
    platform: str
    constraints: dict[str, Any] = Field(default_factory=dict)
    revision_request: str | None = None

    @model_validator(mode="after")
    def validate_query_input(self) -> "EvalCaseInputs":
        if not (self.topic or self.user_query):
            raise ValueError("Eval case inputs require at least one of topic or user_query.")
        return self


class SerpFixtureItem(BaseModel):
    title: str
    url: str
    snippet: str = ""


class EvalCaseFixtures(BaseModel):
    serp_fixture: list[SerpFixtureItem] = Field(default_factory=list)
    stubbed_node_outputs: dict[str, dict[str, Any]] = Field(default_factory=dict)


class EvalCaseExpectations(BaseModel):
    max_iterations: int = 2
    require_citation_precision: bool = True
    require_headline_compliance: bool = True
    require_cta_presence: bool = True
    require_skim_format: bool = True


class EvalCase(BaseModel):
    case_id: str
    description: str = ""
    inputs: EvalCaseInputs
    fixtures: EvalCaseFixtures
    expectations: EvalCaseExpectations = Field(default_factory=EvalCaseExpectations)


class GoldenManifest(BaseModel):
    golden_set_version: str
    description: str
    cases: list[str]

