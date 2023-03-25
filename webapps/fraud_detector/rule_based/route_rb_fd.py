from fastapi import APIRouter
from fastapi import Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from schemas.transactions import TransactionCreate
from db.repository.transactions import retrieve_transactions_by_fraud_value
from db.session import get_db

templates = Jinja2Templates(directory="Templates")
router = APIRouter(include_in_schema=False)

@router.get("/rb_processor")
async def home(request: Request, db: Session = Depends(get_db)):
    transactions = retrieve_transactions_by_fraud_value(2, db=db)
    return templates.TemplateResponse(
        "general_pages/rb_fraud_detector.html", {"request": request, "transactions": transactions}
    )

