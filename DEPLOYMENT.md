# Vercel Deployment Guide

## Prerequisites

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Make sure you have your YouTube API key ready

## Deployment Steps

### 1. Set Environment Variables
```bash
vercel env add YOUTUBE_API_KEY
# Enter your YouTube API key when prompted
```

### 2. Deploy to Vercel
```bash
vercel
```

### 3. Follow the prompts:
- Set up and deploy? → `Y`
- Which scope? → Select your account
- Link to existing project? → `N`
- Project name? → `vibecheckml` (or your preferred name)
- Directory? → `./` (current directory)

### 4. Your app will be deployed to:
- Production: `https://your-project-name.vercel.app`
- Preview: `https://your-project-name-git-branch-username.vercel.app`

## Environment Variables in Vercel Dashboard

1. Go to your Vercel dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add: `YOUTUBE_API_KEY` with your actual API key

## Troubleshooting

### Common Issues:

1. **Model files not found**: Make sure `sentiment_classifier.pkl` and `vectorizer.pkl` are in the root directory
2. **API key not working**: Check that the environment variable is set correctly in Vercel dashboard
3. **CORS issues**: The app is configured to handle CORS automatically

### Local Testing:
```bash
# Test locally before deploying
python3 app.py
# Visit http://localhost:5050
```

## File Structure for Deployment:
```
VibeCheckML/
├── app.py                 # Main Flask app
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
├── runtime.txt          # Python version
├── sentiment_classifier.pkl  # ML model
├── vectorizer.pkl       # Text vectorizer
├── public/
│   └── index.html       # Frontend
└── .env                 # Local environment (not deployed)
``` 