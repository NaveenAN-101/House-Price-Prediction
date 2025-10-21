from __future__ import annotations

from typing import List

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point


# Centralized configuration for geographic computations
WGS84_CRS = "EPSG:4326"
# UTM Zone 10N (meters) for Seattle region
METRIC_CRS = 32610
# Approximate downtown Seattle reference point
SEATTLE_CENTER_WGS84 = Point(-122.3321, 47.6062)


# Feature list used by the model
NUMERIC_FEATURE_COLUMNS: List[str] = [
    "bedrooms",
    "bathrooms",
    "sqft_living",
    "sqft_lot",
    "floors",
    "waterfront",
    "view",
    "condition",
    "grade",
    "sqft_above",
    "sqft_basement",
    "yr_built",
    "yr_renovated",
    "lat",
    "long",
    "sqft_living15",
    "sqft_lot15",
    "dist_to_center_m",
]


def add_distance_feature(frame: pd.DataFrame) -> pd.DataFrame:
    """Add `dist_to_center_m` computed from `lat`/`long` to a copy of the frame.

    The function expects columns `lat` and `long` in WGS84 degrees.
    Returns a new DataFrame with the added column.
    """
    required = {"lat", "long"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns for distance feature: {sorted(missing)}")

    gdf = gpd.GeoDataFrame(
        frame.copy(),
        geometry=gpd.points_from_xy(frame["long"], frame["lat"]),
        crs=WGS84_CRS,
    )
    gdf_metric = gdf.to_crs(METRIC_CRS)
    center_metric = gpd.GeoSeries([SEATTLE_CENTER_WGS84], crs=WGS84_CRS).to_crs(METRIC_CRS).iloc[0]
    gdf_metric["dist_to_center_m"] = gdf_metric.geometry.distance(center_metric)
    return pd.DataFrame(gdf_metric.drop(columns="geometry"))


def build_feature_frame(raw_frame: pd.DataFrame) -> pd.DataFrame:
    """Return the model-ready feature DataFrame.

    - Adds `dist_to_center_m` using geodesic projection
    - Selects and orders the feature columns expected by the model
    """
    enriched = add_distance_feature(raw_frame)
    # Ensure all columns exist; raise with a helpful message if any are missing
    missing = [c for c in NUMERIC_FEATURE_COLUMNS if c not in enriched.columns]
    if missing:
        raise ValueError(
            "Missing columns required by the model: " + ", ".join(missing)
        )
    return enriched[NUMERIC_FEATURE_COLUMNS].copy()


