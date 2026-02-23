import logging
import sqlite3

from fastapi import APIRouter, Depends

from app.core.database import get_db
from app.models.schemas import ChatRequest, ChatResponse
from app.services.ai_service import generate_grounded_answer
from app.services.portfolio_service import (
    build_context_blob,
    generate_local_answer,
    get_portfolio_data,
    try_apply_mutation
)

router = APIRouter(prefix="/chat", tags=["chat"])
logger = logging.getLogger(__name__)


@router.post("", response_model=ChatResponse)
async def chat(payload: ChatRequest, db: sqlite3.Connection = Depends(get_db)):
    mutation_result = try_apply_mutation(db, payload.message)
    if mutation_result is not None:
        return ChatResponse(answer=mutation_result)

    portfolio = get_portfolio_data(db)
    context_blob = build_context_blob(portfolio)

    try:
        answer = await generate_grounded_answer(payload.message, payload.history, context_blob)
    except Exception as exc:
        logger.warning("OpenRouter chat failed. Using local fallback answer. Error: %s", exc)
        answer = generate_local_answer(payload.message, portfolio)

    return ChatResponse(answer=answer)
