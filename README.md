# House-Price-Prediction

Simple end-to-end house price prediction for King County (Seattle area) with:

- Training script (`run.py`) that saves a `joblib` pipeline
- Inference script (`inference.py`) for CSV inputs
- Shared feature engineering in `features.py` (adds `dist_to_center_m`)
- FastAPI app (`app.py`) with HTML forms/templates in `templates/`

## Setup

1. Create a virtual environment and install dependencies:

```
pip install -r requirements.txt
```

2. Ensure training data `kc_house_data.csv` is present in the project root.

## Train

```
python run.py
```

This will print MAE/RMSE, run spatial CV, and save `kc_price_model.joblib`.

## Inference (CSV)

Place your input as `kc_new_listings.csv` (same columns as dataset except `price`).

```
python inference.py
```

This writes `predictions_kc_new.csv`.

## Web App

Start the FastAPI server:

```
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000` for single prediction and `http://127.0.0.1:8000/upload` for batch upload.

## Notes

- Geographic distance uses UTM Zone 10N (EPSG:32610) for meters.
- Feature list is centralized in `features.py` to keep training, inference and app consistent.
