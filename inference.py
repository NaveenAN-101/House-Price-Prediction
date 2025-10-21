# inference.py

from pathlib import Path
import pandas as pd
from joblib import load

from features import build_feature_frame


def predict_csv(input_csv: Path = Path("kc_new_listings.csv"), output_csv: Path = Path("predictions_kc_new.csv")) -> None:
    model = load("kc_price_model.joblib")
    raw = pd.read_csv(input_csv)
    X = build_feature_frame(raw)
    preds = model.predict(X)
    pd.DataFrame({"predicted_price": preds}).to_csv(output_csv, index=False)
    print("Saved", str(output_csv))


if __name__ == "__main__":
    predict_csv()
