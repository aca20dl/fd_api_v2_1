from datetime import datetime
import pandas as pd
from imblearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE
from sklearn.metrics import confusion_matrix
from imblearn.under_sampling import RandomUnderSampler
from sklearn.preprocessing import StandardScaler


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
    dt = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    return dt.hour


def calculate_age(dob_str):
    dob = datetime.strptime(dob_str, '%Y-%m-%d')
    current_year = datetime.now().year
    return current_year - dob.year


def preprocess_transactions(transactions):
    print("Preprocessing Initiated ...")

    f_name_encoder = LabelEncoder()
    l_name_encoder = LabelEncoder()
    gender_encoder = LabelEncoder()
    street_encoder = LabelEncoder()

    data = []
    labels = []

    # Initialize LabelEncoders for categorical features
    merchant_encoder = LabelEncoder()
    category_encoder = LabelEncoder()
    state_encoder = LabelEncoder()
    job_encoder = LabelEncoder()

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
            #merchant_encoder.fit_transform([transaction.merchant])[0],
            category_encoder.fit_transform([transaction.category])[0],
            state_encoder.fit_transform([transaction.state])[0],
            job_encoder.fit_transform([transaction.job])[0],
            extract_hour(transaction.date_time),
            #transaction.cc_num,
            f_name_encoder.fit_transform([transaction.f_name])[0],
            l_name_encoder.fit_transform([transaction.l_name])[0],
            gender_encoder.fit_transform([transaction.gender])[0],
            # street_encoder.fit_transform([transaction.street])[0],
            # transaction.zip,
            calculate_age(transaction.dob)
        ]
        data.append(feature_vector)
        labels.append(transaction.isFraud)
    scaler = StandardScaler()
    data = scaler.fit_transform(data)
    return data, labels




def main():
    transactions_test_small = Transaction.load_data('smallerTrain.csv')
    test_transactions = Transaction.load_data('fraudTest.csv')
    train_transactions = Transaction.load_data('fraudTrain.csv')

    for transaction in transactions_test_small:
        print(transaction.id)

    # Preprocess Data
    X_train, y_train = preprocess_transactions(train_transactions)
    X_test, y_test = preprocess_transactions(test_transactions)
    print("PREPROCESSING FINISHED ...")

    # Apply SMOTE to balance the classes in the training data and RandomUnderSampler to reduce the majority class
    over = SMOTE(sampling_strategy=0.1, random_state=42)
    under = RandomUnderSampler(sampling_strategy=0.5, random_state=42)
    steps = [('over', over), ('under', under)]
    pipeline = Pipeline(steps=steps)

    X_train_resampled, y_train_resampled = pipeline.fit_resample(X_train, y_train)

    # Create and train a Gaussian Naive Bayes Classifier
    print("Classifying Transaction ...")

    # Adjust the var_smoothing parameter to improve the model
    clf = GaussianNB(var_smoothing=1e-2)
    clf.fit(X_train_resampled, y_train_resampled)
    # Predict probabilities for the test set
    y_pred_prob = clf.predict_proba(X_test)[:, 1]

    # Classify transactions based on a threshold (e.g., 0.5)
    y_pred = [1 if p > 0.35 else 0 for p in y_pred_prob]

    # Print classification report
    print(classification_report(y_test, y_pred, target_names=["Not Fraudulent", "Fraudulent"]))

    confusion = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = confusion.ravel()

    print(f"True Negatives: {tn}")
    print(f"False Positives: {fp}")
    print(f"False Negatives: {fn}")
    print(f"True Positives: {tp}")


if __name__ == "__main__":
    main()
