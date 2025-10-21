from pathlib import Path
from typing import Optional

import pandas as pd
from fastapi import FastAPI, Request, UploadFile, File, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from joblib import load

from features import build_feature_frame, NUMERIC_FEATURE_COLUMNS


app = FastAPI(title="KC House Price Prediction")

templates = Jinja2Templates(directory="templates")

# Optional static dir if needed later
app.mount("/static", StaticFiles(directory="static"), name="static")


def _load_model():
    return load("kc_price_model.joblib")


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)


@app.get("/health", include_in_schema=False)
def health_check():
    """Health check endpoint for deployment platforms"""
    return {"status": "healthy", "message": "King County House Price Prediction API is running"}


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict", response_class=HTMLResponse)
async def predict_form(
    request: Request,
    bedrooms: float = Form(...),
    bathrooms: float = Form(...),
    sqft_living: float = Form(...),
    sqft_lot: float = Form(...),
    floors: float = Form(...),
    waterfront: float = Form(0),
    view: float = Form(0),
    condition: float = Form(3),
    grade: float = Form(7),
    sqft_above: float = Form(...),
    sqft_basement: float = Form(0),
    yr_built: float = Form(...),
    yr_renovated: float = Form(0),
    lat: float = Form(...),
    long: float = Form(...),
    sqft_living15: float = Form(...),
    sqft_lot15: float = Form(...),
):
    raw = pd.DataFrame([
        {
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "sqft_living": sqft_living,
            "sqft_lot": sqft_lot,
            "floors": floors,
            "waterfront": waterfront,
            "view": view,
            "condition": condition,
            "grade": grade,
            "sqft_above": sqft_above,
            "sqft_basement": sqft_basement,
            "yr_built": yr_built,
            "yr_renovated": yr_renovated,
            "lat": lat,
            "long": long,
            "sqft_living15": sqft_living15,
            "sqft_lot15": sqft_lot15,
        }
    ])

    X = build_feature_frame(raw)
    model = _load_model()
    pred = float(model.predict(X)[0])
    return templates.TemplateResponse(
        "result.html", {"request": request, "prediction": pred}
    )


@app.get("/upload", response_class=HTMLResponse)
def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/upload", response_class=HTMLResponse)
async def upload_predict(request: Request, file: UploadFile = File(...)):
    content = await file.read()
    df = pd.read_csv(pd.io.common.BytesIO(content))
    X = build_feature_frame(df)
    model = _load_model()
    preds = model.predict(X)
    out = pd.DataFrame({"predicted_price": preds})
    # Show first rows preview
    sample_html = out.head(20).to_html(classes="table table-striped", index=False)
    return templates.TemplateResponse(
        "batch_result.html",
        {"request": request, "rows": len(out), "preview_html": sample_html},
    )


