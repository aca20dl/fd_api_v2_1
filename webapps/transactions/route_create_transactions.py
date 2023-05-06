import datetime
import socket

from fastapi import APIRouter
from fastapi import Request, Depends, responses, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from dateutil.parser import parse
from datetime import datetime
import psutil

from db.models.customer import Customer
from db.repository.users import list_users, get_user_from_id
from schemas.customer import CustomerCreate
from schemas.transactions import TransactionCreate
from db.repository.transactions import create_new_transaction
from db.repository.customer import create_new_customer, update_customer, get_week_dict, get_week_number

from db.repository.transactions import list_transactions, update_transaction_fraud_value
from db.repository.customer import retrieve_customer_by_name
from db.session import get_db
from sqlalchemy.exc import IntegrityError

from webapps.fraud_detector.rule_based.rb_fraud_detector import get_fraud_score
from webapps.transactions.forms import TransactionCreateForm
from webapps.customers.customers import average_transactions_per_week, avg_time_frame
from MLClassifier.main import preprocess_transaction, classify_transaction_xgBoost


templates = Jinja2Templates(directory="Templates")
router = APIRouter(include_in_schema=False)

@router.get("/transaction_creation")
async def transaction_creation(request: Request, db: Session = Depends(get_db)):
    users = list_users(db)


    return templates.TemplateResponse("testing/transaction_creation.html", {"request": request, "merchants": users})

@router.post("/transaction_creation")
async def create_transaction(request: Request, db: Session = Depends(get_db), train_data = Depends):
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
    ip_address = form.ip_address
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


    merchant = get_user_from_id(db=db, id=form.merchant_id)
    print(merchant)
    transaction = TransactionCreate(
        customer_id = customer.id,
        merchant = merchant.company_name,
        merchant_category = form.merchant_category,
        cc_number = form.cc_number,
        amount = form.amount,
        state = form.state,
        street = form.street,
        city = form.city,
        zip = form.zip,
        ip_address = form.ip_address,
        city_population = form.city_population,
        job = form.job,
        unix_time = form.unix_time,
        date_and_time = form.date_and_time,
        transaction_number = form.transaction_number,
        latitude = form.latitude,
        longitude = form.longitude,
        merchant_latitude = merchant.merch_lat,
        merchant_longitude = merchant.merch_long,
        device_latitude = form.device_latitude,
        device_longitude = form.device_longitude,
        is_fraud = form.is_fraud,
        ml_prob = 0.0,
        rb_prob = 0.0

    )
    try:
        transaction = create_new_transaction(transaction=transaction,customer=customer, db=db)
        rb_score = (get_fraud_score(request=request, db=db, transaction=transaction))
        ml_probability = classify_transaction_xgBoost(transaction, customer, db)
        print("ML: ", ml_probability[0])
        print("Rule Based: ",rb_score)
        fraud_probability = (rb_score + ml_probability[0]) / 2
        if fraud_probability > 0.5:
            update_transaction_fraud_value(transaction.id, float(ml_probability[0]), float(rb_score), 1, db)
        else:
            update_transaction_fraud_value(transaction.id, float(ml_probability[0]), float(rb_score), 0, db)
        print(fraud_probability)
        return responses.RedirectResponse(
            "/?msg=Successfully-Registered", status_code=status.HTTP_302_FOUND
        )
    except IntegrityError:
        form.__dict__.get("errors").append("Something went wrong")
        return templates.TemplateResponse("testing/transaction_creation.html", form.__dict__)
    print(transaction)
    print("HUEHUEHEUHEUHEUHE")
    ml_probability = classify_transaction_xgBoost(transaction, customer, db)
    print(ml_probability)


    return transaction