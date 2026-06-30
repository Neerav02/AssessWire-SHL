from fastapi import FastAPI

from assesswise_shl.schemas import ChatRequest, ChatResponse, HealthResponse
from assesswise_shl.services.chat_service import ChatService

from fastapi.responses import RedirectResponse

app = FastAPI(
    title="AssessWise SHL Conversational Recommender",
    version="0.1.0",
    description="Conversational recommender for SHL Individual Test Solutions.",
)

chat_service = ChatService()


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return chat_service.respond(request)

