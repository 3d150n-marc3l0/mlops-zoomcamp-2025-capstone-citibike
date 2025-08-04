import bentoml
import pandas as pd
import os
from bentoml.models import BentoModel
from pydantic import BaseModel, Field
from bentoml.io import JSON
from typing import List

path="."
dir_list = os.listdir(path)
print(dir_list)

print(os.environ)

@bentoml.service(
    resources={"cpu": "2"},
    traffic={"timeout": 10},
)
class CitibikeService:

    def __init__(self):
        self.model = bentoml.xgboost.load_model("xgb-citibike-reg-model:latest")

    # Modelo de entrada para una sola instancia
    class CitibikeInput(BaseModel):
        holiday: int = Field(..., example=0)
        TMAX: float = Field(..., example=28.0)
        TMIN: float = Field(..., example=17.0)
        hr_sin: float = Field(..., example=0.5)
        hr_cos: float = Field(..., example=0.866)
        weekday_sin: float = Field(..., example=0.0)
        weekday_cos: float = Field(..., example=1.0)
        week_sin: float = Field(..., example=0.707)
        week_cos: float = Field(..., example=0.707)
        mnth_sin: float = Field(..., example=0.5)
        mnth_cos: float = Field(..., example=0.866)

    @bentoml.api()
    def predict(
        self,
        input_data: List[CitibikeInput]
    ) -> dict:
        # Convertimos la lista de objetos Pydantic a una lista de dicts
        input_dicts = [item.dict() for item in input_data]
        print(input_dicts[0])

        # Convertimos a DataFrame
        df = pd.DataFrame(input_dicts)
        print(df.head(1))

        # Predicción
        preds = self.model.predict(df)

        return {"predictions": preds.tolist()}
