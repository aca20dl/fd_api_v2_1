from datetime import datetime
import datetime
import pandas as pd
import math

from fastapi import Depends
from imblearn.pipeline import Pipeline
from imblearn.under_sampling import RandomUnderSampler
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from xgboost import XGBClassifier

from sklearn.metrics import classification_report, accuracy_score
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import GridSearchCV
from imblearn.combine import SMOTEENN, SMOTETomek
from sklearn.metrics import confusion_matrix
import numpy as np
from sqlalchemy.orm import Session

from MLClassifier.data_loader import x_train, y_train
from schemas.transactions import Transaction

from db.repository.transactions import list_transactions, retrieve_transactions_by_cc_number
from db.session import get_db
from webapps.fraud_detector.rule_based.rb_fraud_detector import get_customer_age
from MLClassifier.utils import Transaction, preprocess_transactions, haversine_distance


def preprocess_transaction(transaction, customer, db: Session = Depends(get_db)):
    transactions = list_transactions(db)
    customer_avg_amounts = get_avg_transaction_amount_per_card(db, transaction.cc_number)
    category_encoded = LabelEncoder()
    category = category_encoded.fit_transform([transaction.merchant_category])
    date_time = pd.to_datetime(transaction.date_and_time)
    hour = date_time.hour
    month = date_time.month
    dayofweek = date_time.dayofweek
    dob = pd.to_datetime(customer.dob)
    age = get_customer_age(customer)
    distance = haversine_distance(float(transaction.latitude), float(transaction.longitude),
                                  float(transaction.merchant_latitude),
                                  float(transaction.merchant_longitude))
    amt = transaction.amount
    lat = transaction.latitude
    long = transaction.longitude
    city_pop = transaction.city_population
    merch_lat = transaction.merchant_latitude
    merch_long = transaction.merchant_longitude

    x = [amt, lat, long, city_pop, merch_lat, merch_long, distance, category, hour, month
         , dayofweek, age, customer_avg_amounts]
    return x

def classify_transaction_xgBoost(transaction, customer, db: Session = Depends(get_db)):
    x_test = preprocess_transaction(transaction, customer, db)
    clf = XGBClassifier(n_estimators=100, random_state=42, use_label_encoder=False, eval_metrics="logloss")
    clf.fit(x_train, y_train)
    x_test = [float(item) if not isinstance(item, np.ndarray) else float(item[0]) for item in x_test]
    print("x_test:", x_test)
    x_test_array = np.array(x_test)
    x_test_2d = x_test_array.reshape(1, -1)
    fraud_probability = clf.predict_proba(x_test_2d)[:, 1]
    return fraud_probability



def get_avg_transaction_amount_per_card(db: Session, credit_card_number):

    # Fetch all transactions using the provided function
    transactions = retrieve_transactions_by_cc_number(credit_card_number, db)

    total_amount = 0
    number_of_transactions = 0
    for transaction in transactions:
        total_amount = total_amount + transaction.amount
        number_of_transactions += 1
    if number_of_transactions> 0:
        avg_amount = total_amount / number_of_transactions
    else:
        avg_amount = 0

    return avg_amount
def is_fraud(x_train, y_train, transaction):
    preprocess_transactions(transaction)


