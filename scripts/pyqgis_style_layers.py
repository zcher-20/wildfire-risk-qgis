"""
PyQGIS script — run from the QGIS Python console or via qgis --code.

Loads the fire points GeoPackage, applies a graduated color ramp by FRP
(Fire Radiative Power), and exports a PNG map layout.

Usage inside QGIS Python console:
    exec(open("scripts/pyqgis_style_layers.py").read())
"""

from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsGraduatedSymbolRenderer,
    QgsRendererRange,
    QgsSymbol,
    QgsLayoutExporter,
    QgsPrintLayout,
    QgsReadWriteContext,
)
from qgis.PyQt.QtGui import QColor
from PyQt5.QtXml import QDomDocument
import os

GPKG_PATH = os.path.abspath("data/processed/morocco_fires.gpkg")
LAYER_NAME = "fire_points"
EXPORT_PATH = os.path.abspath("maps/wildfire_points_map.png")

FRP_RANGES = [
    (0,   50,  "#fee5d9", "Low (0–50 MW)"),
    (50,  150, "#fc9272", "Medium (50–150 MW)"),
    (150, 300, "#fb6a4a", "High (150–300 MW)"),
    (300, 1e6, "#99000d", "Extreme (>300 MW)"),
]


def load_layer(path: str, layer_name: str) -> QgsVectorLayer:
    uri = f"{path}|layername={layer_name}"
    layer = QgsVectorLayer(uri, "Morocco Wildfire Detections", "ogr")
    if not layer.isValid():
        raise RuntimeError(f"Could not load layer from {uri}")
    QgsProject.instance().addMapLayer(layer)
    return layer


def apply_graduated_renderer(layer: QgsVectorLayer):
    ranges = []
    for low, high, hex_color, label in FRP_RANGES:
        symbol = QgsSymbol.defaultSymbol(layer.geometryType())
        symbol.setColor(QColor(hex_color))
        symbol.setSize(2.5)
        ranges.append(QgsRendererRange(low, high, symbol, label))

    renderer = QgsGraduatedSymbolRenderer("frp", ranges)
    layer.setRenderer(renderer)
    layer.triggerRepaint()


def export_map(export_path: str, dpi: int = 300):
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    iface.mapCanvas().saveAsImage(export_path, None, "PNG", dpi, dpi)
    print(f"Map exported → {export_path}")


layer = load_layer(GPKG_PATH, LAYER_NAME)
apply_graduated_renderer(layer)
iface.mapCanvas().refresh()
export_map(EXPORT_PATH)
