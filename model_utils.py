import pandas as pd
from sklearn.linear_model import LinearRegression
from encryption_utils import public_key

def load_data():
    url = "https://raw.githubusercontent.com/atharvjairath/Linear-Regression---Diabetes-Dataset/master/0000000000002329_training_diabetes_x_y_train.csv"
    df = pd.read_csv(url)
    return df

def train_model(df):
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    model = LinearRegression()
    model.fit(X, y)
    return model


def predict_encrypted(enc_row, model, pub_key=None):
    if pub_key is None:
        pub_key = public_key
    enc_result = pub_key.encrypt(model.intercept_)
    for i, coef in enumerate(model.coef_):
        enc_result += enc_row[i] * coef
    return enc_result
