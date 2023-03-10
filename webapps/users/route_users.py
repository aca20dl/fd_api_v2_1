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
    return templates.TemplateResponse("users/register.html", {"request": request})


@router.post("/register")
async def register(request: Request, db: Session = Depends(get_db)):
    form = UserCreateForm(request)
    await form.load_data()
    if await form.is_valid():
        user = UserCreate(
            company_name=form.company_name, email=form.email, password=form.passowrd,
            company_category=form.company_category
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