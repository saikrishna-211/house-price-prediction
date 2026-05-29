import numpy as np
import pandas as pd

def get_similar_houses(df, sqft, bhk, bath, n=5):

    # ensure numeric safety
    df = df.copy()

    features = df[['total_sqft', 'bhk', 'bath']].values

    input_vec = np.array([sqft, bhk, bath])

    # Euclidean distance
    distances = np.linalg.norm(features - input_vec, axis=1)

    df['distance'] = distances

    # sort closest
    similar = df.sort_values('distance').head(n)

    return similar[['total_sqft', 'bhk', 'bath', 'price']]