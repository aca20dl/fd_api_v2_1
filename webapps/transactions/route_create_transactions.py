from fastapi import APIRouter
from fastapi import Request, Depends, responses, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from schemas.transactions import TransactionCreate
from db.repository.transactions import create_new_transaction
from db.repository.transactions import list_transactions
from db.session import get_db
from sqlalchemy.exc import IntegrityError
from webapps.transactions.forms import TransactionCreateForm

templates = Jinja2Templates(directory="Templates")
router = APIRouter(include_in_schema=False)

@router.get("/transaction_creation")
async def transaction_creation(request: Request):
    return templates.TemplateResponse("testing/transaction_creation.html", {"request": request})

@router.post("/transaction_creation")
async def create_transaction(request: Request, db: Session = Depends(get_db)):
    form = TransactionCreateForm(request)
    await form.load_data(request)
    transaction = TransactionCreate(
        first_name = form.first_name,
        surname = form.surname,
        gender = form.gender,
        dob = form.dob,
        merchant = form.merchant,
        merchant_category = form.merchant_category,
        cc_number = form.cc_number,
        amount = form.amount,
        state = form.state,
        street = form.street,
        city = form.city,
        zip = form.zip,
        city_population = form.city_population,
        job = form.job,
        unix_time = form.unix_time,
        date_and_time = form.date_and_time,
        transaction_number = form.transaction_number,
        latitude = form.latitude,
        longitude = form.longitude,
        merchant_latitude = form.merchant_latitude,
        merchant_longitude = form.merchant_longitude,
        is_fraud = form.is_fraud

    )
    try:
        transaction = create_new_transaction(transaction=transaction, db=db)
        return responses.RedirectResponse(
            "/?msg=Successfully-Registered", status_code=status.HTTP_302_FOUND
        )
    except IntegrityError:
        form.__dict__.get("errors").append("Something went wrong")
        return templates.TemplateResponse("testing/transaction_creation.html", form.__dict__)
    print(transaction)
    return transaction