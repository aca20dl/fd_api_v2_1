from datetime import datetime
import datetime
import pandas as pd
import math
from imblearn.pipeline import Pipeline
from imblearn.under_sampling import RandomUnderSampler
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler

from sklearn.metrics import classification_report, accuracy_score
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import GridSearchCV
from imblearn.combine import SMOTEENN, SMOTETomek
from sklearn.metrics import confusion_matrix
import numpy as np



class Transaction:
    def __init__(self, id, date_time, cc_num, merchant, category, amt, f_name, l_name, gender, street, state, zip_code, lat,
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

        tr = pd.read_csv(f'transaction_datasets/{csv_file}', index_col=0)

        for id, row in tr.iterrows():
            transaction = cls(id, row['trans_date_trans_time'], row['cc_num'], row['merchant'], row['category'],
                              row['amt'], row['first'], row['last'], row['gender'], row['street'], row['state'],
                              row['zip'], row['lat'], row['long'], row['city_pop'], row['job'], row['dob'],
                              row['trans_num'], row['unix_time'], row['merch_lat'], row['merch_long'], row['is_fraud'])
            transactions.append(transaction)
        print(" DATASET LOADED ")
        return transactions


def extract_hour(date_time_str):
    dt = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    return dt.hour


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
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
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


def preprocess_transactions(transactions):
    print("Preprocessing Initiated ...")

    data = []
    labels = []

    # Initialize LabelEncoders for categorical features
    merchant_encoder = LabelEncoder()
    category_encoder = LabelEncoder()
    job_encoder = LabelEncoder()
    customer_avg_amounts = calculate_average_transaction_amount(transactions)
    for transaction in transactions:

        # Extract features and the target label (isFraud)
        feature_vector = [
            transaction.amt,
            transaction.lat,
            transaction.long,
            transaction.city_pop,
            transaction.unix_time,
            transaction.merch_lat,
            transaction.merch_long,
            haversine_distance(transaction.lat, transaction.long, transaction.merch_lat, transaction.merch_long),
            merchant_encoder.fit_transform([transaction.merchant])[0],
            category_encoder.fit_transform([transaction.category])[0],
            job_encoder.fit_transform([transaction.job])[0],
            extract_hour(transaction.date_time),
            calculate_age(transaction.dob),
            customer_avg_amounts[transaction.cc_num]['avg_amt']
        ]
        data.append(feature_vector)
        labels.append(transaction.isFraud)

    return data, labels


def main():
    now = datetime.datetime.now()
    start_unix_time = int(now.timestamp())
    print(start_unix_time)
    test_transactions = Transaction.load_data('fraudTest.csv')
    train_transactions = Transaction.load_data('fraudTrain.csv')


    # Preprocess Data
    X_train, y_train = preprocess_transactions(train_transactions)

    X_test, y_test = preprocess_transactions(test_transactions)
    print("X_train shape:", np.array(X_train).shape)
    print("X_test shape:", np.array(X_test).shape)
    print("PREPROCESSING FINISHED ...")

    # Normalize the data using StandardScaler
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    try:
        X_test = scaler.transform(X_test)
    except Exception as e:
        print("Error during transformation:", e)


    # Calculation for the appropriate sampling strategy
    #desired_ratio = 1 / 4  # 1 fraudulent transaction for every 4 non-fraudulent transactions
    #fraudulent_count = 2145
    #non_fraudulent_count = 553574

    #sampling_strategy = fraudulent_count / (desired_ratio * non_fraudulent_count)

    # Apply SMOTEENN to balance the classes in the training data
    smoteen = SMOTEENN(sampling_strategy='auto', random_state=42)
    X_train_resampled, y_train_resampled = smoteen.fit_resample(X_train, y_train)

    # Apply SMOTE to balance the classes in the training data
    #smote = SMOTE(sampling_strategy='auto', random_state=42)
    #X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)





    # Set up a parameter grid for GridSearchCV
    #param_grid = {
    #    'n_estimators': [50, 100, 200],
    #    'max_depth': [None, 10, 20, 30],
    #    'min_samples_split': [2, 5, 10],
    #    'min_samples_leaf': [1, 2, 4],
    #}
    #param_dist = {
    #    'n_estimators': [50, 100, 200],
    #    'max_depth': [None, 10, 20, 30],
    #    'min_samples_split': [2, 5, 10],
    #    'min_samples_leaf': [1, 2, 4],
    #}
    #random_search = RandomizedSearchCV(
    #    estimator=RandomForestClassifier(random_state=42),
    #    param_distributions=param_dist,
    #    n_iter=20,  # Number of random combinations to try
    #    cv=5,  # Number of cross-validation folds
    #    n_jobs=-1,  # Use all available CPU cores
    #    random_state=42,  # Set a random seed for reproducibility
    #)
    #random_search.fit(X_train_resampled, y_train_resampled)
    #print("Best Parameters: ", random_search.best_params_)

    # Perform Grid Search
    #grid_search = GridSearchCV(estimator=RandomForestClassifier(random_state=42),
    #                          param_grid=param_grid, cv=5, n_jobs=-1)
    #grid_search.fit(X_train_resampled, y_train_resampled)

    #print("Best Parameters: ", grid_search.best_params_)

    # Create and train a RandomForest Classifier
    print("Classifying Transaction ...")

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    #clf = RandomForestClassifier(**random_search.best_params_, random_state=42)
    clf.fit(X_train_resampled, y_train_resampled)

    # Predict probabilities for the test set
    y_pred_prob = clf.predict_proba(X_test)[:, 1]

    # Classify transactions based on a threshold (e.g., 0.5)
    y_pred = [1 if p > 0.35 else 0 for p in y_pred_prob]

    # Print clas clf = RandomForestClassifier(n_estimators=100, random_state=42)sification report
    print(classification_report(y_test, y_pred, target_names=["Not Fraudulent", "Fraudulent"]))
    print("Accuracy: ",  accuracy_score(y_test, y_pred))
    confusion = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = confusion.ravel()

    print(f"True Negatives: {tn}")
    print(f"False Positives: {fp}")
    print(f"False Negatives: {fn}")
    print(f"True Positives: {tp}")

    now2 = datetime.datetime.now()
    finish_unix_time = int(now2.timestamp())
    time_taken = finish_unix_time - start_unix_time
    print(time_taken / 60) # Time in minutes

if __name__ == "__main__":
    main()

