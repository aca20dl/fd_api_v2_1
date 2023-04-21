import datetime

from fastapi import APIRouter
from fastapi import Request, Depends, responses, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from dateutil.parser import parse
from datetime import datetime

from db.models.customer import Customer
from schemas.customer import CustomerCreate
from schemas.transactions import TransactionCreate
from db.repository.transactions import create_new_transaction
from db.repository.customer import create_new_customer, update_customer, get_week_dict, get_week_number

from db.repository.transactions import list_transactions
from db.repository.customer import retrieve_customer_by_name
from db.session import get_db
from sqlalchemy.exc import IntegrityError

from webapps.fraud_detector.rule_based.rb_fraud_detector import get_fraud_score
from webapps.transactions.forms import TransactionCreateForm
from webapps.customers.customers import average_transactions_per_week, avg_time_frame


templates = Jinja2Templates(directory="Templates")
router = APIRouter(include_in_schema=False)

@router.get("/transaction_creation")
async def transaction_creation(request: Request):
    return templates.TemplateResponse("testing/transaction_creation.html", {"request": request})

@router.post("/transaction_creation")
async def create_transaction(request: Request, db: Session = Depends(get_db)):
    form = TransactionCreateForm(request)
    await form.load_data(request)
    first_name = form.first_name
    surname = form.surname
    gender = form.gender
    dob = form.dob
    job = form.job
    merchant_category = form.merchant_category
    date_and_time= form.date_and_time
    print(type(form.amount))
    #if not isinstance(date_and_time, datetime):
    #    date_and_time = parse(date_and_time)

    #date_and_time_str = date_and_time.strftime("%Y-%m-%d %H:%M:%S.%f")
    date_and_time_str = date_and_time
    print((date_and_time_str))
    ip_address = request.client.host
    retrieved_customer = retrieve_customer_by_name(first_name, surname, dob, db=db)
    if len(retrieved_customer) == 0:
        customer = Customer(first_name=first_name,
                            surname=surname,
                            gender=gender,
                            job=job,
                            dob=dob,
                            credit_card_numbers = [form.cc_number],
                            number_of_transactions=1,
                            transaction_dates = [date_and_time_str],
                            transactions_time_frame=avg_time_frame([date_and_time_str]),
                            types_of_merchants={merchant_category: 1},
                            #avg_transaction_per_category={merchant_category: form.amount},
                            ip_addresses= {ip_address: 1},
                            transactions_per_week = get_week_dict(date_and_time_str)

        )
        create_new_customer(customer, db)
    else:
        week_number = get_week_number(date_and_time_str)
        customer = retrieved_customer[0]
        #updated_types_of_merchants = customer.types_of_merchants
        #if merchant_category in updated_types_of_merchants.keys():
        #    updated_types_of_merchants[merchant_category] += 1
        #else:
        #    updated_types_of_merchants[merchant_category] = 1

        update_customer(customer, merchant_category, date_and_time, form.amount,ip_address, form.cc_number, week_number , db)



    transaction = TransactionCreate(
        customer_id = customer.id,
        merchant = form.merchant,
        merchant_category = form.merchant_category,
        cc_number = form.cc_number,
        amount = form.amount,
        state = form.state,
        street = form.street,
        city = form.city,
        zip = form.zip,
        ip_address = ip_address,
        city_population = form.city_population,
        job = form.job,
        unix_time = form.unix_time,
        date_and_time = form.date_and_time,
        transaction_number = form.transaction_number,
        latitude = form.latitude,
        longitude = form.longitude,
        merchant_latitude = form.merchant_latitude,
        merchant_longitude = form.merchant_longitude,
        device_latitude = form.device_latitude,
        device_longitude = form.device_longitude,
        is_fraud = form.is_fraud

    )
    try:
        transaction = create_new_transaction(transaction=transaction,customer=customer, db=db)
        print(get_fraud_score(request=request, db=db, transaction=transaction))
        return responses.RedirectResponse(
            "/?msg=Successfully-Registered", status_code=status.HTTP_302_FOUND
        )
    except IntegrityError:
        form.__dict__.get("errors").append("Something went wrong")
        return templates.TemplateResponse("testing/transaction_creation.html", form.__dict__)
    print(transaction)
    return transaction