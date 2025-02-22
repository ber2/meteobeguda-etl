import datetime as dt
from pathlib import Path

import pandas as pd


class Writer:
    def __init__(self, date: dt.date):
        self.date = date

    @staticmethod
    def mkdir(path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)

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
        self.mkdir(path)
        with open(path, "wb") as fp:
            fp.write(raw)

    def df_to_disk(self, df: pd.DataFrame) -> None:
        path = self.csv_path()
        self.mkdir(path)
        df.to_csv(path, index=False)
