import pandas as pd
import numpy as np


# ------------------------------------------------
# CONVERT SQFT
# ------------------------------------------------
def convert_sqft(x):

    try:
        x = str(x)

        if '-' in x:
            a, b = x.split('-')
            return (float(a) + float(b)) / 2

        return float(x)

    except:
        return np.nan


# ------------------------------------------------
# CLEAN DATASET
# ------------------------------------------------
def clean_data(df):

    df = df.dropna()

    drop_cols = [
        'area_type',
        'availability',
        'society',
        'balcony'
    ]

    for col in drop_cols:
        if col in df.columns:
            df = df.drop(col, axis=1)

    # convert sqft
    df['total_sqft'] = df['total_sqft'].apply(convert_sqft)

    # remove invalid rows
    df = df.dropna(subset=['total_sqft'])

    # create bhk
    df['bhk'] = df['size'].apply(
        lambda x: int(str(x).split(' ')[0])
    )

    return df