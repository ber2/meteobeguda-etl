import datetime as dt
import logging
from pathlib import Path
import sys

import pandas as pd

from meteobeguda.request import get_last_two_days
from meteobeguda.parser import parse_response
from meteobeguda.sqlite import SqliteClient
from meteobeguda.writer import Writer


SQLITE_PATH = Path("data/warehouse/meteobeguda_post_2020.sqlite")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)


def main():
    yesterday = dt.date.today() - dt.timedelta(1)
    writer = Writer(yesterday)
    logging.info("Fetching data for date: %s", yesterday.isoformat())

    raw_data: bytes = get_last_two_days()
    logging.info("Retrieved %d bytes", sys.getsizeof(raw_data))
    writer.bytes_to_disk(raw_data)
    logging.info("Written raw data into %s", str(writer.raw_path()))

    df_yesterday: pd.DataFrame = parse_response(yesterday, raw_data)
    logging.info("Parsed into %d rows", df_yesterday.shape[0])
    writer.df_to_disk(df_yesterday)
    logging.info("Written parsed data into %s", str(writer.csv_path()))

    logging.info("Loading into sqlite database")
    db = SqliteClient(SQLITE_PATH)
    db.delete_and_append(yesterday, df_yesterday)
    db.close()
    logging.info("All done")


if __name__ == "__main__":
    main()
