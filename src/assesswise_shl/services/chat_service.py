from assesswise_shl.config import settings
from assesswise_shl.generation.responder import ResponseBuilder
from assesswise_shl.retrieval.catalog import Catalog
from assesswise_shl.retrieval.hybrid import HybridRetriever, RetrievalQuery
from assesswise_shl.routing.router import ConversationRouter
from assesswise_shl.schemas import ChatRequest, ChatResponse, ConversationState


class ChatService:
    def __init__(self) -> None:
        catalog = Catalog.load(settings.catalog_path)
        self.router = ConversationRouter()
        self.retriever = HybridRetriever(catalog)
        self.responses = ResponseBuilder()

    def respond(self, request: ChatRequest) -> ChatResponse:
        routed = self.router.route(request.messages)

        if routed.state == ConversationState.CLARIFYING:
            return self.responses.clarify()

        if routed.state == ConversationState.OUT_OF_SCOPE:
            return self.responses.out_of_scope()

        if routed.state == ConversationState.COMPARING:
            return self.responses.comparison_placeholder()

        retrieval_query = RetrievalQuery(
            text=routed.query_text,
            limit=min(request.max_recommendations, settings.max_recommendations),
        )
        results = self.retriever.search(retrieval_query)
        return self.responses.recommendations(routed.state, results)

