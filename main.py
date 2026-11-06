"""Small file-backed API for the Thai zoo visitor statistics resource."""

import csv
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException

ROOT = Path(__file__).resolve().parent
CSV_FILE = ROOT / "zoo_visitors_january_2569.csv"

app = FastAPI(title="Zoo Visitor Statistics", version="1.0.0")


def parse_cell(value: str | None) -> Any:
    """Convert blank cells to null and comma-formatted counts to integers."""
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    try:
        return int(value.replace(",", ""))
    except ValueError:
        return value


def read_csv_rows() -> list[dict[str, Any]]:
    if not CSV_FILE.exists():
        raise HTTPException(status_code=500, detail="CSV data file is missing")

    try:
        with CSV_FILE.open(encoding="utf-8-sig", newline="") as source_file:
            table = csv.DictReader(source_file)
            result = []
            for source_row in table:
                row = {
                    column.strip(): parse_cell(cell)
                    for column, cell in source_row.items()
                    if column and column.strip()
                }
                if any(cell is not None for cell in row.values()):
                    result.append(row)
            return result
    except (OSError, UnicodeError, csv.Error) as error:
        raise HTTPException(status_code=500, detail=f"Could not read CSV: {error}") from error


@app.get("/api/zoo-visitors", tags=["Zoo visitor statistics"])
def zoo_visitors() -> dict[str, Any]:
    rows = read_csv_rows()
    return {
        "source": "Data.go.th - Open Government Data of Thailand",
        "dataset": "ข้อมูลรายงานสถิติจำนวนผู้เข้าชมสวนสัตว์ ปีงบประมาณ 2569",
        "dataset_url": "https://data.go.th/dataset/zoo-visitors2569",
        "dataset_id": "970c2632-1669-44aa-80c5-2c20cb2295e4",
        "resource_id": "0ecc96cf-d914-42a1-b184-dbbd013c3c9c",
        "resource": "ข้อมูลรายงานสถิติจำนวนผู้เข้าชมสวนสัตว์ อสส มกราคม 2569",
        "fiscal_year": 2569,
        "records_count": len(rows),
        "records": rows,
    }


@app.get("/", include_in_schema=False)
def home() -> dict[str, str]:
    return {"api": "/api/zoo-visitors", "documentation": "/docs"}
