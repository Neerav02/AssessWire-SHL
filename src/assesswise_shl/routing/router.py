from dataclasses import dataclass, field

from assesswise_shl.schemas import ChatMessage, ConversationState


@dataclass(frozen=True)
class RoutedTurn:
    state: ConversationState
    query_text: str
    extracted_slots: dict[str, str | list[str]] = field(default_factory=dict)


class ConversationRouter:
    off_topic_terms = {"salary", "legal", "lawsuit", "weather", "recipe", "stock price", "interview question", "cfo", "joke"}
    injection_terms = {"ignore previous", "system prompt", "developer message", "jailbreak"}
    compare_terms = {"compare", "difference", "versus", " vs ", "better than"}

    def route(self, messages: list[ChatMessage]) -> RoutedTurn:
        latest_user_message = next(message for message in reversed(messages) if message.role == "user")
        text = latest_user_message.content.strip()
        lowered = text.lower()

        if self._contains_any(lowered, self.injection_terms) or self._contains_any(
            lowered, self.off_topic_terms
        ):
            return RoutedTurn(state=ConversationState.OUT_OF_SCOPE, query_text=text)

        if self._contains_any(lowered, self.compare_terms):
            return RoutedTurn(state=ConversationState.COMPARING, query_text=text)

        has_prior_recommendations = any(
            message.role == "assistant" and any(term in message.content.lower() for term in ["recommend", "shortlist", "catalog-backed"])
            for message in messages[:-1]
        )
        if has_prior_recommendations:
            return RoutedTurn(state=ConversationState.REFINING, query_text=text)

        if self._has_minimum_retrieval_signal(lowered):
            return RoutedTurn(state=ConversationState.RETRIEVING, query_text=text)

        return RoutedTurn(state=ConversationState.CLARIFYING, query_text=text)

    @staticmethod
    def _contains_any(text: str, terms: set[str]) -> bool:
        return any(term in text for term in terms)

    @staticmethod
    def _has_minimum_retrieval_signal(text: str) -> bool:
        role_terms = {
            "developer",
            "engineer",
            "sales",
            "manager",
            "graduate",
            "analyst",
            "finance",
            "java",
            "python",
        }
        test_terms = {"personality", "cognitive", "ability", "aptitude", "knowledge", "skills"}
        return any(term in text for term in role_terms.union(test_terms))

