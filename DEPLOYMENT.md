# Deployment Guide

## Local Testing
```bash
pip install -r requirements.txt
uvicorn app:app --reload
```
Access: http://localhost:8000/pnr/2510323163

## Deployment Options

### 1. Render (Free, Easiest)
- Push code to GitHub
- Go to render.com
- Create new Web Service
- Connect your repo
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
- Add buildpack for Chrome in render.yaml

### 2. Railway (Free tier)
- Push to GitHub
- Go to railway.app
- Deploy from GitHub repo
- Auto-detects Python and runs

### 3. AWS EC2
```bash
# SSH into EC2
sudo apt update
sudo apt install python3-pip chromium-browser chromium-chromedriver
git clone <your-repo>
cd api
pip3 install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

### 4. Docker (Any platform)
```bash
docker build -t pnr-api .
docker run -p 8000:8000 pnr-api
```

### 5. Heroku
- Requires Heroku account
- Add Chrome buildpack
- Deploy via Git

## API Usage
GET /pnr/{pnr_number}

Example: https://your-domain.com/pnr/2510323163

Response:
```json
{
  "pnr": "2510323163",
  "train_name": "Train Name",
  "train_number": "12345",
  "status": "CNF",
  "station": "NDLS"
}
```
