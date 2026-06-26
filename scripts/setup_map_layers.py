from qgis.core import *
from qgis.PyQt.QtGui import QColor, QFont
from qgis.PyQt.QtCore import QRectF
import os

BASE = "/Users/zaynebcherif/wildfire-risk-qgis/data/processed"
project = QgsProject.instance()

# ── 1. Remove existing layers ──────────────────────────────────────────────
project.clear()

# ── 2. Load layers ─────────────────────────────────────────────────────────
neighbors_lyr = QgsVectorLayer(f"{BASE}/neighbors.geojson", "Neighboring Countries", "ogr")
regions_lyr   = QgsVectorLayer(f"{BASE}/morocco_regions.geojson", "Fire Density by Region", "ogr")
morocco_lyr   = QgsVectorLayer(f"{BASE}/morocco_boundary.geojson", "Morocco", "ogr")
fires_lyr     = QgsVectorLayer(f"{BASE}/morocco_fires.gpkg|layername=fire_points", "Fire Detections", "ogr")

for lyr in [neighbors_lyr, regions_lyr, morocco_lyr, fires_lyr]:
    assert lyr.isValid(), f"Failed to load: {lyr.name()}"
    project.addMapLayer(lyr)

# ── 3. Style neighbors (flat grey) ────────────────────────────────────────
sym = QgsFillSymbol.createSimple({'color': '#d6d6d6', 'outline_color': '#aaaaaa', 'outline_width': '0.4'})
neighbors_lyr.setRenderer(QgsSingleSymbolRenderer(sym))

# ── 4. Choropleth — fire density by region ────────────────────────────────
graduated_ranges = [
    (0,      0.001,  '#fff5f0', 'Very Low'),
    (0.001,  0.002,  '#fdbdac', 'Low'),
    (0.002,  0.005,  '#fc6955', 'Moderate'),
    (0.005,  0.015,  '#d91c23', 'High'),
    (0.015,  1.0,    '#67000d', 'Very High'),
]
rranges = []
for low, high, color, label in graduated_ranges:
    sym = QgsFillSymbol.createSimple({'color': color, 'outline_color': '#888888', 'outline_width': '0.3'})
    rranges.append(QgsRendererRange(low, high, sym, label))
regions_lyr.setRenderer(QgsGraduatedSymbolRenderer('fire_density', rranges))

# ── 5. Morocco outline on top of choropleth ───────────────────────────────
sym = QgsFillSymbol.createSimple({'color': '0,0,0,0', 'outline_color': '#222222', 'outline_width': '0.8'})
morocco_lyr.setRenderer(QgsSingleSymbolRenderer(sym))

# ── 6. Fire points — graduated by FRP ────────────────────────────────────
point_ranges = [
    (0,   2,   '#fcbea5', 'Low (0–2 MW)',      '2.5'),
    (2,   5,   '#fb6a4a', 'Moderate (2–5 MW)', '3.5'),
    (5,   15,  '#cb181d', 'High (5–15 MW)',     '4.5'),
    (15,  200, '#67000d', 'Extreme (>15 MW)',   '6'),
]
pranges = []
for low, high, color, label, size in point_ranges:
    sym = QgsMarkerSymbol.createSimple({'color': color, 'size': size, 'outline_style': 'no'})
    pranges.append(QgsRendererRange(low, high, sym, label))
fires_lyr.setRenderer(QgsGraduatedSymbolRenderer('frp', pranges))

# ── 7. Layer order: neighbors → regions → morocco outline → fires ─────────
root = project.layerTreeRoot()
order = [fires_lyr, morocco_lyr, regions_lyr, neighbors_lyr]
root.setHasCustomLayerOrder(True)
root.setCustomLayerOrder(order)

# ── 8. Refresh canvas ─────────────────────────────────────────────────────
iface.mapCanvas().refresh()
iface.zoomToActiveLayer()

print("Map styled. Now build the print layout:")
print("  Project → New Print Layout → name it 'Wildfire Map'")
print("  Add: Map, Title, Legend, Scale Bar, North Arrow")
