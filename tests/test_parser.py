import datetime as dt
import pickle

import pytest

import pandas as pd
import numpy as np

from meteobeguda.parser import (
    COLUMNS,
    load_bytes,
    parse_timestamps_and_add_date,
    reorder_columns,
    parse_response,
    only_one_day
)


@pytest.fixture
def raw_input():
    with open("tests/resources/downld02.txt", "rb") as fp:
        raw = fp.read()
    return raw


@pytest.fixture
def loaded_df(raw_input):
    return load_bytes(raw_input)


@pytest.fixture
def parsed_timestamps():
    input_data = {
        "date": ["5/03/2022", "11/03/2022", "9/2/1985"],
        "time": ["18:00", "19:00", "06:30"],
    }
    df = pd.DataFrame(input_data)
    parse_timestamps_and_add_date(df)
    return df


@pytest.fixture
def loaded_df_with_timestamps(loaded_df):
    parse_timestamps_and_add_date(loaded_df)
    return loaded_df


@pytest.fixture
def df_with_only_dates():
    return pd.DataFrame(
        [
            {"timestamp": pd.Timestamp("2022-03-14 00:15:00"), "other": 2},
            {"timestamp": pd.Timestamp("2022-03-15 00:00:00"), "other": 3},
            {"timestamp": pd.Timestamp("2022-03-15 00:15:00"), "other": 4},
        ]
    )


@pytest.fixture
def expected_parsed_response():
    with open("tests/resources/parsed_response.pkl", "rb") as fp:
        df = pickle.load(fp)
    return df


def test_loaded_bytes_has_all_columns(loaded_df):
    assert loaded_df.shape[1] == 29


def test_loaded_bytes_column_names(loaded_df):
    assert loaded_df.columns.to_list() == list(COLUMNS.keys())


def test_loaded_numerical_columns_are_inferred(loaded_df):
    expected_dtypes = pd.Series(COLUMNS.values(), index=COLUMNS.keys())
    pd.testing.assert_series_equal(expected_dtypes, loaded_df.dtypes)


def test_temperatures_are_ordered(loaded_df):
    mask = (loaded_df.temperature_min <= loaded_df.temperature) & (
        loaded_df.temperature <= loaded_df.temperature_max
    )
    assert loaded_df[~mask].shape[0] == 0


def test_windspeed_max_is_higher_than_windspeed(loaded_df):
    mask = loaded_df.windspeed <= loaded_df.windspeed_max
    assert loaded_df[~mask].shape[0] == 0


def test_timestamps_are_properly_parsed(parsed_timestamps):
    expected_timestamps = pd.DataFrame(
        [
            {
                "timestamp": pd.Timestamp("2022-03-05 18:00:00"),
                "date": dt.date(2022, 3, 5),
            },
            {
                "timestamp": pd.Timestamp("2022-03-11 19:00:00"),
                "date": dt.date(2022, 3, 11),
            },
            {
                "timestamp": pd.Timestamp("1985-02-09 06:30:00"),
                "date": dt.date(1985, 2, 9),
            },
        ]
    )

    pd.testing.assert_frame_equal(expected_timestamps, parsed_timestamps)


def test_old_time_column_is_dropped_after_parsing_timestamps(parsed_timestamps):
    assert "time" not in parsed_timestamps.columns


def test_final_df_has_enough_rows(loaded_df_with_timestamps):
    assert loaded_df_with_timestamps.shape[0] == 155


def test_final_df_has_columns(loaded_df_with_timestamps):
    assert loaded_df_with_timestamps.shape[1] == 29


def test_final_df_min_timestamp(loaded_df_with_timestamps):
    assert loaded_df_with_timestamps.timestamp.min() == pd.Timestamp(
        "2022-03-11 00:15:00"
    )


def test_final_df_max_timestamp(loaded_df_with_timestamps):
    assert loaded_df_with_timestamps.timestamp.max() == pd.Timestamp(
        "2022-03-12 14:45:00"
    )


def test_only_one_day(df_with_only_dates):
    date = dt.date(2022, 3, 14)
    expected = pd.DataFrame(
        [
            {"timestamp": pd.Timestamp("2022-03-14 00:15:00"), "other": 2},
            {"timestamp": pd.Timestamp("2022-03-15 00:00:00"), "other": 3},
        ]
    )
    actual = only_one_day(date, df_with_only_dates)
    pd.testing.assert_frame_equal(expected, actual)


def test_column_reordering():
    input_data = pd.DataFrame(
        [{"one_column": 2, "other_column": 3, "timestamp": 4, "date": 5}]
    )

    expected_column_order = ["date", "timestamp", "one_column", "other_column"]
    actual_column_order = reorder_columns(input_data).columns.to_list()
    assert expected_column_order == actual_column_order


def test_end_to_end_parsing(raw_input, expected_parsed_response):
    date = dt.date(2022, 3, 11)
    actual_parsed_response = parse_response(date, raw_input)
    pd.testing.assert_frame_equal(expected_parsed_response, actual_parsed_response)
