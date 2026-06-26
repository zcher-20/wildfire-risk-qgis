# Morocco Wildfire Risk Mapping — QGIS + Python

A geospatial wildfire-risk mapping project using QGIS, Python, and open Earth observation data. The project visualizes fire occurrence patterns, prepares spatial datasets, and produces reproducible wildfire-risk maps for Morocco.

Complements the [RICER wildfire prediction model](https://github.com/zaynebcherif) by adding the geospatial and visual layer to the ML/data-science workflow.

---

## Project structure

```
wildfire-risk-qgis/
├── data/
│   ├── raw/               # NASA FIRMS CSVs (not committed — see Data section)
│   └── processed/         # Cleaned CSV, GeoJSON, GeoPackage
├── qgis/
│   ├── wildfire_mapping_project.qgz   # QGIS project file
│   └── exported_maps/                 # QGIS layout exports
├── notebooks/
│   └── 01_data_cleaning.ipynb         # EDA + preprocessing walkthrough
├── scripts/
│   ├── clean_fire_data.py             # Filters and cleans raw FIRMS CSV
│   ├── export_geojson.py              # CSV → GeoJSON / GeoPackage
│   └── pyqgis_style_layers.py         # PyQGIS styling + map export
├── maps/                              # Final exported map images
├── methodology.md                     # Full methodology writeup
└── README.md
```

---

## Quickstart

### 1. Install dependencies

```bash
pip install pandas geopandas matplotlib shapely
```

### 2. Download fire data

Go to [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/download/), select:
- **Product:** VIIRS S-NPP 375m
- **Region:** draw Morocco bounding box (lon −17.2 to −1.0, lat 21.0 to 36.0)
- **Date range:** your target years
- **Format:** CSV

Save to `data/raw/FIRMS_morocco.csv`.

### 3. Run preprocessing

```bash
python scripts/clean_fire_data.py
python scripts/export_geojson.py
```

### 4. Open in QGIS

Load `data/processed/morocco_fires.gpkg` into QGIS.  
Open `qgis/wildfire_mapping_project.qgz` if the project file is present.  
Run `scripts/pyqgis_style_layers.py` from the QGIS Python console to apply styling.

---

## Data sources

| Data | Source |
|------|--------|
| Active fire detections | [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov) |
| Administrative boundaries | [GADM v4.1](https://gadm.org) |
| Elevation (SRTM 30m) | [USGS EarthExplorer](https://earthexplorer.usgs.gov) |
| Land cover | [ESA WorldCover 2021](https://esa-worldcover.org) |

---

## Maps produced

| Map | Description |
|-----|-------------|
| `fire_scatter_preview.png` | Quick spatial scatter of fire detections |
| `fire_temporal_distribution.png` | Annual and monthly detection counts |
| `wildfire_points_map.png` | Styled QGIS export — graduated by FRP |
| `regional_risk_map.png` | Choropleth of fire density by province |

---

## Methodology

See [methodology.md](methodology.md) for the full technical writeup covering data sources, filtering logic, CRS handling, and risk classification approach.

---

## Stack

- **QGIS 3.x** — visual GIS, layer management, print layouts
- **PyQGIS** — scripted styling and map export
- **GeoPandas / Shapely** — spatial data processing in Python
- **Pandas / Matplotlib** — data cleaning and EDA
- **NASA FIRMS** — satellite fire detection (VIIRS S-NPP)
