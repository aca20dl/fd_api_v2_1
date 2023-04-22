from random import randint

from db.repository.users import create_new_user
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends, Request, responses, status
from fastapi.templating import Jinja2Templates
from schemas.users import UserCreate
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from webapps.users.forms import UserCreateForm

templates = Jinja2Templates(directory="Templates")
router = APIRouter(include_in_schema=False)


@router.get("/register")
def register(request: Request):
    user_is_logged_in = "access_token" in request.cookies
    if user_is_logged_in:
        return templates.TemplateResponse(
            "general_pages/homepage.html",
            {"request": request, "user_is_logged_in": user_is_logged_in}
        )
    else:
        return templates.TemplateResponse("users/register.html", {"request": request})


@router.post("/register")
async def register(request: Request, db: Session = Depends(get_db)):
    form = UserCreateForm(request)
    await form.load_data()
    if await form.is_valid():
        user = UserCreate(
            company_name=form.company_name, email=form.email, password=form.password,
            company_category=form.company_category, company_id=randint(1000, 9999),
            merch_lat=form.merch_lat, merch_long=form.merch_long
        )
        try:
            user = create_new_user(user=user, db=db)
            return responses.RedirectResponse(
                "/?msg=Successfully-Registered", status_code=status.HTTP_302_FOUND
            )
        except IntegrityError:
            form.__dict__.get("errors").append("Duplicate name or email")
            return templates.TemplateResponse("users/register.html", form.__dict__)
        return templates.TemplateResponse("users/register.html", form.__dict__)