import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def generate_dataset(n_samples=200):
    np.random.seed(42)

    ages = np.random.randint(18, 85, n_samples)
    severity = np.random.randint(1, 11, n_samples)

    recovery_days = (
        (ages * 0.12) +        
        (severity * 1.8) +    
        np.random.normal(0, 2, n_samples) 
    )

    recovery_days = np.maximum(1, np.round(recovery_days))

    df = pd.DataFrame({
        "Age": ages,
        "Severity": severity,
        "Recovery_Days": recovery_days
    })

    return df


def train_model():
    df = generate_dataset()

    X = df[["Age", "Severity"]]
    y = df["Recovery_Days"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    return model, X_test, y_test

def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)

    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    return {
        "MSE": round(mse, 2),
        "R2_Score": round(r2, 2)
    }

def predict_recovery(model, age, severity):
    try:
        input_df = pd.DataFrame([[age, severity]], columns=["Age", "Severity"])
        prediction = model.predict(input_df)

        return round(float(prediction[0]), 1)

    except Exception as e:
        print("Prediction Error:", e)
        return None

def initialize_model():
    model, X_test, y_test = train_model()
    metrics = evaluate_model(model, X_test, y_test)

    print("\n=== ML MODEL INITIALIZED ===")
    print("Performance:", metrics)

    return model, metrics

if __name__ == "__main__":
    model, metrics = initialize_model()

    print("\nModel Metrics:", metrics)

    test_age = 45
    test_severity = 8

    pred = predict_recovery(model, test_age, test_severity)

    print(f"\nTest Prediction → Age: {test_age}, Severity: {test_severity}")
    print(f"Estimated Recovery Days: {pred}")