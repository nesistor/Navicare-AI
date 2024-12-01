from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from ai.ai_processing import MedicalDocumentProcessor
import logging

# Set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize router and medical document processor
router = APIRouter()
doc_processor = MedicalDocumentProcessor()

# Define chat message format
class ChatMessage(BaseModel):
    content: str

# Define chat request format
class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    context: Optional[str] = None

# Handle chat interaction and generate medical responses
@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        context = [{"content": msg.content} for msg in request.messages[:-1]]
        result = await doc_processor.process_chat(request.messages[-1].content, context=context)
        return result
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
