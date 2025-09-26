# inference.py

from pathlib import Path
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from joblib import load

# 1) Load trained pipeline
model = load("kc_price_model.joblib")  # saved Pipeline (pre + model) [training step]

# 2) Load new inputs
new_df = pd.read_csv(Path("kc_new_listings.csv"))

# 3) Recreate distance feature (same as training)
gdf = gpd.GeoDataFrame(new_df.copy(),
                       geometry=gpd.points_from_xy(new_df["long"], new_df["lat"]),
                       crs="EPSG:4326")
gdf_m = gdf.to_crs(32610)
center = gpd.GeoSeries([Point(-122.3321, 47.6062)], crs="EPSG:4326").to_crs(32610).iloc[0]
gdf_m["dist_to_center_m"] = gdf_m.geometry.distance(center)
new_df = pd.DataFrame(gdf_m.drop(columns="geometry"))

# 4) Predict with same feature set used in training
num_cols = [
    "bedrooms","bathrooms","sqft_living","sqft_lot","floors","waterfront",
    "view","condition","grade","sqft_above","sqft_basement","yr_built",
    "yr_renovated","lat","long","sqft_living15","sqft_lot15","dist_to_center_m"
]
preds = model.predict(new_df[num_cols])

# 5) Save predictions
pd.DataFrame({"predicted_price": preds}).to_csv("predictions_kc_new.csv", index=False)
print("Saved predictions_kc_new.csv")
