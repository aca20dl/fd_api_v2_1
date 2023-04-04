from fastapi import APIRouter
from fastapi import Request, Depends
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from apis.version1.route_login import get_current_user_from_token
from db.repository.transactions import list_transactions
from db.session import get_db
from db.models.users import User

templates = Jinja2Templates(directory="Templates")
router = APIRouter(include_in_schema=False)


@router.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    user_is_logged_in = "access_token" in request.cookies
    return templates.TemplateResponse(
        "general_pages/homepage.html",
        {"request": request, "user_is_logged_in": user_is_logged_in}
    )


@router.get("/logout")
async def logout(request: Request):
    response = RedirectResponse("/")
    response.delete_cookie("access_token", httponly=True)
    return response
