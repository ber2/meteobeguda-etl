import datetime as dt
from pathlib import Path
import sqlite3

import pandas as pd

import pytest

from meteobeguda.sqlite import SqliteClient


@pytest.fixture
def test_db():
    path = Path("tests/resources/test_db.sqlite")
    fixture_data = sqlite3.connect(path)
    client = SqliteClient(":memory:")
    fixture_data.backup(client.con)
    fixture_data.close()
    yield client
    client.con.close()


@pytest.fixture
def one_row():
    return pd.DataFrame(
        [
            {
                "date": "2022-05-12",
                "timestamp": "2022-05-12 00:15:00",
                "temperature": 13.6,
                "temperature_max": 13.6,
                "temperature_min": 13.4,
                "humidity": 93,
                "dew": 12.4,
                "windspeed": 1.6,
                "wind_direction": "NO",
                "wind_rec": 0.4,
                "windspeed_max": 4.8,
                "windspeed_max_direction": "NO",
                "temperature_feeling": 13.6,
                "heat_index": 13.7,
                "thw_index": 13.7,
                "pressure": 1019.0,
                "rain": 0.0,
                "rain_intensity": 0.0,
                "heat_degrees": 0.05,
                "cold_degrees": 0.0,
                "temperature_interior": 22.3,
                "humidity_interior": 60,
                "dew_interior": 14.1,
                "heat_index_interior": 22.3,
                "air_density_interior": 11.01,
                "wind_direction_degrees": 1.1832,
                "tx_wind": 349,
                "iss_reception": 1,
                "arc_interior": 100.0,
            }
        ]
    )


class TestSqliteClient:
    def test_db_initial_state(self, test_db):
        row_count = test_db.con.execute(
            "select count(*) from meteobeguda_events;"
        ).fetchone()[0]
        assert row_count == 285

        expected_counts_per_date = pd.DataFrame(
            [
                {"date": "2022-05-01", "cnt": 95},
                {"date": "2022-05-02", "cnt": 95},
                {"date": "2022-05-03", "cnt": 95},
            ]
        )

        actual_counts_per_date = pd.read_sql(
            "SELECT date, count(*) as cnt FROM meteobeguda_events GROUP BY date ORDER BY date;",
            test_db.con,
        )

        pd.testing.assert_frame_equal(expected_counts_per_date, actual_counts_per_date)

    def test_delete_for_date(self, test_db):
        date = dt.date(2022, 5, 2)
        test_db.delete_for_date(date)

        new_count = test_db.con.execute(
            "select count(*) from meteobeguda_events;"
        ).fetchone()[0]
        assert new_count == 190

        new_count_for_date = test_db.con.execute(
            f"select count(*) from meteobeguda_events where date = '{date.isoformat()}';"
        ).fetchone()[0]
        assert new_count_for_date == 0

    def test_append_data(self, test_db, one_row):
        test_db.append_data(one_row)

        new_count = test_db.con.execute(
            "select count(*) from meteobeguda_events;"
        ).fetchone()[0]
        assert new_count == 286

        new_date_df = pd.read_sql(
            "select * from meteobeguda_events where date = '2022-05-12';", test_db.con
        )
        pd.testing.assert_frame_equal(one_row, new_date_df)

    def test_delete_and_append_is_idempotent(self, test_db, one_row):
        date = dt.date(2022, 5, 12)
        test_db.delete_and_append(date, one_row)
        test_db.delete_and_append(date, one_row)

        count_for_date = test_db.con.execute(
            f"select count(*) from meteobeguda_events where date = '{date.isoformat()}';"
        ).fetchone()[0]
        assert count_for_date == 1
