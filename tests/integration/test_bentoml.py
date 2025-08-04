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


def test_endpoints():
    print(
        "BENTOML_PREDICT_ENDPOINT_URL:",
        os.getenv("BENTOML_PREDICT_ENDPOINT_URL"),
    )
    assert os.getenv("BENTOML_PREDICT_ENDPOINT_URL") is not None
    print(
        "BENTOML_PREDICT_TRIP_ENDPOINT_URL:",
        os.getenv("BENTOML_PREDICT_TRIP_ENDPOINT_URL"),
    )
    assert os.getenv("BENTOML_PREDICT_TRIP_ENDPOINT_URL") is not None


def test_predict():

    assert os.getenv("TEST_DATA_DIR") is not None, "Data dir is None"
    assert (
        os.getenv("BENTOML_PREDICT_ENDPOINT_URL") is not None
    ), "Endpoint is None"
    bentoml_endpoint_url = os.getenv("BENTOML_PREDICT_ENDPOINT_URL")

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

    X = model_data_sampple.drop(columns=["trips", "day_sin"])
    y = model_data_sampple["trips"].astype("float")

    print(f"columns: {X.columns}")

    instances = X.to_dict(orient="records")
    data = {"input_data": instances}

    actual_response = requests.post(bentoml_endpoint_url, json=data).json()
    print("actual response:")

    print(json.dumps(actual_response, indent=2))

    expected_predictions = []
    for trip in y.values.tolist():
        data = {"model": "xgb-citibike-reg-model", "prediction": trip}
        expected_predictions.append(data)

    expected_response = {"predictions": expected_predictions}

    print("expected response:")

    print(json.dumps(expected_response, indent=2))

    # Umbral de tolerancia en porcentaje
    threshold = 15

    # Comparar cada valor de predicción con el umbral
    for i, (actual, expected) in enumerate(
        zip(actual_response["predictions"], expected_response["predictions"])
    ):
        actual = actual["prediction"]
        expected = expected["prediction"]
        assert within_percentage_threshold(actual, expected, threshold), (
            f"Prediction {i} outside the threshold: "
            f"present value {actual} and expected {expected}. "
            f"Percentage difference:{abs((actual - expected) / expected * 100):.2f}%"
        )

    print(f"All predictions are within the threshold {threshold}.")


def test_predict_trips():

    assert os.getenv("TEST_DATA_DIR") is not None, "Data dir is None"
    assert (
        os.getenv("BENTOML_PREDICT_TRIP_ENDPOINT_URL") is not None
    ), "Endpoint is None"
    bentoml_endpoint_url = os.getenv("BENTOML_PREDICT_TRIP_ENDPOINT_URL")

    test_dir = os.getenv("TEST_DATA_DIR")
    citibike_test_file = "test-modeling.parquet"
    citibike_test_path = os.path.join(test_dir, citibike_test_file)
    assert os.path.exists(
        citibike_test_path
    ), f"Don't found trips data {citibike_test_path}"

    model_data = pd.read_parquet(citibike_test_path)

    model_data_sample = model_data["2025-01-01 00:00:00":"2025-01-01 03:00:01"]

    model_data_sample.reset_index(inplace=True)
    model_data_sample.rename(columns={"index": "date"}, inplace=True)
    model_data_sample["date"] = model_data_sample["date"].apply(
        lambda x: x.isoformat()
    )
    X = model_data_sample[["date", "TMAX", "TMIN", "SNOW"]]
    y = model_data_sample["trips"].astype("float")

    instances = X.to_dict(orient="records")
    data = {"input_data": instances}
    print(f"actual response: {data}")

    actual_response = requests.post(bentoml_endpoint_url, json=data).json()
    print("actual response:")

    print(json.dumps(actual_response, indent=2))

    expected_predictions = []
    for trip in y.values.tolist():
        data = {"model": "xgb-citibike-reg-model", "prediction": trip}
        expected_predictions.append(data)

    expected_response = {"predictions": expected_predictions}

    print("expected response:")

    print(json.dumps(expected_response, indent=2))

    # Umbral de tolerancia en porcentaje
    threshold = 15

    # Comparar cada valor de predicción con el umbral
    for i, (actual, expected) in enumerate(
        zip(actual_response["predictions"], expected_response["predictions"])
    ):
        actual = actual["prediction"]
        expected = expected["prediction"]
        assert within_percentage_threshold(actual, expected, threshold), (
            f"Prediction {i} outside the threshold: "
            f"present value {actual} and expected {expected}. "
            f"Percentage difference:{abs((actual - expected) / expected * 100):.2f}%"
        )

    print(f"All predictions are within the threshold {threshold}.")
