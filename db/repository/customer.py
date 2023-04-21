import datetime
from datetime import date
from sqlalchemy import func, cast, String, Integer, update
from sqlalchemy.orm import Session
from datetime import datetime


from schemas.customer import CustomerCreate, CustomerUpdate
from db.models.customer import Customer
from core.hashing import Hasher
from db.models.transactions import Transaction
from webapps.customers.customers import average_transactions_per_week, avg_time_frame, avg_amount_per_category


def create_new_customer(customer: Customer, db: Session):
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

def update_customer(customer: Customer, merchant_category: str , date_and_time: str, amount: float, ip_address: str, cc_number, week_number , db: Session):
    # Add the new transaction date to the list
    t_dates = update(Customer).where(Customer.id == customer.id).values(
        transaction_dates=func.array_append(Customer.transaction_dates, date_and_time))

    cc_exists = db.query(Customer).filter(Customer.id == customer.id, Customer.credit_card_numbers.any(cc_number)).scalar()
    if not cc_exists:
        cc_update = update(Customer).where(Customer.id == customer.id).values(
            credit_card_numbers=func.array_append(Customer.credit_card_numbers, cc_number))
        db.execute(cc_update)

    # Execute the update statement
    db.execute(t_dates)

    # Refresh the customer object
    db.refresh(customer)

    # Increment the number of transactions
    customer.number_of_transactions += 1

    # Update transactions_per_week
    #customer.transactions_per_week = average_transactions_per_week(customer.transaction_dates)
    print(avg_time_frame(customer.transaction_dates))
    # Update transactions_time_frame
    customer.transactions_time_frame = avg_time_frame(customer.transaction_dates)

    # Update types_of_merchants
    customer.types_of_merchants = func.jsonb_set(
        Customer.types_of_merchants,
        f'{{{merchant_category}}}',
        func.to_jsonb(func.coalesce(Customer.types_of_merchants[merchant_category].astext.cast(Integer) + 1, 1)),
    )

    customer.ip_addresses = func.jsonb_set(
        Customer.ip_addresses,
        f'{{{ip_address}}}',
        func.to_jsonb(func.coalesce(Customer.ip_addresses[ip_address].astext.cast(Integer) + 1, 1)),
    )
    customer.transactions_per_week = func.jsonb_set(
        Customer.transactions_per_week,
        f'{{{week_number}}}',
        func.to_jsonb(func.coalesce(Customer.transactions_per_week[week_number].astext.cast(Integer) + 1, 1))
    )
    """
    if db.query(func.has_key(customer.avg_transaction_per_category, merchant_category)).scalar():
        num_of_transactions = customer.types_of_merchants.op('->>')(merchant_category).cast(Integer)
        num_of_transactions = db.query(num_of_transactions).scalar()
        avg_amount = customer.avg_transaction_per_category[merchant_category]
        customer.avg_transaction_per_category[merchant_category] = avg_amount_per_category(avg_amount, amount,
                                                                                           num_of_transactions)
    else:
        customer.avg_transaction_per_category[merchant_category] = amount

    if ip_address in customer.ip_addresses:
        customer.ip_addresses[ip_address] = customer.ip_addresses[ip_address] + 1
    else:
        customer.ip_addresses[ip_address] = 1
    """



    # Commit the changes to the database
    db.commit()

    # Refresh the customer object
    db.refresh(customer)

def get_all_customers(db: Session):
    customers = db.query(Customer).all()
    return customers
def get_customer_by_id(customer_id: int , db: Session):
    customer = db.query(Customer).filter(Customer.id == customer_id).one()
    return customer
def retrieve_customer_by_name(first_name: str, surname: str, dob:str, db:Session):
    customers = db.query(Customer).filter((Customer.first_name == first_name) & (Customer.surname == surname) &
                                          (Customer.dob == dob))
    return customers.all()

def get_customer_by_transaction_id(transaction_id: int, db:Session):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).one()
    customer = db.query(Customer).filter(Customer.id == transaction.customer_id).one()
    return customer

def get_customers_by_ip(ip_address: str, db:Session):
    with db:
        with db.cursor() as cur:
            query = f"SELECT * FROM customers WHERE jsonb_column ? %s;"
            cur.execute(query, (db,))
            results = cur.fetchall()

    db.close()
    return results

def get_week_number(date_str):
    format = "%Y-%m-%d %H:%M:%S.%f"
    date = (datetime.strptime(date_str, format)).date()
    day = date.day
    if 1 <= day <= 7:
        return "week1"
    elif 7 < day <= 14:
        return "week2"
    elif 14 < day <= 21:
        return "week3"
    else:
        return "week4"

def get_week_dict(date_str):
    format = "%Y-%m-%d %H:%M:%S.%f"
    date = (datetime.strptime(date_str, format)).date()
    day = date.day
    if 1 <= day <= 7:
        return {"week1": 1,
                "week2": 0,
                "week3": 0,
                "week4": 0}
    elif 7 < day <= 14:
        return {"week1": 0,
                "week2": 1,
                "week3": 0,
                "week4": 0}
    elif 14 < day <= 21:
        return {"week1": 0,
                "week2": 0,
                "week3": 1,
                "week4": 0}
    else:
        return {"week1": 0,
                "week2": 0,
                "week3": 0,
                "week4": 1}



