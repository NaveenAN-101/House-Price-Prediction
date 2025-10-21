# run.py

from pathlib import Path
from typing import Tuple

import numpy as pd_alias  # alias only to keep imports stable before refactor users; not used directly
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor
import numpy as np
import verde as vd
from joblib import dump

from features import build_feature_frame, NUMERIC_FEATURE_COLUMNS


def build_model() -> Pipeline:
    pre = ColumnTransformer(
        transformers=[("num", StandardScaler(), NUMERIC_FEATURE_COLUMNS)],
        remainder="drop",
    )
    model = Pipeline(
        steps=[
            ("pre", pre),
            (
                "xgb",
                XGBRegressor(
                    n_estimators=600,
                    learning_rate=0.05,
                    max_depth=6,
                    subsample=0.8,
                    colsample_bytree=0.8,
                    random_state=42,
                    tree_method="hist",
                ),
            ),
        ]
    )
    return model


def train(csv_path: Path = Path("kc_house_data.csv")) -> Tuple[Pipeline, float, float]:
    df_raw = pd.read_csv(csv_path)
    X = build_feature_frame(df_raw)
    y = df_raw["price"].copy()

    model = build_model()

    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_tr, y_tr)
    preds = model.predict(X_te)

    try:
        from sklearn.metrics import root_mean_squared_error

        rmse = root_mean_squared_error(y_te, preds)
    except Exception:
        from sklearn.metrics import mean_squared_error

        rmse = np.sqrt(mean_squared_error(y_te, preds))
    mae = mean_absolute_error(y_te, preds)

    # Spatial CV across lon/lat degrees (BlockKFold)
    coords = np.c_[df_raw["long"].values, df_raw["lat"].values]
    cv = vd.BlockKFold(spacing=0.2, n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(
        model, X, y, cv=cv.split(coords), scoring="neg_root_mean_squared_error"
    )
    print("Spatial-CV RMSE:", -scores.mean(), "+/-", scores.std())

    dump(model, "kc_price_model.joblib")
    print("Saved kc_price_model.joblib")

    return model, mae, rmse


if __name__ == "__main__":
    _, mae, rmse = train()
    print(f"MAE: {mae:.3f} | RMSE: {rmse:.3f}")

