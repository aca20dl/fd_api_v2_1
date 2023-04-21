from typing import List

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi import Request, Depends, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from schemas.transactions import TransactionCreate
from db.repository.transactions import retrieve_transactions_by_fraud_value
from db.session import get_db
from schemas.transactions import TransactionCreate, ShowTransaction
from webapps.fraud_detector.rule_based.form import Rule_Management_form


templates = Jinja2Templates(directory="Templates")
router = APIRouter(include_in_schema=False)

@router.get("/rb_processor")
async def home(request: Request, db: Session = Depends(get_db)):
    transactions = retrieve_transactions_by_fraud_value(2, db=db)
    return templates.TemplateResponse(
        "general_pages/rb_fraud_detector.html", {"request": request, "transactions": transactions}
    )


@router.post("/rule_form")
async def rule_form(request: Request, response: Response):
    user_is_logged_in = "access_token" in request.cookies
    form = Rule_Management_form(request)
    await form.load_data(request)

    # store all data into variables
    age1 = form.age1
    age2 = form.age2
    age3 = form.age3
    age4 = form.age4
    age5 = form.age5
    age6 = form.age6
    f_age1 = form.f_age1
    f_age2 = form.f_age2
    f_age3 = form.f_age3
    f_age4 = form.f_age4
    f_age5 = form.f_age5
    f_age6 = form.f_age6
    time_threshold_m_t = form.time_threshold_m_t
    num_multiple_transactions_threshold = form.num_multiple_transactions_threshold
    first_time_customer = form.first_time_customer
    transaction_time = form.transaction_time
    multiple_transactions = form.multiple_transactions
    larger_purchases_avg = form.larger_purchases_avg
    purchases_avg = form.purchases_avg
    purchases_avg_threshold = form.purchases_avg_threshold
    purchases_outside_customer_pattern = form.purchases_outside_customer_pattern
    purchase_pattern = form.purchase_pattern
    matches_zip_code = form.matches_zip_code
    is_merchant_category_prone_to_fraud = form.is_merchant_category_prone_to_fraud
    ip_matches_with_device_location_and_billing_adr = form.ip_matches_with_device_location_and_billing_adr
    ip_address_volume = form.ip_address_volume
    user_volume = form.user_volume
    user_volume_threshold = form.user_volume_threshold
    ip_for_multiple_users = form.ip_for_multiple_users
    ip_for_multiple_users_threshold = form.ip_for_multiple_users_threshold
    ip_for_multiple_credit_cards = form.ip_for_multiple_credit_cards
    ip_for_multiple_credit_cards_threshold = form.ip_for_multiple_credit_cards_threshold
    device_transaction_volume = form.device_transaction_volume

    content = templates.TemplateResponse("general_pages/fd_rules.html",
                                         {"request": request, "user_is_logged_in": user_is_logged_in},
                                         media_type="text/html")


    response = HTMLResponse(content=content.body, status_code=200)

    response.set_cookie(key="age1", value=age1, httponly=False)
    response.set_cookie(key="age2", value=age2, httponly=False)
    response.set_cookie(key="age3", value=age3, httponly=False)
    response.set_cookie(key="age4", value=age4, httponly=False)
    response.set_cookie(key="age5", value=age5, httponly=False)
    response.set_cookie(key="age6", value=age6, httponly=False)
    response.set_cookie(key="f_age1", value=f_age1, httponly=False)
    response.set_cookie(key="f_age2", value=f_age2, httponly=False)
    response.set_cookie(key="f_age3", value=f_age3, httponly=False)
    response.set_cookie(key="f_age4", value=f_age4, httponly=False)
    response.set_cookie(key="f_age5", value=f_age5, httponly=False)
    response.set_cookie(key="f_age6", value=f_age6, httponly=False)
    response.set_cookie(key="time_threshold_m_t", value=time_threshold_m_t, httponly=False)
    response.set_cookie(key="first_time_customer" , value=first_time_customer, httponly=False)
    response.set_cookie(key="num_multiple_transactions_threshold", value=num_multiple_transactions_threshold, httponly=False)
    response.set_cookie(key="transaction_time", value=transaction_time , httponly=False)
    response.set_cookie(key="multiple_transactions", value=multiple_transactions, httponly=False)
    response.set_cookie(key="larger_purchases_avg", value=larger_purchases_avg, httponly=False)
    response.set_cookie(key="purchases_avg", value=purchases_avg, httponly=False)
    response.set_cookie(key="purchases_avg_threshold", value=purchases_avg_threshold, httponly=False)
    response.set_cookie(key="purchases_outside_customer_pattern", value=purchases_outside_customer_pattern, httponly=False)
    response.set_cookie(key="purchase_pattern", value=purchase_pattern, httponly=False)
    response.set_cookie(key="matches_zip_code", value=matches_zip_code, httponly=False)
    response.set_cookie(key="is_merchant_category_prone_to_fraud", value=is_merchant_category_prone_to_fraud, httponly=False)
    response.set_cookie(key="ip_matches_with_device_location_and_billing_adr", value=ip_matches_with_device_location_and_billing_adr, httponly=False)
    response.set_cookie(key="ip_address_volume", value=ip_address_volume, httponly=False)
    response.set_cookie(key="user_volume", value=user_volume, httponly=False)
    response.set_cookie(key="user_volume_threshold", value=user_volume_threshold, httponly=False)
    response.set_cookie(key="ip_for_multiple_users", value=ip_for_multiple_users, httponly=False)
    response.set_cookie(key="ip_for_multiple_users_threshold", value=ip_for_multiple_users_threshold, httponly=False)
    response.set_cookie(key="ip_for_multiple_credit_cards", value=ip_for_multiple_credit_cards, httponly=False)
    response.set_cookie(key="ip_for_multiple_credit_cards_threshold", value=ip_for_multiple_credit_cards_threshold, httponly=False)
    response.set_cookie(key="device_transaction_volume", value=device_transaction_volume, httponly=False)

    # print or use the variables as needed
    print(first_time_customer, transaction_time, multiple_transactions, larger_purchases_avg, purchases_avg,
          purchases_avg_threshold, purchases_outside_customer_pattern, purchase_pattern, matches_zip_code,
          is_merchant_category_prone_to_fraud, ip_matches_with_device_location_and_billing_adr, ip_address_volume,
          user_volume, user_volume_threshold, ip_for_multiple_users, ip_for_multiple_users_threshold, device_transaction_volume)

    return response


@router.get("/rule_form")
async def rules(request: Request, db: Session = Depends(get_db)):
    user_is_logged_in = "access_token" in request.cookies
    #first_time_customer = request.cookies.get("first_time_customer")
    #transaction_time = request.cookies.get("transaction_time")
    #multiple_transactions = request.cookies.get("multiple_transactions")
    #larger_purchase_avg = request.cookies.get("larger_purchase_avg")
    #purchases_avg = request.cookies.purchases_avg
    #purchases_avg_threshold = request.cookies.purchases_avg_threshold
    #purchases_outside_customer_pattern = request.cookies.get("purchases_outside_customer_pattern")
    #purchase_pattern = request.cookies.get("purchase_pattern")
    #matches_zip_code = request.cookies.get("matches_zip_code")
    #is_merchant_category_prone_to_fraud = request.cookies.get("is_merchant_category_prone_to_fraud")
    #ip_matches_with_device_location_and_billing_adr = request.cookies.get("ip_matches_with_device_location_and_billing_adr")
    #ip_address_volume = request.cookies.get("ip_address_volume")
    #ip_address_volume_threshold = request.cookies.get("ip_address_volume_threshold")
    #user_volume = request.cookies.get("user_volume")
    #user_volume_threshold = request.cookies.get("user_volume_threshold")
    #ip_for_multiple_users = request.cookies.get("ip_for_multiple_users")
    #ip_for_multiple_users_threshold = request.cookies.get("ip_for_multiple_users_threshold")


    return templates.TemplateResponse("general_pages/fd_rules.html", {"request": request, "user_is_logged_in": user_is_logged_in})

