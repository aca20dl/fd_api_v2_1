from fastapi import APIRouter
from fastapi import Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from db.repository.transactions import list_transactions
from db.session import get_db

templates = Jinja2Templates(directory="Templates")
router = APIRouter(include_in_schema=False)


@router.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    transactions = list_transactions(db=db)
    return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request, "transactions": transactions}
    )
