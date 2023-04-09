from sqlalchemy.orm import Session

from schemas.customer import CustomerCreate, CustomerUpdate
from db.models.customer import Customer
from core.hashing import Hasher
from webapps.customers.customers import average_transactions_per_week, avg_time_frame


def create_new_customer(customer: CustomerCreate, db: Session):
    customer = CustomerCreate(
        first_name = customer.first_name,
        surname = customer.surname,
        gender = customer.gender,
        dob = customer.dob,
        job = customer.job,
        numberOfTransactions = customer.numberOfTransactions,
        transactions_per_week = customer.transactions_per_week,
        transactions_time_frame = customer.transactions_time_frame,
        types_of_merchants = customer.types_of_merchants
        )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

def update_customer(customer: Customer, merchant_category: str , date_and_time: str , db: Session):
    # Increment the number of transactions
    customer.numberOfTransactions += 1

    # Update transactions_per_week
    customer.transactions_per_week = average_transactions_per_week(customer.transactions_time_frame + [date_and_time])

    # Update transactions_time_frame
    customer.transactions_time_frame = avg_time_frame(customer.transactions_time_frame + [date_and_time])

    # Update types_of_merchants
    if merchant_category in customer.types_of_merchants:
        customer.types_of_merchants[merchant_category] += 1
    else:
        customer.types_of_merchants[merchant_category] = 1

    # Commit the changes to the database
    db.commit()

    # Refresh the customer object
    db.refresh(customer)

def retrieve_customer_by_name(first_name: str, surname: str, dob:str, db:Session):
    customers = db.query(Customer).filter(Customer.first_name == first_name & Customer.surname == surname &
                                          Customer.dob == dob)
    return customers

