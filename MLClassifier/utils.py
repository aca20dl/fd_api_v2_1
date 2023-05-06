
from datetime import datetime
import datetime
import pandas as pd
import math
from sklearn.preprocessing import LabelEncoder, StandardScaler

class Transaction:
    def __init__(self, id, date_time, cc_num, merchant, category, amt, f_name, l_name, gender, street, state, zip_code,
                 lat,
                 long, city_pop, job, dob, trans_num, unix_time, merch_lat, merch_long, is_fraud):
        self.id = id
        self.date_time = date_time
        self.cc_num = cc_num
        self.merchant = merchant
        self.category = category
        self.amt = amt
        self.f_name = f_name
        self.l_name = l_name
        self.gender = gender
        self.street = street
        self.state = state
        self.zip = zip_code
        self.lat = lat
        self.long = long
        self.city_pop = city_pop
        self.job = job
        self.dob = dob
        self.trans_num = trans_num
        self.unix_time = unix_time
        self.merch_lat = merch_lat
        self.merch_long = merch_long
        self.isFraud = is_fraud

    @classmethod
    def load_data(cls, csv_file):
        transactions = []

        tr = pd.read_csv(f'MLClassifier/transaction_datasets/{csv_file}', index_col=0)

        return tr


def extract_hour(date_time_str):
    dt = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    return dt.hour


def extract_dayofweek(date_time_str):
    dt = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    return dt.weekday()


def extract_month(date_time_str):
    dt = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    return dt.month


def calculate_age(dob_str):
    dob = datetime.datetime.strptime(dob_str, '%Y-%m-%d')
    current_year = datetime.datetime.now().year
    return current_year - dob.year


def haversine_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    # Radius of the Earth in kilometers
    earth_radius = 6371

    # Calculate the distance
    distance = earth_radius * c
    return distance


def calculate_average_transaction_amount(transactions):
    # Create a dictionary to store the total transaction amount and count for each customer
    customer_data = {}

    for transaction in transactions:
        if transaction.cc_num not in customer_data:
            customer_data[transaction.cc_num] = {'total_amt': 0, 'count': 0}

        customer_data[transaction.cc_num]['total_amt'] += transaction.amt
        customer_data[transaction.cc_num]['count'] += 1

    # Calculate the average transaction amount for each customer
    for cc_num, data in customer_data.items():
        avg_amt = data['total_amt'] / data['count']
        customer_data[cc_num]['avg_amt'] = avg_amt

    return customer_data
def preprocess_transactions(transactions_df):
    print("Preprocessing Initiated ...")

    # Calculate customer average transaction amounts
    customer_avg_amounts = transactions_df.groupby('cc_num')['amt'].agg(['sum', 'count'])
    customer_avg_amounts['avg_amt'] = customer_avg_amounts['sum'] / customer_avg_amounts['count']
    transactions_df = transactions_df.merge(customer_avg_amounts['avg_amt'], on='cc_num')

    # Encode categorical features
    category_encoder = LabelEncoder()
    transactions_df['category_encoded'] = category_encoder.fit_transform(transactions_df['category'])

    # Extract date-time features
    transactions_df['trans_date_trans_time'] = pd.to_datetime(transactions_df['trans_date_trans_time'])
    transactions_df['hour'] = transactions_df['trans_date_trans_time'].dt.hour
    transactions_df['month'] = transactions_df['trans_date_trans_time'].dt.month
    transactions_df['dayofweek'] = transactions_df['trans_date_trans_time'].dt.weekday

    # Calculate age
    transactions_df['dob'] = pd.to_datetime(transactions_df['dob'])
    transactions_df['age'] = (pd.Timestamp.now().normalize() - transactions_df['dob']).dt.total_seconds() / (60 * 60 * 24 * 365.25)

    # Calculate haversine distance
    transactions_df['distance'] = transactions_df.apply(
        lambda row: haversine_distance(row['lat'], row['long'], row['merch_lat'], row['merch_long']),
        axis=1
    )

    # Select columns for the feature matrix
    feature_columns = [
        'amt', 'lat', 'long', 'city_pop', 'merch_lat', 'merch_long', 'distance', 'category_encoded',
        'hour', 'month', 'dayofweek', 'age', 'avg_amt'
    ]
    X = transactions_df[feature_columns].values
    y = transactions_df['is_fraud'].values

    return X, y

