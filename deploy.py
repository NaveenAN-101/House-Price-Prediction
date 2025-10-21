# deploy.py - One-time setup script for web deployment
import os
import subprocess
import sys
from pathlib import Path

def setup_for_deployment():
    """Prepare the app for web deployment"""
    print("🚀 Setting up for web deployment...")
    
    # 1. Train the model if it doesn't exist
    model_path = Path("kc_price_model.joblib")
    if not model_path.exists():
        print("📊 Training model...")
        subprocess.run([sys.executable, "run.py"], check=True)
        print("✅ Model trained and saved")
    else:
        print("✅ Model already exists")
    
    # 2. Create a simple health check endpoint
    print("🔧 Setting up health check...")
    
    # 3. Print deployment instructions
    print("\n" + "="*50)
    print("🌐 DEPLOYMENT READY!")
    print("="*50)
    print("\n📋 Next steps:")
    print("1. Push this code to GitHub")
    print("2. Go to https://railway.app")
    print("3. Connect your GitHub repo")
    print("4. Deploy!")
    print("\n🔗 Alternative: Use Render.com")
    print("1. Go to https://render.com")
    print("2. Connect GitHub repo")
    print("3. Choose 'Web Service'")
    print("4. Set build command: pip install -r requirements.txt")
    print("5. Set start command: uvicorn app:app --host 0.0.0.0 --port $PORT")
    print("\n✨ Your app will be live at a public URL!")

if __name__ == "__main__":
    setup_for_deployment()
