import numpy as np

def calculate_luxury(sqft, bhk, bath):

    # better logic (more realistic)
    if sqft > 2500 or bhk >= 4 or bath >= 3:
        return 1
    return 0


def validate_inputs(sqft, bhk, bath):

    if sqft <= 0 or bhk <= 0 or bath <= 0:
        raise ValueError("Invalid input values")

    if bhk > 10 or bath > 10:
        raise ValueError("Unrealistic house configuration")

    return True


def predict_price(model, sqft, bhk, bath):

    validate_inputs(sqft, bhk, bath)

    luxury = calculate_luxury(sqft, bhk, bath)

    input_data = np.array([[sqft, bhk, bath, luxury]])

    prediction = model.predict(input_data)[0]

    return prediction, luxury