from fastapi import APIRouter
from fastapi import Request, Depends
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from apis.version1.route_login import get_current_user_from_token, oauth2_scheme
from schemas.transactions import TransactionCreate
from db.repository.transactions import retrieve_transactions_by_merchant
from db.session import get_db
from db.models.users import User
from webapps.transactions.forms import TransactionCreateForm

templates = Jinja2Templates(directory="Templates")
router = APIRouter(include_in_schema=False)


@router.get("/transaction_history")
async def history(request: Request, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_is_logged_in = "access_token" in request.cookies
    if user_is_logged_in:
        user = get_current_user_from_token(token, db=db)
        company_name = user.company_name
        transactions = retrieve_transactions_by_merchant(company_name, db=db)
        return templates.TemplateResponse("general_pages/transactionHistory.html", {"request": request,
                                                                                    "transactions": transactions,
                                                                                    "user_is_logged_in":
                                                                                        user_is_logged_in})
    else:
        response = RedirectResponse("/login")
        return response


