from dataclasses import dataclass

from assesswise_shl.retrieval.catalog import Catalog, CatalogRecord


@dataclass(frozen=True)
class RetrievalQuery:
    text: str
    test_types: set[str] | None = None
    role_families: set[str] | None = None
    skill_domains: set[str] | None = None
    limit: int = 10


@dataclass(frozen=True)
class RetrievalResult:
    record: CatalogRecord
    score: float
    reasons: list[str]


class HybridRetriever:
    def __init__(self, catalog: Catalog) -> None:
        self.catalog = catalog

    def search(self, query: RetrievalQuery) -> list[RetrievalResult]:
        candidates = self._structured_filter(query)
        ranked = sorted(
            (self._score(record, query) for record in candidates),
            key=lambda result: result.score,
            reverse=True,
        )
        return ranked[: query.limit]

    def _structured_filter(self, query: RetrievalQuery) -> list[CatalogRecord]:
        records = self.catalog.records

        if query.test_types:
            records = [
                record
                for record in records
                if query.test_types.intersection({code.upper() for code in record.test_type})
            ]

        if query.role_families:
            records = [
                record
                for record in records
                if query.role_families.intersection(set(record.role_families))
            ]

        if query.skill_domains:
            records = [
                record
                for record in records
                if query.skill_domains.intersection(set(record.skill_domains))
            ]

        return records

    def _score(self, record: CatalogRecord, query: RetrievalQuery) -> RetrievalResult:
        query_terms = set(query.text.lower().split())
        record_terms = set(record.searchable_text().split())
        overlap = query_terms.intersection(record_terms)
        score = float(len(overlap))
        reasons = [f"matched term: {term}" for term in sorted(overlap)]

        if query.test_types:
            score += 2.0
            reasons.append("matched explicit test type filter")
        if query.role_families:
            score += 1.5
            reasons.append("matched role family filter")
        if query.skill_domains:
            score += 1.5
            reasons.append("matched skill domain filter")

        return RetrievalResult(record=record, score=score, reasons=reasons)

