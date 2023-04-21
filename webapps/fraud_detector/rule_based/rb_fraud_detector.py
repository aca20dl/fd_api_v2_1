import math
import re
from datetime import date, datetime
from typing import List

import requests

from fastapi import Request


from db.repository.transactions import list_transactions, retrieve_transaction_by_name, retrieve_transactions_by_time
from db.repository.customer import get_customers_by_ip, get_customer_by_transaction_id, get_customer_by_id, get_all_customers
from db.session import get_db
from sqlalchemy.orm import Session

from schemas.transactions import Transaction


class timeThreshold:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time


def is_first_time_customer(customer_id:int, db):
    customer = get_customer_by_id(customer_id, db)
    if customer.number_of_transactions == 1:
        return True
    else:
        return False

def address_matches_zip_code(transaction):
    street = transaction.street
    zip = transaction.zip
    state = transaction.state
    city = transaction.city




def get_customer_age(customer):
    dob_string = customer.dob
    today = date.today()
    dob = re.split(r'\s|-', dob_string)
    year = int(dob[0])
    month = int(dob[1])
    day = int(dob[2])

    return today.year - year - ((today.month, today.day) < (month, day))


def purchases_outside_average(request: Request, transaction):
    average = int(request.cookies.get("purchases_avg"))
    threshold = int(request.cookies.get("purchases_avg_threshold"))
    print(type(average))
    print(type(threshold))
    amount = transaction.amount
    if amount < average:
        return 0
    elif amount > average:
        if ((amount - average) > threshold) & ((amount - average) < 2 * threshold):
            return 1
        elif (amount - average) >= 2 * threshold:
            return 2
        else:
            return 0
    else:
        return 0


def age_group_pattern(request:Request, age):
    threshold1 = (request.cookies.get("age1"), request.cookies.get("f_age1"))
    threshold2 = (request.cookies.get("age2"), request.cookies.get("f_age2"))
    threshold3 = (request.cookies.get("age3"), request.cookies.get("f_age3"))
    threshold4 = (request.cookies.get("age4"), request.cookies.get("f_age4"))
    threshold5 = (request.cookies.get("age5"), request.cookies.get("f_age5"))
    threshold6 = (request.cookies.get("age6"), request.cookies.get("f_age6"))
    if age >= 18 & age <= 25:
        return threshold1
    elif age > 25 & age <= 35:
        return threshold2
    elif age > 35 & age <= 45:
        return threshold3
    elif age > 45 & age <= 55:
        return threshold4
    elif age > 55 & age <= 65:
        return threshold5
    elif age > 65:
        return threshold6


def check_time_in_range(request: Request, datetime_str, age):
    threshold = age_group_pattern(request, age)
    time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f').time()
    start_time_str = threshold[0]
    end_time_str = threshold[1]
    start_time = datetime.strptime(start_time_str, '%H:%M').time()
    end_time = datetime.strptime(end_time_str, '%H:%M').time()
    print(type(start_time))
    print(type(end_time))
    print(type(time))

    if start_time <= end_time:
        # Time range does not span midnight
        return start_time <= time <= end_time
    else:
        # Time range spans midnight
        return start_time <= time or time <= end_time

# Detects all the transactions done in a certain period of time, that were made by the same credit card
def multiple_transactions_same_cc_short_time(request: Request,transaction, db: Session(get_db)):
    credit_card = transaction.cc_number
    seconds = transaction.unix_time
    time_threshold = request.cookies.get("time_threshold_m_t")
    transactions = retrieve_transactions_by_time(seconds, time_threshold, db=db)
    threshold = int(request.cookies.get("num_multiple_transactions_threshold"))
    # Change fraud score to the weight of this rule
    fraud_score = 0
    count = 0
    for transaction in transactions:
        if credit_card == transaction.cc_number:
            count = count + 1

        else:
            pass
    if count > threshold:
        fraud_score = 3

    return fraud_score

def multiple_transactions_same_ip_short_time(request: Request, transaction, db: Session(get_db)):
    ip_address = transaction.ip_address
    seconds = transaction.unix_time
    time_threshold = request.cookies.get("time_threshold_m_t")
    transactions = retrieve_transactions_by_time(seconds, time_threshold, db=db)
    threshold = int(request.cookies.get("num_multiple_transactions_threshold"))
    # Change fraud score to the weight of this rule
    fraud_score = 0
    count = 0
    for transaction in transactions:
        if ip_address == transaction.ip_address:
            count = count + 1

        else:
            pass
    if count > threshold:
        fraud_score = 3

    return fraud_score

def multiple_transactions_same_location_short_time(request: Request, transaction, db: Session(get_db)):
    seconds = transaction.unix_time
    latitude = transaction.device_latitude
    longitude = transaction.device_longitude
    time_threshold = request.cookies.get("time_threshold_m_t")
    transactions = retrieve_transactions_by_time(seconds, time_threshold, db=db)
    threshold = int(request.cookies.get("num_multiple_transactions_threshold"))
    fraud_score = 0
    count = 0
    for transaction in transactions:
        if transaction.latitude == latitude & transaction.longitude == longitude:
            count = count + 1
        else:
            pass
    if count > threshold:
        fraud_score = 3

    return fraud_score



def check_zip_code(country, city, street, zip_code):
    api_key = "fe422b29ee22eb2bb9fb6ff426236d42b922323"
    # Construct the URL for the Geocodio API
    url = f"https://api.geocod.io/v1.6/geocode?q={street}+{city}+{country}&api_key={api_key}"

    # Send a GET request to the API
    response = requests.get(url)

    # Parse the JSON response
    data = response.json()

    # Check if the response contains the given zip code
    if "results" in data and len(data["results"]) > 0:
        result = data["results"][0]
        if "address_components" in result:
            for component in result["address_components"]:
                if "postal_code" in component and component["postal_code"] == zip_code:
                    return True

    # If the zip code was not found, return False
    return False

def is_category_prone_to_fraud(merchant_category):

    return True


def haversine_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, (lat1, lon1, lat2, lon2))

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    # Earth radius in kilometers (approximately)
    earth_radius = 6371

    # Calculate the distance in kilometers
    distance = earth_radius * c

    return distance


def ip_address_matches_with_device_location(transaction: Transaction):
    device_lat = float(transaction.device_latitude)
    device_long = float(transaction.device_longitude)
    ip_lat = float(transaction.latitude)
    ip_long = float(transaction.longitude)
    score = 0
    margin_of_error =1.3  # 1.3 kilometer
    threshold_distance = 600  # 600 Kilometers

    distance = haversine_distance(device_lat, device_long, ip_lat, ip_long)
    print(distance)

    if distance <= margin_of_error:
        return score
    elif distance >= threshold_distance:
        score = 7
        return score
    else:
        score = 2
        return score

# If an ip address is used  multiple times
'''
def ip_address_matches_multiple_users(transaction: Transaction, db: Session(get_db)):
    public_network_threshold = 20
    seconds = transaction.unix_time
    time_threshold = 3600  # 1 hour
    all_customers = get_all_customers(db=db)
    transactions = retrieve_transactions_by_time(seconds, time_threshold, db)
    transaction_ip_list = List
    for transaction in transactions:
        transaction_ip_list.append(transaction.ip_address)
    ip1 = transaction.ip_address
    count = 0
    for customer in all_customers:
        ip_dict = customer.ip_addresses
        if ip1 in ip_dict & ip1 in transaction_ip_list:
            count = count + 1

    return count
    
'''




# -------------- Customer Pattern Functions -------------------------

def is_transaction_time_inside_pattern(time_frame: dict, transaction_datetime_str):
    time_format = "%H:%M:%S"
    start_time_str = time_frame["start_time"]
    end_time_str = time_frame["end_time"]
    start_time = datetime.strptime(start_time_str, time_format)
    end_time = datetime.strptime(end_time_str, time_format)
    transaction_time = (datetime.strptime(transaction_datetime_str, "%Y-%m-%d %H:%M:%S")).time()
    if start_time <= transaction_time <= end_time:
        return True
    else:
        return False

# If a customer has a total of transactions greater than a threshold and
def is_category_outside_pattern():


    return False


#def transaction_per_week_outside_pattern(transaction_per_week, )




def get_fraud_score(request: Request, db: Session(get_db), transaction):
    score = 0
    customer = get_customer_by_transaction_id(transaction.id, db)
    age = get_customer_age(customer)
    first_time_customer_cookie = request.cookies.get("first_time_customer")
    transaction_time_cookie = request.cookies.get("transaction_time")
    multiple_transaction_cookie = request.cookies.get("multiple_transactions")
    larger_purchases_avg_cookie = request.cookies.get("larger_purchases_avg")
    ip_address_matches_with_device_location_cookie = request.cookies.get("ip_matches_with_device_location_and_billing_adr")
    ip_address_volume_cookie = request.cookies.get("ip_address_volume")
    device_transaction_volume_cookie = request.cookies.get("device_transaction_volume")

    # Call the is_first_time_customer function
    first_time_customer = is_first_time_customer(customer.id, db)
    if first_time_customer_cookie == "True":
        if first_time_customer:
            score = score + 1
        else:
            pass
    if transaction_time_cookie == "True":
        print("debug1")
        if not (check_time_in_range(request, transaction.date_and_time, age)):
            score = score + 2
        else:
            pass
    else:
        pass

    if multiple_transaction_cookie == "True":
        score = score + multiple_transactions_same_cc_short_time(request, transaction, db)
    else:
        pass

    if larger_purchases_avg_cookie == "True":
        score = score + purchases_outside_average(request, transaction)
    else:
        pass
    if ip_address_matches_with_device_location_cookie == "True":
       score = score + ip_address_matches_with_device_location(transaction)
    else:
        pass

    if ip_address_volume_cookie == "True":
        score = score + multiple_transactions_same_ip_short_time(request, transaction, db)

    if device_transaction_volume_cookie == "True":
        score = score + multiple_transactions_same_location_short_time(request, transaction, db)


    return score



