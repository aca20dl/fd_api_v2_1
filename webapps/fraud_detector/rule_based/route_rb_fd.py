from typing import List

from fastapi import APIRouter
from fastapi import Request, Depends
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
async def rule_form(request: Request):
    user_is_logged_in = "access_token" in request.cookies
    form = Rule_Management_form(request)
    await form.load_data(request)

    # store all data into variables
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
    ip_address_volume_threshold = form.ip_address_volume_threshold
    user_volume = form.user_volume
    user_volume_threshold = form.user_volume_threshold
    ip_for_multiple_users = form.ip_for_multiple_users
    ip_for_multiple_users_threshold = form.ip_for_multiple_users_threshold

    # print or use the variables as needed
    print(first_time_customer, transaction_time, multiple_transactions, larger_purchases_avg, purchases_avg,
          purchases_avg_threshold, purchases_outside_customer_pattern, purchase_pattern, matches_zip_code,
          is_merchant_category_prone_to_fraud, ip_matches_with_device_location_and_billing_adr, ip_address_volume,
          ip_address_volume_threshold, user_volume, user_volume_threshold, ip_for_multiple_users,
          ip_for_multiple_users_threshold)

    return templates.TemplateResponse("general_pages/fd_rules.html",
                                      {"request": request, "user_is_logged_in": user_is_logged_in})


@router.get("/rule_form")
async def rules(request: Request, db: Session = Depends(get_db)):
    user_is_logged_in = "access_token" in request.cookies
    return templates.TemplateResponse("general_pages/fd_rules.html", {"request": request, "user_is_logged_in": user_is_logged_in})

