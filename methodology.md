# Methodology

## Overview

This project maps historical wildfire occurrence in Morocco using open satellite fire detection data and a QGIS-based geospatial workflow. The goal is to visualize fire density, seasonality, and intensity patterns across Moroccan regions.

---

## Data Sources

| Dataset | Source | Format | Description |
|---------|--------|--------|-------------|
| Fire detections | NASA FIRMS (VIIRS S-NPP 375m) | CSV | Active fire detections with lat/lon, date, FRP, and confidence |
| Administrative boundaries | GADM v4.1 | GeoPackage | Morocco province/region polygons |
| Elevation | SRTM 30m | GeoTIFF | Digital elevation model for terrain context |
| Land cover | ESA WorldCover 2021 | GeoTIFF | 10m resolution land use / vegetation classification |

---

## Workflow

### Step 1 — Data Acquisition

Download VIIRS fire detection archive from NASA FIRMS for the Morocco bounding box (lon: −17.2 to −1.0, lat: 21.0 to 36.0). Export as CSV.

### Step 2 — Data Cleaning (`scripts/clean_fire_data.py`)

- Filter to Morocco bounding box
- Remove low-confidence detections (keep "nominal" and "high" only for VIIRS; ≥60 for MODIS)
- Deduplicate on (latitude, longitude, acq_date, acq_time)
- Output: `data/processed/morocco_fires_clean.csv`

### Step 3 — GeoJSON / GeoPackage Export (`scripts/export_geojson.py`)

- Convert CSV to GeoDataFrame using GeoPandas
- Add derived fields: year, month, season
- Export to GeoJSON (for web use) and GeoPackage (for QGIS)

### Step 4 — QGIS Layer Setup

1. Load `morocco_fires.gpkg` → fire_points layer
2. Load GADM Morocco boundaries
3. (Optional) Load SRTM DEM as hillshade base layer
4. Apply graduated symbol renderer by FRP (Fire Radiative Power)
5. Perform spatial join: count fire points per region

### Step 5 — Risk Classification

Regions are classified into fire-risk tiers by combining:
- Fire occurrence density (points/km²)
- Peak fire season frequency (June–September)
- Proximity to forests or wildland-urban interface

### Step 6 — Map Export

Final maps exported at 300 DPI from QGIS print layout:
- `maps/wildfire_points_map.png` — raw fire detection scatter
- `maps/regional_risk_map.png` — choropleth by region fire density

---

## Coordinate Reference System

All layers are stored in **WGS 84 (EPSG:4326)**. For area calculations, data is reprojected to **UTM Zone 29N (EPSG:32629)** within QGIS processing.

---

## Limitations

- FIRMS detections are instantaneous thermal anomalies — they capture active fire, not burned area.
- Cloud cover can suppress detections; fire counts may underrepresent cloudy seasons.
- FRP intensity is sensor- and geometry-dependent and should not be used as an absolute energy measure across sensors.
