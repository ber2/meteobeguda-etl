import datetime as dt
from pathlib import Path

import pandas as pd


class Writer:
    def __init__(self, date: dt.date):
        self.date = date

    def raw_path(self) -> Path:
        return (
            Path("data/lake/raw")
            / self.date.strftime("%Y/%m")
            / f"{self.date.isoformat()}.txt"
        )

    def csv_path(self) -> Path:
        return (
            Path("data/lake/parsed")
            / self.date.strftime("%Y/%m")
            / f"{self.date.isoformat()}.csv"
        )

    def bytes_to_disk(self, raw: bytes) -> None:
        path = self.raw_path()
        path.parent.mkdir(parents=True)
        with open(path, "wb") as fp:
            fp.write(raw)

    def df_to_disk(self, df: pd.DataFrame) -> None:
        path = self.csv_path()
        path.parent.mkdir(parents=True)
        df.to_csv(path, index=False)

