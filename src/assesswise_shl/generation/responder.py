from assesswise_shl.retrieval.hybrid import RetrievalResult
from assesswise_shl.schemas import ChatResponse, ConversationState, Recommendation


class ResponseBuilder:
    def clarify(self) -> ChatResponse:
        return ChatResponse(
            reply="What role family or skill area should the assessment shortlist focus on?",
            recommendations=[],
            end_of_conversation=False,
        )

    def out_of_scope(self) -> ChatResponse:
        return ChatResponse(
            reply=(
                "I can help only with SHL Individual Test Solution recommendations, refinements, "
                "and comparisons."
            ),
            recommendations=[],
            end_of_conversation=True,
        )

    def recommendations(
        self, state: ConversationState, results: list[RetrievalResult]
    ) -> ChatResponse:
        if not results:
            return ChatResponse(
                reply=(
                    "I do not have enough catalog-backed matches yet. Please provide a role, "
                    "skill area, or assessment type."
                ),
                recommendations=[],
                end_of_conversation=False,
            )

        recommendations = [
            Recommendation(
                name=result.record.assessment_name,
                url=result.record.url,
                test_type=", ".join(result.record.test_type),
            )
            for result in results
        ]
        return ChatResponse(
            reply="Here is a catalog-backed shortlist based on the current constraints.",
            recommendations=recommendations,
            end_of_conversation=False,
        )

    def comparison_placeholder(self) -> ChatResponse:
        return ChatResponse(
            reply=(
                "I can compare assessments once both names can be matched to catalog records. "
                "Please provide the exact SHL assessment names."
            ),
            recommendations=[],
            end_of_conversation=False,
        )
