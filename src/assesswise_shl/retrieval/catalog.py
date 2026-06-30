import json
from pathlib import Path

from pydantic import BaseModel, Field, HttpUrl


class CatalogRecord(BaseModel):
    assessment_name: str = Field(min_length=1)
    url: HttpUrl
    test_type: list[str] = Field(min_length=1)
    description: str = ""
    duration_minutes: int | None = Field(default=None, ge=1)
    remote_testing: bool | None = None
    role_families: list[str] = Field(default_factory=list)
    skill_domains: list[str] = Field(default_factory=list)
    seniority: list[str] = Field(default_factory=list)

    def searchable_text(self) -> str:
        fields = [
            self.assessment_name,
            self.description,
            " ".join(self.test_type),
            " ".join(self.role_families),
            " ".join(self.skill_domains),
            " ".join(self.seniority),
        ]
        return " ".join(field for field in fields if field).lower()


class Catalog:
    def __init__(self, records: list[CatalogRecord]) -> None:
        self.records = records

    @classmethod
    def load(cls, path: Path) -> "Catalog":
        if not path.exists():
            return cls(records=[])

        with path.open("r", encoding="utf-8") as file:
            payload = json.load(file)

        records = [CatalogRecord.model_validate(item) for item in payload]
        return cls(records=records)

