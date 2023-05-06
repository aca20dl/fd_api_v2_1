from sklearn.preprocessing import StandardScaler

from MLClassifier.utils import Transaction, preprocess_transactions


train_transactions = Transaction.load_data('fraudTrain.csv')
print("============================ Training Set Loaded ============================================")
x_train, y_train = preprocess_transactions(train_transactions)
print("====================== Preprocessing Finished =====================================")
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)