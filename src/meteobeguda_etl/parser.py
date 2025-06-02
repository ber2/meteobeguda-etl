import datetime as dt
from io import BytesIO

import pandas as pd
import numpy as np


COLUMNS = {
    "date": np.dtype("O"),
    "time": np.dtype("O"),
    "temperature": pd.Float64Dtype(),
    "temperature_max": pd.Float64Dtype(),
    "temperature_min": pd.Float64Dtype(),
    "humidity": pd.Int64Dtype(),
    "dew": pd.Float64Dtype(),
    "windspeed": pd.Float64Dtype(),
    "wind_direction": pd.StringDtype(),
    "wind_rec": pd.Float64Dtype(),
    "windspeed_max": pd.Float64Dtype(),
    "windspeed_max_direction": pd.StringDtype(),
    "temperature_feeling": pd.Float64Dtype(),
    "heat_index": pd.Float64Dtype(),
    "thw_index": pd.Float64Dtype(),
    "pressure": pd.Float64Dtype(),
    "rain": pd.Float64Dtype(),
    "rain_intensity": pd.Float64Dtype(),
    "heat_degrees": pd.Float64Dtype(),
    "cold_degrees": pd.Float64Dtype(),
    "temperature_interior": pd.Float64Dtype(),
    "humidity_interior": pd.Int64Dtype(),
    "dew_interior": pd.Float64Dtype(),
    "heat_index_interior": pd.Float64Dtype(),
    "air_density_interior": pd.Float64Dtype(),
    "wind_direction_degrees": pd.Float64Dtype(),
    "tx_wind": pd.Int64Dtype(),
    "iss_reception": pd.Int64Dtype(),
    "arc_interior": pd.Float64Dtype(),
}


def load_bytes(raw: bytes) -> pd.DataFrame:
    return pd.read_csv(
        BytesIO(raw),
        sep=r"\s+",
        header=None,
        skiprows=3,
        encoding="latin1",
        names=COLUMNS.keys(),
        index_col=False,
        dtype=COLUMNS,
        na_values=["---", "------"],
    )


def parse_timestamps_and_add_date(data: pd.DataFrame) -> None:
    data["timestamp"] = pd.to_datetime(data["date"] + " " + data["time"], dayfirst=True)
    data.drop(["date", "time"], axis=1, inplace=True)
    data["date"] = data.timestamp.dt.date


def only_one_day(date: dt.date, data: pd.DataFrame) -> pd.DataFrame:
    min_ts = pd.Timestamp(date)
    max_ts = pd.Timestamp(date + dt.timedelta(1))
    mask = data.timestamp.between(min_ts, max_ts, inclusive="right")
    return data[mask].copy()


def reorder_columns(data: pd.DataFrame) -> pd.DataFrame:
    new_columns = ["date", "timestamp"] + list(data.columns[0:-2])
    return data[new_columns]


def parse_response(date: dt.date, raw: bytes) -> pd.DataFrame:
    data = load_bytes(raw)
    parse_timestamps_and_add_date(data)
    new_columns = reorder_columns(data)
    return only_one_day(date, new_columns)
