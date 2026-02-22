# Deploy to Render - Step by Step

## Prerequisites
- GitHub account
- Render account (free at render.com)

## Steps:

### 1. Push to GitHub
```bash
cd "c:\Users\Asus\OneDrive\Desktop\New folder\api"
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. Deploy on Render
1. Go to https://render.com
2. Sign up/Login with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - Name: pnr-api
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
6. Click "Create Web Service"

### 3. Wait for Deployment
- First deploy takes 5-10 minutes
- Render will install Chrome automatically
- You'll get a URL like: https://pnr-api.onrender.com

### 4. Test Your API
```
https://your-app.onrender.com/pnr/2510323163
```

## Important Notes:
- Free tier sleeps after 15 min of inactivity
- First request after sleep takes ~30 seconds
- Upgrade to paid ($7/month) for always-on service

## Troubleshooting:
If deployment fails, check Render logs and ensure:
- All files are committed to GitHub
- requirements.txt is present
- Python version is 3.11
