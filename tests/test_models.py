import pytest
from pydantic import ValidationError

from assesswise_shl.schemas import ChatRequest


def test_chat_request_requires_user_message() -> None:
    request = ChatRequest(messages=[{"role": "user", "content": "Need Java assessments"}])

    assert request.messages[0].content == "Need Java assessments"


def test_chat_request_rejects_empty_messages() -> None:
    with pytest.raises(ValidationError):
        ChatRequest(messages=[])

