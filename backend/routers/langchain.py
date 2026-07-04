from fastapi import APIRouter, status

from schemas.chat import ChatRequest, ChatResponse
from service.langchain_service import service

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):

    response = service.chat_with_memory(
        payload.message,
        payload.session_id,
    )

    return ChatResponse(
        response=response,
    )


@router.delete(
    "/chat/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_chat(session_id: str):
    service.clear_history(session_id)