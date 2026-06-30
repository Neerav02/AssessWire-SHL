from assesswise_shl.retrieval.catalog import Catalog, CatalogRecord
from assesswise_shl.retrieval.hybrid import HybridRetriever, RetrievalQuery


def test_hybrid_retriever_scores_text_overlap() -> None:
    catalog = Catalog(
        records=[
            CatalogRecord(
                assessment_name="Software Skills Test",
                url="https://example.com/software-skills-test",
                test_type=["K"],
                description="Java programming skills",
                role_families=["software_engineering"],
                skill_domains=["programming"],
            )
        ]
    )
    retriever = HybridRetriever(catalog)

    results = retriever.search(RetrievalQuery(text="java programming", limit=10))

    assert len(results) == 1
    assert results[0].score > 0

