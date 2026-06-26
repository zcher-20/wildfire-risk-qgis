"""
Converts the cleaned fire CSV to a GeoJSON FeatureCollection and a GeoPackage layer.

Input:  data/processed/morocco_fires_clean.csv
Output: data/processed/morocco_fires.geojson
        data/processed/morocco_fires.gpkg  (layer: fire_points)
"""

import geopandas as gpd
import pandas as pd
from pathlib import Path
from shapely.geometry import Point

IN_CSV = Path("data/processed/morocco_fires_clean.csv")
OUT_GEOJSON = Path("data/processed/morocco_fires.geojson")
OUT_GPKG = Path("data/processed/morocco_fires.gpkg")
CRS = "EPSG:4326"


def csv_to_geodataframe(path: Path) -> gpd.GeoDataFrame:
    df = pd.read_csv(path, parse_dates=["acq_date"])
    geometry = [Point(lon, lat) for lon, lat in zip(df["longitude"], df["latitude"])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs=CRS)
    return gdf


def add_derived_fields(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    gdf["year"] = gdf["acq_date"].dt.year
    gdf["month"] = gdf["acq_date"].dt.month
    gdf["season"] = gdf["month"].map({
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Spring", 4: "Spring", 5: "Spring",
        6: "Summer", 7: "Summer", 8: "Summer",
        9: "Autumn", 10: "Autumn", 11: "Autumn",
    })
    return gdf


def main():
    OUT_GEOJSON.parent.mkdir(parents=True, exist_ok=True)
    gdf = csv_to_geodataframe(IN_CSV)
    gdf = add_derived_fields(gdf)

    gdf.to_file(OUT_GEOJSON, driver="GeoJSON")
    print(f"Exported GeoJSON → {OUT_GEOJSON}")

    gdf.to_file(OUT_GPKG, layer="fire_points", driver="GPKG")
    print(f"Exported GeoPackage → {OUT_GPKG} (layer: fire_points)")

    print(f"\nSummary: {len(gdf):,} fire points | years: {gdf['year'].min()}–{gdf['year'].max()}")


if __name__ == "__main__":
    main()
