# Dharma Platform - Live Anti-Nationalist Dashboard

Real-time YouTube search and analysis for anti-nationalist content detection.

## Features
- Live YouTube search for anti-nationalist content
- Real-time threat detection and analysis
- Interactive dashboard with clickable results
- Advanced sentiment analysis and keyword detection
- Threat level classification (Critical, High, Medium, Low)

## Deployment
This app is configured for Streamlit Cloud deployment with minimal dependencies.

### Main Files
- `streamlit_app.py` - Main entry point for Streamlit Cloud
- `streamlit_live_dashboard.py` - Core dashboard functionality
- `requirements.txt` - Streamlit Cloud compatible dependencies
- `.streamlit/secrets.toml` - API key configuration

### Usage
1. Search for specific terms or use auto-detect
2. Click on any video result to view on YouTube
3. Expand analysis details to see threat scoring
4. Filter results by threat level

## API Configuration
The YouTube API key is configured in Streamlit secrets for cloud deployment.

## Local Development
To run locally:
```bash
streamlit run streamlit_app.py
```

## Cloud Deployment
1. Push to GitHub repository
2. Go to https://share.streamlit.io/
3. Connect your GitHub repository
4. Set main file path to: streamlit_app.py
5. Deploy!