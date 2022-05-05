import datetime as dt
from pathlib import Path
import shutil

import pandas as pd

import pytest

from meteobeguda.writer import Writer


@pytest.fixture
def writer():
    yield Writer(dt.date(1990, 5, 4))
    shutil.rmtree("data/lake/raw/1990/", ignore_errors=True)
    shutil.rmtree("data/lake/parsed/1990/", ignore_errors=True)



@pytest.fixture
def some_bytes():
    return b"hello there"


@pytest.fixture
def small_df():
    return pd.DataFrame([
        {"a": 0, "b": "one", "c": pd.Timestamp("1990-05-04 00:00:00")},
        {"a": 1, "b": "other", "c": pd.Timestamp("1990-05-04 00:15:00")},
    ])


class TestWriter:

    def test_raw_path_formatter(self, writer):
        expected_path = Path("data/lake/raw/1990/05/1990-05-04.txt")
        assert expected_path == writer.raw_path()

    def test_csv_path_formatter(self, writer):
        expected_path = Path("data/lake/parsed/1990/05/1990-05-04.csv")
        assert expected_path == writer.csv_path()

    def test_bytes_to_disk(self, writer, some_bytes):
        expected_path = writer.raw_path()
        writer.bytes_to_disk(some_bytes)

        with open(expected_path, "rb") as fp:
            actual_bytes = fp.read()

        assert some_bytes == actual_bytes

    def test_df_to_disk(self, writer, small_df):
        expected_path = writer.csv_path()
        writer.df_to_disk(small_df)

        actual_df = pd.read_csv(expected_path, parse_dates=["c"])
        pd.testing.assert_frame_equal(small_df, actual_df)
