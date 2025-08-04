import os
import pandas as pd
import json
from dotenv import load_dotenv
import requests
from deepdiff import DeepDiff, DeepSearch


load_dotenv()


def within_percentage_threshold(actual, expected, threshold=5):
    # Calcular la diferencia porcentual entre el valor actual y esperado
    percentage_diff = abs((actual - expected) / expected * 100)
    return percentage_diff <= threshold


def test_print_env_vars():
    print("BENTOML_ENDPOINT_URL:", os.getenv("BENTOML_ENDPOINT_URL"))
    print("MODEL_NAME:", os.getenv("MODEL_NAME"))
    assert os.getenv("BENTOML_ENDPOINT_URL") is not None


def test_bentoml():

    assert os.getenv("TEST_DATA_DIR") is not None, "Data dir is None"
    assert os.getenv("BENTOML_ENDPOINT_URL") is not None, "Endpoint is None"
    bentoml_endpoint_url = os.getenv("BENTOML_ENDPOINT_URL")

    test_dir = os.getenv("TEST_DATA_DIR")
    citibike_test_file = "test-modeling.parquet"
    citibike_test_path = os.path.join(test_dir, citibike_test_file)
    assert os.path.exists(
        citibike_test_path
    ), f"Don't found trips data {citibike_test_path}"

    model_data = pd.read_parquet(citibike_test_path)

    model_data_sampple = model_data[
        "2025-01-01 00:00:00":"2025-01-01 03:00:01"
    ]

    X = model_data_sampple.drop(columns=["trips", "SNOW", "day_sin"])
    y = model_data_sampple["trips"].astype("float")

    instances = X.to_dict(orient="records")
    data = {"input_data": instances}

    actual_response = requests.post(bentoml_endpoint_url, json=data).json()
    print("actual response:")

    print(json.dumps(actual_response, indent=2))

    expected_response = {
        "predictions": [
            {
                "model": "ride_duration_prediction_model",
                "version": "Test123",
                "prediction": {
                    "ride_duration": 21.3,
                    "ride_id": 256,
                },
            }
        ]
    }
    expected_response = {"predictions": y.values.tolist()}

    print("expected response:")

    print(json.dumps(expected_response, indent=2))

    # Umbral de tolerancia en porcentaje
    threshold = 15

    # Comparar cada valor de predicción con el umbral
    for i, (actual, expected) in enumerate(
        zip(actual_response["predictions"], expected_response["predictions"])
    ):
        assert within_percentage_threshold(actual, expected, threshold), (
            f"Prediction {i} outside the threshold: "
            f"present value {actual} and expected {expected}. "
            f"Percentage difference:{abs((actual - expected) / expected * 100):.2f}%"
        )

    print(f"All predictions are within the threshold {threshold}.")
