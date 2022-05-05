import datetime as dt
import logging
from pathlib import Path
from sqlite3 import connect, Connection

import pandas as pd


class SqliteClient:

    def __init__(self, db_path: Path):
        self.con = connect(db_path)
        self.table = "meteobeguda_events"

    def delete_for_date(self, date: dt.date) -> None:
        start_timestamp = (
            dt.datetime
            .combine(date, dt.time(0, 15))
            .strftime("%Y-%m-%d %H:%M:%S")
        )
        end_timestamp = (
            dt.datetime
            .combine(
                date + dt.timedelta(1), dt.time(0, 0)
            )
            .strftime("%Y-%m-%d %H:%M:%S")
        )
        query = f"DELETE FROM {self.table} WHERE timestamp between '{start_timestamp}' and '{end_timestamp}';"
        logging.debug("Running query: %s", query)
        self.con.execute(query)

    def append_data(self, df: pd.DataFrame) -> None:
        df.to_sql(
            self.table,
            self.con,
            if_exists="append",
            index=False
        )

    def delete_and_append(self, date: dt.date, df: pd.DataFrame) -> None:
        self.delete_for_date(date)
        self.append_data(df)

    def close(self) -> None:
        self.con.close()
