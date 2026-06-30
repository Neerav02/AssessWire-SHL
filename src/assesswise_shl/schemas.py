from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl, field_validator


class ConversationState(StrEnum):
    CLARIFYING = "CLARIFYING"
    RETRIEVING = "RETRIEVING"
    REFINING = "REFINING"
    COMPARING = "COMPARING"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"


class HealthResponse(BaseModel):
    status: Literal["ok"]


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str = Field(min_length=1)


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_length=1)

    @field_validator("messages")
    @classmethod
    def require_user_message(cls, messages: list[ChatMessage]) -> list[ChatMessage]:
        if not any(message.role == "user" for message in messages):
            raise ValueError("At least one user message is required.")
        return messages


class Recommendation(BaseModel):
    name: str = Field(min_length=1)
    url: HttpUrl
    test_type: str = Field(min_length=1)


class ChatResponse(BaseModel):
    reply: str = Field(min_length=1)
    recommendations: list[Recommendation] = Field(default_factory=list, max_length=10)
    end_of_conversation: bool = False
