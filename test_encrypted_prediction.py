import os
import sys
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from encryption_utils import encrypt_row, decrypt_single, public_key
from model_utils import train_model, predict_encrypted


def test_predict_encrypted_runs():
    df = pd.DataFrame({
        'a': [1, 2, 3],
        'b': [4, 5, 6],
        'target': [7, 8, 9]
    })
    model = train_model(df)
    row = df.iloc[0, :-1].values
    enc_row = encrypt_row(row)
    result = predict_encrypted(enc_row, model, public_key)
    decrypted = decrypt_single(result)
    assert isinstance(decrypted, float)