# run.py

from pathlib import Path
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# 1) Load data (robust path handling)
csv_path = Path("kc_house_data.csv")
df = pd.read_csv(csv_path)

# 2) Build GeoDataFrame in WGS84 (lon/lat)
gdf = gpd.GeoDataFrame(
    df.copy(),
    geometry=gpd.points_from_xy(df["long"], df["lat"]),
    crs="EPSG:4326"
)

# 3) Reproject to a metric CRS (UTM Zone 10N for Seattle area)
gdf_m = gdf.to_crs(32610)

# 4) Distance to downtown Seattle (approx point), in meters
seattle_center = gpd.GeoSeries([Point(-122.3321, 47.6062)], crs="EPSG:4326").to_crs(32610).iloc[0]
gdf_m["dist_to_center_m"] = gdf_m.geometry.distance(seattle_center)

# 5) Back to a flat DataFrame for ML
df = pd.DataFrame(gdf_m.drop(columns="geometry"))

# 6) Define features/target
target = "price"
num_cols = [
    "bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors", "waterfront",
    "view", "condition", "grade", "sqft_above", "sqft_basement", "yr_built",
    "yr_renovated", "lat", "long", "sqft_living15", "sqft_lot15", "dist_to_center_m"
]
X = df[num_cols].copy()
y = df[target].copy()

# 7) Preprocessing + model pipeline
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

pre = ColumnTransformer(
    transformers=[("num", StandardScaler(), num_cols)],
    remainder="drop"
)

model = Pipeline(
    steps=[
        ("pre", pre),
        ("xgb", XGBRegressor(
            n_estimators=600,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            tree_method="hist"
        ))
    ]
)

# 8) Train/test split
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

# 9) Fit and evaluate with MAE + RMSE (version-safe)
from sklearn.metrics import mean_absolute_error

# Prefer new RMSE API when available; otherwise sqrt(MSE) without 'squared' kwarg
try:
    from sklearn.metrics import root_mean_squared_error
    USE_NEW_RMSE = True
except ImportError:
    from sklearn.metrics import mean_squared_error
    import numpy as np
    USE_NEW_RMSE = False

model.fit(X_tr, y_tr)
preds = model.predict(X_te)

mae = mean_absolute_error(y_te, preds)
if USE_NEW_RMSE:
    from sklearn.metrics import root_mean_squared_error
    rmse = root_mean_squared_error(y_te, preds)
else:
    from sklearn.metrics import mean_squared_error
    import numpy as np
    rmse = np.sqrt(mean_squared_error(y_te, preds))

print(f"MAE: {mae:.3f} | RMSE: {rmse:.3f}")