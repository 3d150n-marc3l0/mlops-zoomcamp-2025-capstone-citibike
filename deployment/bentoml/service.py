import bentoml
import pandas as pd
import numpy as np
import os
import datetime
import holidays
from bentoml.models import BentoModel
from pydantic import BaseModel, Field
from bentoml.io import JSON
from typing import List

path = "."
dir_list = os.listdir(path)
print(dir_list)

MODEL_NAME = "xgb-citibike-reg-model"


def is_holiday(date: datetime.date) -> int:
    """Función para determinar si un día es festivo o no en función del año de la fecha"""
    # Obtenemos los días festivos del año de la fecha proporcionada
    us_holidays = holidays.US(years=date.year)
    return 1 if date in us_holidays else 0


def get_datetime_features(trip_dt: datetime.date):
    return {
        "hr_sin": np.sin(trip_dt.hour * (2.0 * np.pi / 24)),
        "hr_cos": np.cos(trip_dt.hour * (2.0 * np.pi / 24)),
        "weekday_sin": np.sin(trip_dt.weekday() * (2.0 * np.pi / 7)),
        "weekday_cos": np.cos(trip_dt.weekday() * (2.0 * np.pi / 7)),
        "week_sin": np.sin((trip_dt.isocalendar()[1] - 1) * (2 * np.pi / 52)),
        "week_cos": np.cos((trip_dt.isocalendar()[1] - 1) * (2 * np.pi / 52)),
        "mnth_sin": np.sin((trip_dt.month - 1) * (2.0 * np.pi / 12)),
        "mnth_cos": np.cos((trip_dt.month - 1) * (2.0 * np.pi / 12)),
    }


@bentoml.service(
    resources={"cpu": "2"},
    traffic={"timeout": 10},
)
class CitibikeService:

    def __init__(self):
        self.model = bentoml.xgboost.load_model(f"{MODEL_NAME}:latest")

    class CitibikeRawInput(BaseModel):
        date: datetime.datetime
        TMAX: float = Field(..., example=28.0)
        TMIN: float = Field(..., example=17.0)
        SNOW: float = Field(..., example=1.0)

    # Modelo de entrada para una sola instancia
    class CitibikeInput(BaseModel):
        holiday: int = Field(..., example=0)
        TMAX: float = Field(..., example=28.0)
        TMIN: float = Field(..., example=17.0)
        SNOW: float = Field(..., example=1.0)
        hr_sin: float = Field(..., example=0.5)
        hr_cos: float = Field(..., example=0.866)
        weekday_sin: float = Field(..., example=0.0)
        weekday_cos: float = Field(..., example=1.0)
        week_sin: float = Field(..., example=0.707)
        week_cos: float = Field(..., example=0.707)
        mnth_sin: float = Field(..., example=0.5)
        mnth_cos: float = Field(..., example=0.866)

    @bentoml.api()
    def predict(self, input_data: List[CitibikeInput]) -> dict:
        # Convertimos la lista de objetos Pydantic a una lista de dicts
        input_dicts = [item.dict() for item in input_data]
        print(input_dicts[0])

        # Convertimos a DataFrame
        df = pd.DataFrame(input_dicts)
        print(df.head(1))

        # Predicción
        preds = self.model.predict(df)

        predictions = [
            {"model": MODEL_NAME, "prediction": pred}
            for pred in preds.tolist()
        ]
        return {"predictions": predictions}

    @bentoml.api()
    def predict_trip(self, input_data: List[CitibikeRawInput]) -> dict:
        input_dicts = [item.dict() for item in input_data]
        pro_input_dicts = []
        for item in input_dicts:
            data = {
                "holiday": is_holiday(item["date"]),
                "TMAX": item["TMAX"],
                "TMIN": item["TMIN"],
                "SNOW": item["SNOW"],
            }
            data = data | get_datetime_features(item["date"])
            pro_input_dicts.append(data)
        print(input_dicts[0])
        df = pd.DataFrame(pro_input_dicts)
        print(input_dicts[0])
        print(df.columns)
        preds = self.model.predict(df)
        predictions = [
            {"model": MODEL_NAME, "prediction": pred}
            for pred in preds.tolist()
        ]
        return {"predictions": predictions}
