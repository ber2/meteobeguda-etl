import datetime as dt
from io import BytesIO

import pandas as pd
import numpy as np


COLUMNS = {
    "date": np.dtype("O"),
    "time": np.dtype("O"),
    "temperature": np.dtype("float64"),
    "temperature_max": np.dtype("float64"),
    "temperature_min": np.dtype("float64"),
    "humidity": np.dtype("int64"),
    "dew": np.dtype("float64"),
    "windspeed": np.dtype("float64"),
    "wind_direction": pd.StringDtype(),
    "wind_rec": np.dtype("float64"),
    "windspeed_max": np.dtype("float64"),
    "windspeed_max_direction": pd.StringDtype(),
    "temperature_feeling": np.dtype("float64"),
    "heat_index": np.dtype("float64"),
    "thw_index": np.dtype("float64"),
    "pressure": np.dtype("float64"),
    "rain": np.dtype("float64"),
    "rain_intensity": np.dtype("float64"),
    "heat_degrees": np.dtype("float64"),
    "cold_degrees": np.dtype("float64"),
    "temperature_interior": np.dtype("float64"),
    "humidity_interior": np.dtype("int64"),
    "dew_interior": np.dtype("float64"),
    "heat_index_interior": np.dtype("float64"),
    "air_density_interior": np.dtype("float64"),
    "wind_direction_degrees": np.dtype("float64"),
    "tx_wind": np.dtype("int64"),
    "iss_reception": np.dtype("int64"),
    "arc_interior": np.dtype("float64"),
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
    )


def parse_timestamps_and_add_date(data: pd.DataFrame) -> None:
    data["timestamp"] = pd.to_datetime(data["date"] + " " + data["time"], dayfirst=True)
    data.drop(["date", "time"], axis=1, inplace=True)
    data["date"] = data.timestamp.dt.date


def only_one_day(date: dt.date, data: pd.DataFrame) -> pd.DataFrame:
    threshold_timestamp = pd.Timestamp(date + dt.timedelta(1))
    return data[data.timestamp <= threshold_timestamp].copy()


def reorder_columns(data: pd.DataFrame) -> pd.DataFrame:
    new_columns = ["date", "timestamp"] + list(data.columns[0:-2])
    return data[new_columns]


def parse_response(date: dt.date, raw: bytes) -> pd.DataFrame:
    data = load_bytes(raw)
    parse_timestamps_and_add_date(data)
    new_columns = reorder_columns(data)
    return only_one_day(date, new_columns)
