import sqlite3

from fastapi import APIRouter, Depends, HTTPException

from app.core.database import get_db
from app.models.schemas import PortfolioOut
from app.services.portfolio_service import get_portfolio_data

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("", response_model=PortfolioOut)
def fetch_portfolio(db: sqlite3.Connection = Depends(get_db)):
    try:
        return get_portfolio_data(db)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
