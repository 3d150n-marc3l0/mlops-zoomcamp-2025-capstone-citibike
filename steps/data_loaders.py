"""Data loader steps for the Iris classification pipeline."""

#import logging
from typing import Optional, Tuple, List
import time
import numpy as np
import datetime
import pandas as pd
#from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from typing_extensions import Annotated
from zenml import step
from zenml.logger import get_logger

logger = get_logger(__name__)

DATASET_PREDICTION_COLUMN_NAME = 'prediction'
DATASET_TARGET_COLUMN_NAME = "trips"
DATASET_NUMERICAL_COLUMNS = [
    'TMAX', 'TMIN', 'hr_sin', 'hr_cos', 'weekday_sin', 'weekday_cos', 'week_sin', 'week_cos', 'mnth_sin', 'mnth_cos'
] # numerical_features
DATASET_CATEGORICAL_COLUMNS = ["holiday"] # categorical_features



def load_data_by_year(
    base_url: str,
    year: int
) -> Tuple[Annotated[pd.DataFrame, "trips_data"], Annotated[pd.DataFrame, "weather_data"]]:
    # Read Trips data
    i_trip_file = f"{year}-citibike-tripdata.parquet"
    i_trip_url = base_url + "citibike/" + i_trip_file
    logger.info(f"Reading data from data url {i_trip_url}...")
    i_trips_data = pd.read_parquet(i_trip_url)

    # Read Weather data
    i_weather_file = f"{year}-weather.parquet"
    i_weather_url = base_url + "weather/" + i_weather_file
    logger.info(f"Reading data from data url {i_weather_url}...")
    i_weather_data = pd.read_parquet(i_weather_url)
    
    return i_trips_data, i_weather_data



@step(
    enable_cache=False
)
def data_loader(
    base_url: str,
    start_date: datetime.date, 
    end_date: datetime.date,
) -> Tuple[Annotated[pd.DataFrame, "dataset"], Annotated[str, "target"]]:
#) -> Annotated[pd.DataFrame, "dataset"]:
    logger.info(f"Loading data from base_url {base_url}...")
    start_time = time.time()

    trips_data_list = []
    weather_data_list = []
    for current_year in list(range(start_date.year, end_date.year + 1)):
        # Read Trips data
        i_trips_data, i_weather_data = load_data_by_year(base_url=base_url, year=current_year)
        trips_data_list.append(i_trips_data)
        weather_data_list.append(i_weather_data)

    # Concat data bu years
    trips_data = pd.concat(trips_data_list, ignore_index=True)
    weather_data = pd.concat(weather_data_list, ignore_index=True)

    # Merge trips and weather data
    modeling_data = trips_data.merge(weather_data, how='inner', left_on='date', right_on='DATE')
    modeling_data.index = modeling_data.apply(lambda row: datetime.datetime.combine(row.date.date(), datetime.time(row.hour)), axis=1)

    # Print runing time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.2f} seconds")

    
    #return modeling_data
    return modeling_data, DATASET_TARGET_COLUMN_NAME


@step
def data_splitter(
    dataset: pd.DataFrame,
    test_size: float = 0.2,
    shuffle: bool = True,
    random_state: int = 42,
) -> Tuple[Annotated[pd.DataFrame, "train"], Annotated[pd.DataFrame, "test"]]:
    """Split the dataset into train and test (validation) subsets.

    Args:
        dataset: The dataset to split.
        test_size: The size of the test subset.
        shuffle: Whether to shuffle the dataset.
        random_state: The random state to use for shuffling.

    Returns:
        The train and test (validation) subsets of the dataset.
    """
    train, test = train_test_split(
        dataset,
        test_size=test_size,
        shuffle=shuffle,
        random_state=random_state,
    )

    logger.debug(f"train.dtypes: {train.dtypes}")
    logger.debug(f"test.dtypes : {test.dtypes}")

    return train, test


@step(
    #enable_cache=False
)
def data_preprocessor(
      dataset: pd.DataFrame, 
      is_reference: bool = False
) -> Annotated[pd.DataFrame, "clean_dataset"]: 
    # Copy
    data = dataset.copy()
    
    #data['holiday'] = data['holiday'].map({1: 'Yes', 0: 'No'})

    # Create day of the week feature
    data['weekday'] = data['date'].dt.dayofweek

    # Create day of the year feature
    data['week_num'] = data['date'].dt.isocalendar().week

    # Create month number column
    data['mnth'] = data['date'].dt.month
    
    # New Features
    data['hr_sin'] = np.sin(data.hour * (2.*np.pi/24))
    data['hr_cos'] = np.cos(data.hour * (2.*np.pi/24))
    data['weekday_sin'] = np.sin(data.weekday * (2.*np.pi/7))
    data['weekday_cos'] = np.cos(data.weekday * (2.*np.pi/7))
    data['week_sin'] = np.sin((data.week_num-1) * (2*np.pi/52))
    data['week_cos'] = np.cos((data.week_num-1) * (2*np.pi/52))
    data['mnth_sin'] = np.sin((data.mnth - 1) * (2.*np.pi/12))
    data['mnth_cos'] = np.cos((data.mnth - 1) * (2.*np.pi/12))


    data['week_sin'] = data['week_sin'].astype('float64')
    data['week_cos'] = data['week_cos'].astype('float64')
    
    # drop 'Start Station Name' y 'End Station Name' colums
    # Drop columns
    drop_columns = [
        'date', 'hour',
        'weekday', 'mnth', 'week_num', 
        'DATE', 'AWND', 'PRCP', 'SNOW', 'SNWD', 'TAVG', 
    ]
    if not is_reference and 'datetime' in data.columns:
        drop_columns = drop_columns + ['datetime']
    data = data.drop(columns=drop_columns)

    logger.debug(f"data: {data.dtypes}")

    return data


@step(
    enable_cache=False
)
def reference_data_loader(
    base_url: str,
    start_reference_date: datetime.date, 
    end_reference_date: datetime.date,
	start_current_date: datetime.date, 
    end_current_date: datetime.date
) -> Tuple[
    Annotated[pd.DataFrame, "reference_data"],
    Annotated[pd.DataFrame, "comparison_data"],
    Annotated[str, "target"],
    #Annotated[List[str], "categorical"],
    #Annotated[List[str], "numerical"]
]:
    logger.info(f"Loading data from base_url {base_url}...")
    start_time = time.time()
    
    reference_data, target = data_loader(
        base_url=base_url,
        start_date=start_reference_date, 
        end_date=end_reference_date,
    )
    reference_data = reference_data[(reference_data.index.date >= start_reference_date) & (reference_data.index.date <= end_reference_date)]
    logger.info(f"reference_data: {reference_data.shape}")

    comparison_data, target = data_loader(
        base_url=base_url,
        start_date=start_current_date, 
        end_date=end_current_date,
    )
    comparison_data = comparison_data[(comparison_data.index.date >= start_current_date) & (comparison_data.index.date <= end_current_date)]
    logger.info(f"reference_data: {comparison_data.shape}")

    # Print runing time
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"Execution time: {elapsed_time:.2f} seconds")

    
    #return modeling_data
    #return reference_data, comparison_data, DATASET_TARGET_COLUMN_NAME, DATASET_CATEGORICAL_COLUMNS, DATASET_NUMERICAL_COLUMNS
    return reference_data, comparison_data, target
