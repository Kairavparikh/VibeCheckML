import os
import pickle
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import re
from collections import Counter
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

with open('sentiment_classifier.pkl', 'rb') as f:
    model = pickle.load(f)
with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

def extract_video_id(url):
    match = re.search(r'(?:v=|youtu\.be/|embed/|shorts/)([\w-]{11})', url)
    return match.group(1) if match else None

def fetch_comments(video_id, api_key):
    url = 'https://www.googleapis.com/youtube/v3/commentThreads'
    params = {
        'part': 'snippet',
        'videoId': video_id,
        'key': api_key,
        'maxResults': 100,
        'textFormat': 'plainText'
    }

    comments = []
    nextPageToken = None

    while True:
        if nextPageToken:
            params['pageToken'] = nextPageToken

        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code != 200:
            raise Exception(f"API Error: {data.get('error', {}).get('message')}")

        for item in data.get('items', []):
            text = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(text)

        nextPageToken = data.get('nextPageToken')
        if not nextPageToken:
            break

    return comments

def fetch_video_title(video_id, api_key):
    url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {
        'part': 'snippet',
        'id': video_id,
        'key': api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    if response.status_code != 200 or not data.get('items'):
        return None
    return data['items'][0]['snippet']['title']

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'VibeCheckML API is running'})

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    video_id = extract_video_id(data['url'])
    if not video_id:
        return jsonify({'error': 'Invalid URL'}), 400
    try:
        comments = fetch_comments(video_id, YOUTUBE_API_KEY)
        title = fetch_video_title(video_id, YOUTUBE_API_KEY)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    if not comments:
        return jsonify({'error': 'No comments found'}), 404
    X = vectorizer.transform(comments)
    preds = model.predict(X)
    counts = Counter(preds)
    total = len(preds)
    sentiments = ['POSITIVE', 'NEGATIVE']
    breakdown = {sent: round(100*counts.get(sent,0)/total,2) for sent in sentiments}
    examples = {sent: [c for c,p in zip(comments, preds) if p==sent][2:5] for sent in sentiments}
    return jsonify({'breakdown': breakdown, 'examples': examples, 'all_comments': comments, 'title': title})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5050)))
