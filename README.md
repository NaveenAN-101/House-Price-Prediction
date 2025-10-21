# 🏠 King County House Price Prediction

A complete machine learning web application for predicting house prices in the Seattle area using XGBoost regression with spatial features.

## 🌐 **LIVE DEMO**

**🚀 [Try the live app here!](https://house-price-prediction-cbgk.onrender.com/)**

- **Single Prediction**: Beautiful form interface
- **Batch Upload**: CSV file processing
- **Mobile Responsive**: Works on all devices

## ✨ Features

- **🎯 Accurate Predictions**: XGBoost model with spatial cross-validation
- **🌐 Beautiful Web Interface**: Modern, responsive UI with Bootstrap
- **📊 Single & Batch Prediction**: Individual forms and CSV upload
- **🗺️ Geographic Features**: Distance to downtown Seattle
- **📱 Mobile Friendly**: Works on all devices
- **☁️ Easy Deployment**: Ready for Railway, Render, or Heroku

## 🚀 Quick Start

### Option 1: Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Train the model
python run.py

# Start web server
uvicorn app:app --reload
```

### Option 2: One-Command Setup

```bash
python deploy.py
```

Then open http://127.0.0.1:8000

## 🌐 Web Deployment

### ✅ **Successfully Deployed on Render!**

- **Live URL**: https://house-price-prediction-cbgk.onrender.com/
- **Status**: ✅ Active and running
- **Platform**: Render.com (Free tier)

### Alternative Deployment Options

#### Railway

1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. Connect GitHub repo
4. Deploy automatically!

#### Heroku

1. Install Heroku CLI
2. `heroku create your-app-name`
3. `git push heroku main`

## 📁 Project Structure

```
House-Price-Prediction/
├── app.py                 # FastAPI web application
├── run.py                 # Model training script
├── inference.py           # Batch prediction script
├── features.py            # Feature engineering module
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   ├── index.html        # Main prediction form
│   ├── result.html       # Single prediction result
│   ├── upload.html       # Batch upload page
│   └── batch_result.html # Batch results
├── static/               # Static assets
├── Procfile             # Heroku/Railway config
├── railway.json         # Railway configuration
└── kc_house_data.csv    # Training data
```

## 🎯 Usage

### 🌐 Live Web Interface

- **Single Prediction**: https://house-price-prediction-cbgk.onrender.com/
- **Batch Upload**: https://house-price-prediction-cbgk.onrender.com/upload
- **API Health**: https://house-price-prediction-cbgk.onrender.com/health

### 💻 Local Development

- **Single Prediction**: http://127.0.0.1:8000
- **Batch Upload**: http://127.0.0.1:8000/upload
- **API Health**: http://127.0.0.1:8000/health

### Command Line

```bash
# Train model
python run.py

# Batch prediction
python inference.py
```

## 🔧 Model Details

- **Algorithm**: XGBoost Regressor
- **Features**: 18 property characteristics + distance to downtown
- **Validation**: Spatial cross-validation with BlockKFold
- **Performance**: ~$66K MAE, ~$126K RMSE
- **Geographic**: UTM Zone 10N (EPSG:32610) for accurate distances

## 📊 Required CSV Columns

For batch prediction, your CSV should contain:

- `bedrooms`, `bathrooms`, `sqft_living`, `sqft_lot`
- `floors`, `waterfront`, `view`, `condition`, `grade`
- `sqft_above`, `sqft_basement`, `yr_built`, `yr_renovated`
- `lat`, `long`, `sqft_living15`, `sqft_lot15`

## 🛠️ Development

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Tests

```bash
python -m pytest tests/
```

### Code Structure

- `features.py`: Centralized feature engineering
- `app.py`: FastAPI routes and web interface
- `run.py`: Model training with spatial CV
- `inference.py`: Batch prediction utilities

## 📈 Performance

- **Training Time**: ~2-3 minutes
- **Prediction Time**: <100ms per property
- **Memory Usage**: ~500MB for model
- **Accuracy**: Spatial CV RMSE ~$124K

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- King County Assessor's Office for the dataset
- XGBoost team for the ML framework
- FastAPI for the web framework
- Bootstrap for the UI components
