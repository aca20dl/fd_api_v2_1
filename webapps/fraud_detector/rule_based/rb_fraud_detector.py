import datetime
import re
from datetime import date

from db.repository.transactions import list_transactions, retrieve_transaction_by_name
from db.session import get_db
from sqlalchemy.orm import Session

class timeThreshold:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time



def is_first_time_customer(db: Session(get_db), transaction):
    first_name = transaction.first_name
    surname = transaction.surname
    dob = transaction.dob
    merchant = transaction.merchant
    customer_transactions = retrieve_transaction_by_name(first_name, surname, dob, db=db)
    length = 0
    for transaction in customer_transactions:
        if transaction.merchant == merchant:
            length = length + 1
        else:
            pass
    print(length)

    if length == 1:
        return True
    else:
        return False

def get_customer_age(db: Session(get_db), transaction):
    dob_string = transaction.dob
    today = date.today()
    dob = re.split(r'\s|-', dob_string)
    year = int(dob(0))
    month = int(dob(1))
    day = int(dob(2))

    return today.year - year - ((today.month, today.day) < (month, day))

def purchases_outside_average(transaction, average, threshold):
    amount = transaction.amount
    if amount < average:
        return 0
    elif amount > average:
        if (amount - average) > threshold:
            return 1
        elif (amount - average) > 2*threshold:
            return 2
        else:
            return 0
    else:
        return 0

def age_group_pattern(age, threshold1, threshold2, threshold3, threshold4, threshold5, threshold6):
    if age > 18 & age < 25:
        return threshold1
    elif age > 25 & age < 35:
        return threshold2
    elif age > 35 & age < 45:
        return threshold3
    elif age > 45 & age < 55:
        return threshold4
    elif age > 55 & age < 65:
        return threshold5
    elif age > 65:
        return threshold6

def check_time_in_range(time_str):
    threshold = age_group_pattern()
    time = datetime.datetime.strptime(time_str, '%H:%M').time()
    start_time = datetime.datetime.strptime(threshold.start_time, '%H:%M').time()
    end_time = datetime.datetime.strptime(threshold.end_time, '%H:%M').time()

    if start_time <= end_time:
        # Time range does not span midnight
        return start_time <= time <= end_time
    else:
        # Time range spans midnight
        return start_time <= time or time <= end_time





def get_fraud_score(self, db: Session(get_db) , transaction):
    age = get_customer_age(transaction)
    form = self.request.form()
    transactions = list_transactions(db)
    score = 0
    if is_first_time_customer(transaction):
        score = score + 1
    else:
        pass
    if check_time_in_range():
        score = score + 2
    else: pass

    if purchases_outside_average(transaction, average, threshold)


    return score

