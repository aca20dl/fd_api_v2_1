import math
import re
from datetime import date, datetime
from typing import List

import requests

from fastapi import Request

from db.repository.transactions import list_transactions, retrieve_transaction_by_name, retrieve_transactions_by_time
from db.repository.customer import get_customers_by_ip, get_customer_by_transaction_id, get_customer_by_id, \
    get_all_customers
from db.session import get_db
from sqlalchemy.orm import Session

from schemas.transactions import Transaction


class timeThreshold:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time


def is_first_time_customer(customer_id: int, db):
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


def age_group_pattern(request: Request, age):
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
def multiple_transactions_same_cc_short_time(request: Request, transaction, db: Session(get_db)):
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
        print("Device Transaction Volume")
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
        print("Device Transaction Volume")
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
        print("Device Transaction Volume")
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
    lat1, lon1, lat2, lon2 = map(math.radians, (float(lat1), float(lon1), float(lat2), float(lon2)))

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
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
    margin_of_error = 1.3  # 1.3 kilometer
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


def category_prone_to_fraud(request: Request):
    return True


def ip_address_used_for_multiple_cards(request: Request, transaction, db: Session(get_db)):
    threshold = request.cookies.get("ip_for_multiple_credit_cards_threshold")
    transactions = list_transactions(db=db)
    credit_cards = []
    count = 0
    for transaction_x in transactions:
        credit_card = transaction_x.cc_number
        if credit_card not in credit_cards:
            credit_cards.append(credit_card)
            if transaction.ip_address == transaction_x.ip_address:
                count = count + 1

    if count > int(threshold):
        return True
    else:
        return False


def device_location_used_for_multiple_cards(request: Request, transaction, db: Session(get_db)):
    threshold = request.cookies.get("location_for_multiple_credit_cards_threshold")
    transactions = list_transactions(db=db)
    credit_cards = []
    count = 0
    for transaction_x in transactions:
        credit_card = transaction_x.cc_number
        if credit_card not in credit_cards:
            credit_cards.append(credit_card)
            if transaction.latitude == transaction_x.latitude & transaction.longitude == transaction_x.longitude:
                count = count + 1

    if count > threshold:
        return True
    else:
        return False


def get_country_from_coordinates(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18&addressdetails=1"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "address" in data and "country" in data["address"]:
            return data["address"]["country"]

    return None


def coordinates_in_same_country(lat1, lon1, lat2, lon2):
    country1 = get_country_from_coordinates(lat1, lon1)
    country2 = get_country_from_coordinates(lat2, lon2)

    if country1 == country2:
        return True
    else:
        return False


# Customer's location is out of the usual range of Merchant's Location
def merch_loc_not_match_customer_loc(request: Request, transaction):
    # Threshold in km
    threshold = request.cookies.get("merch_location_customer_location_distance_threshold")
    fraud_score = 0
    lat = transaction.latitude
    long = transaction.longitude
    merch_lat = transaction.merchant_latitude
    merch_long = transaction.merchant_longitude
    if coordinates_in_same_country(lat, long, merch_lat, merch_long) == False:
        print("Merch Location, Customer Location Diferent Country")
        fraud_score = fraud_score + 1

    distance = haversine_distance(lat, long, merch_lat, merch_long)
    if distance > int(threshold):
        print("Merch Location, Customer Location Distance")
        fraud_score = fraud_score + 1

    return fraud_score


# -------------- Customer Pattern Functions -------------------------

def is_transaction_time_inside_pattern(time_frame: dict, transaction_datetime_str):
    time_format = "%H:%M:%S"
    start_time_str = time_frame["start_time"]
    end_time_str = time_frame["end_time"]
    start_time = datetime.strptime(start_time_str, time_format)
    end_time = datetime.strptime(end_time_str, time_format)
    transaction_time = (datetime.strptime(transaction_datetime_str, "%Y-%m-%d %H:%M:%S.%f")).time()
    transaction_time = (datetime.strptime(transaction_datetime_str, "%Y-%m-%d %H:%M:%S.%f")).time()

    start_time = start_time.time()
    end_time = end_time.time()
    if start_time <= transaction_time <= end_time:
        return True
    else:
        return False


def transaction_made_in_short_time_from_2_different_places(request: Request, db: Session(get_db), transaction):
    threshold = request.cookies.get("time_threshold")
    distance_threshold = request.cookies.get("distance_threshold")
    transactions = retrieve_transactions_by_time(transaction.unix_time, threshold, db)
    for transaction_x in transactions:
        if transaction.cc_number == transaction_x.cc_number:
            distance = haversine_distance(transaction_x.latitude, transaction_x.longitude, transaction.latitude,
                                          transaction.longitude)
            if distance >= distance_threshold:
                return True
            else:
                pass
        else:
            pass


# def transaction_per_week_outside_pattern(transaction_per_week, )


def get_fraud_score(request: Request, db: Session(get_db), transaction):
    score = 0
    rule_count = 0
    customer = get_customer_by_transaction_id(transaction.id, db)
    age = get_customer_age(customer)
    first_time_customer_cookie = request.cookies.get("first_time_customer")
    transaction_time_cookie = request.cookies.get("transaction_time")
    multiple_transaction_cookie = request.cookies.get("multiple_transactions")
    larger_purchases_avg_cookie = request.cookies.get("larger_purchases_avg")
    ip_address_matches_with_device_location_cookie = request.cookies.get(
        "ip_matches_with_device_location_and_billing_adr")
    ip_address_volume_cookie = request.cookies.get("ip_address_volume")
    device_transaction_volume_cookie = request.cookies.get("device_transaction_volume")
    merchant_category_prone_to_fraud_cookie = request.cookies.get("is_merchant_category_prone_to_fraud")
    ip_for_multiple_credit_cards_cookie = request.cookies.get("ip_for_multiple_credit_cards")
    location_for_multiple_credit_cards_cookie = request.cookies.get("ip_for_multiple_credit_cards")
    transaction_time_customer_pattern_cookie = request.cookies.get("transaction_time_customer_pattern")
    merch_location_customer_location_distance_cookie = request.cookies.get("merch_location_customer_location_distance")
    same_credit_card_different_location_short_time_cookie = request.cookies.get("same_credit_card_different_location_short_time")
    # Call the is_first_time_customer function
    first_time_customer = is_first_time_customer(customer.id, db)
    if first_time_customer_cookie == "True":
        rule_count += 1
        if first_time_customer:
            print("first time customer")
            score += 1

        else:
            pass
    if transaction_time_cookie == "True":
        rule_count += 1
        print("debug1")
        if not (check_time_in_range(request, transaction.date_and_time, age)):
            score = score + 1
            print("transaction outside normal time for age")
        else:
            pass
    else:
        pass

    if multiple_transaction_cookie == "True":
        rule_count += 3
        score = score + multiple_transactions_same_cc_short_time(request, transaction, db)
        print("multiple_transaction short time")
    else:
        pass

    if larger_purchases_avg_cookie == "True":
        score = score + purchases_outside_average(request, transaction)
        rule_count += 2
        print("larger purchases than avg")
    else:
        pass
    if ip_address_matches_with_device_location_cookie == "True":
        score = score + ip_address_matches_with_device_location(transaction)
        rule_count += 2
        print("ip matches device location")
    else:
        pass

    if ip_address_volume_cookie == "True":
        score = score + multiple_transactions_same_ip_short_time(request, transaction, db)
        rule_count += 2
        print("Ip transaction Volume")

    if device_transaction_volume_cookie == "True":
        score = score + multiple_transactions_same_location_short_time(request, transaction, db)
        rule_count += 2

    # if merchant_category_prone_to_fraud_cookie == "True":

    if ip_for_multiple_credit_cards_cookie == "True":
        if ip_address_used_for_multiple_cards(transaction=transaction, db=db, request=request):
            rule_count += 2
            score = score + 2
            print("Ip for multiple credit cards")
    if transaction_time_customer_pattern_cookie == "True":
        time_frame_dict = customer.transactions_time_frame
        datetime_str = transaction.date_and_time
        if not is_transaction_time_inside_pattern(time_frame=time_frame_dict, transaction_datetime_str=datetime_str):
            score = score + 2
            rule_count += 2
            print("Transaction Time Customer Pattern")

    if merch_location_customer_location_distance_cookie == "True":

        score = score + merch_loc_not_match_customer_loc(request, transaction)
        rule_count += 2

    if same_credit_card_different_location_short_time_cookie == "True":

        print("Credit Card in diferent Location in short period of time")


    probability = score / rule_count

    return probability
