import pytest
from pydantic import ValidationError

from assesswise_shl.schemas import ChatRequest, ChatResponse, Recommendation


def test_chat_request_requires_user_message() -> None:
    request = ChatRequest(messages=[{"role": "user", "content": "Need Java assessments"}])

    assert request.messages[0].content == "Need Java assessments"


def test_chat_request_rejects_empty_messages() -> None:
    with pytest.raises(ValidationError):
        ChatRequest(messages=[])


def test_chat_response_matches_assignment_schema() -> None:
    response = ChatResponse(
        reply="Here are matching assessments.",
        recommendations=[
            Recommendation(
                name="Java 8 (New)",
                url="https://www.shl.com/solutions/products/product-catalog/view/java-8-new/",
                test_type="K",
            )
        ],
        end_of_conversation=False,
    )

    assert set(response.model_dump()) == {"reply", "recommendations", "end_of_conversation"}
