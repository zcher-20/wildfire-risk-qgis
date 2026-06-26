"""
Cleans raw NASA FIRMS fire detection data for Morocco and exports a processed CSV
ready for GeoJSON conversion and QGIS ingestion.

Input:  data/raw/FIRMS_morocco.csv  (downloaded from https://firms.modaps.eosdis.nasa.gov)
Output: data/processed/morocco_fires_clean.csv
"""

import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/FIRMS_morocco.csv")
OUT_PATH = Path("data/processed/morocco_fires_clean.csv")

# Morocco bounding box  (lon_min, lat_min, lon_max, lat_max)
BBOX = (-17.2, 21.0, -1.0, 36.0)

# FIRMS VIIRS confidence codes: n=nominal, h=high, l=low
VALID_CONFIDENCE = {"n", "h"}


def load_raw(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["acq_date"])
    print(f"Loaded {len(df):,} raw detections")
    return df


def filter_morocco(df: pd.DataFrame) -> pd.DataFrame:
    lon_min, lat_min, lon_max, lat_max = BBOX
    mask = (
        df["longitude"].between(lon_min, lon_max)
        & df["latitude"].between(lat_min, lat_max)
    )
    result = df[mask].copy()
    print(f"After bounding-box filter: {len(result):,} detections")
    return result


def filter_confidence(df: pd.DataFrame) -> pd.DataFrame:
    result = df[df["confidence"].str.lower().isin(VALID_CONFIDENCE)].copy()
    print(f"After confidence filter: {len(result):,} detections")
    return result


def filter_vegetation_fires(df: pd.DataFrame) -> pd.DataFrame:
    # type 0 = presumed vegetation fire; NRT rows have no type (NaN) — keep those too
    if "type" in df.columns:
        result = df[df["type"].isna() | (df["type"] == 0)].copy()
        print(f"After vegetation-type filter: {len(result):,} detections")
        return result
    return df


def select_columns(df: pd.DataFrame) -> pd.DataFrame:
    keep = [
        "latitude", "longitude", "brightness", "acq_date",
        "acq_time", "satellite", "confidence", "frp",
    ]
    available = [c for c in keep if c in df.columns]
    return df[available]


def main():
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df = load_raw(RAW_PATH)
    df = filter_morocco(df)
    df = filter_confidence(df)
    df = filter_vegetation_fires(df)
    df = select_columns(df)
    df = df.drop_duplicates(subset=["latitude", "longitude", "acq_date", "acq_time"])
    df.to_csv(OUT_PATH, index=False)
    print(f"Saved cleaned data → {OUT_PATH}  ({len(df):,} records)")


if __name__ == "__main__":
    main()
