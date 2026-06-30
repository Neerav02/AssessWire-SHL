from assesswise_shl.retrieval.hybrid import RetrievalResult
from assesswise_shl.schemas import ChatResponse, ConversationState, Recommendation


class ResponseBuilder:
    def clarify(self) -> ChatResponse:
        return ChatResponse(
            state=ConversationState.CLARIFYING,
            message="What role family or skill area should the assessment shortlist focus on?",
            recommendations=[],
        )

    def out_of_scope(self) -> ChatResponse:
        return ChatResponse(
            state=ConversationState.OUT_OF_SCOPE,
            message=(
                "I can help only with SHL Individual Test Solution recommendations, refinements, "
                "and comparisons."
            ),
            recommendations=[],
        )

    def recommendations(
        self, state: ConversationState, results: list[RetrievalResult]
    ) -> ChatResponse:
        if not results:
            return ChatResponse(
                state=state,
                message=(
                    "I do not have enough catalog-backed matches yet. Please provide a role, "
                    "skill area, or assessment type."
                ),
                recommendations=[],
            )

        recommendations = [
            Recommendation(
                assessment_name=result.record.assessment_name,
                url=result.record.url,
                test_type=result.record.test_type,
                description=result.record.description or None,
                duration_minutes=result.record.duration_minutes,
                remote_testing=result.record.remote_testing,
            )
            for result in results
        ]
        return ChatResponse(
            state=state,
            message="Here is a catalog-backed shortlist based on the current constraints.",
            recommendations=recommendations,
        )

    def comparison_placeholder(self) -> ChatResponse:
        return ChatResponse(
            state=ConversationState.COMPARING,
            message=(
                "I can compare assessments once both names can be matched to catalog records. "
                "Please provide the exact SHL assessment names."
            ),
            recommendations=[],
        )

