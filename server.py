"""
MailSmith.AI — Backend API Server
Proxies requests to OpenRouter API with secure key handling.
Stores user reviews in a local JSON file.
"""

import os
import json
import time
import logging
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import requests as http_requests

# ── Config ──────────────────────────────────────────────
load_dotenv()  # Only loads if .env exists (local dev)
logging.basicConfig(level=logging.INFO)

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app, resources={r"/api/*": {"origins": "*"}})

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
OPENROUTER_URL = 'https://openrouter.ai/api/v1/chat/completions'
MODEL = 'arcee-ai/trinity-large-preview:free'
REVIEWS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reviews.json')


def _load_reviews():
    if os.path.exists(REVIEWS_FILE):
        try:
            with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def _save_reviews(reviews):
    with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, indent=2, ensure_ascii=False)


# ── Static file serving ────────────────────────────────
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')


@app.route('/reviews')
def serve_reviews_page():
    return send_from_directory('.', 'reviews.html')


@app.route('/maintenance')
def serve_maintenance_page():
    return send_from_directory('.', 'maintenance.html')


# ── AI Proxy Endpoints ─────────────────────────────────
@app.route('/api/generate', methods=['POST'])
def api_generate():
    if not OPENROUTER_API_KEY:
        return jsonify({'error': 'API key not configured on server'}), 500

    data = request.get_json()
    if not data or 'messages' not in data:
        return jsonify({'error': 'Missing messages in request body'}), 400

    try:
        resp = http_requests.post(
            OPENROUTER_URL,
            headers={
                'Authorization': f'Bearer {OPENROUTER_API_KEY}',
                'Content-Type': 'application/json',
            },
            json={
                'model': MODEL,
                'messages': data['messages'],
                'reasoning': {'enabled': True},
            },
            timeout=60,
        )
        resp.raise_for_status()
        result = resp.json()
        logging.info(f'Generate API success: {resp.status_code}')
        return jsonify(result)
    except http_requests.exceptions.Timeout:
        logging.error('Generate API timed out')
        return jsonify({'error': 'AI service timed out. Please try again.'}), 504
    except http_requests.exceptions.RequestException as e:
        logging.error(f'Generate API error: {str(e)}')
        return jsonify({'error': f'AI service error: {str(e)}'}), 502


@app.route('/api/enhance', methods=['POST'])
def api_enhance():
    if not OPENROUTER_API_KEY:
        return jsonify({'error': 'API key not configured on server'}), 500

    data = request.get_json()
    if not data or 'messages' not in data:
        return jsonify({'error': 'Missing messages in request body'}), 400

    try:
        resp = http_requests.post(
            OPENROUTER_URL,
            headers={
                'Authorization': f'Bearer {OPENROUTER_API_KEY}',
                'Content-Type': 'application/json',
            },
            json={
                'model': MODEL,
                'messages': data['messages'],
                'reasoning': {'enabled': True},
            },
            timeout=60,
        )
        resp.raise_for_status()
        result = resp.json()
        logging.info(f'Enhance API success: {resp.status_code}')
        return jsonify(result)
    except http_requests.exceptions.Timeout:
        logging.error('Enhance API timed out')
        return jsonify({'error': 'AI service timed out. Please try again.'}), 504
    except http_requests.exceptions.RequestException as e:
        logging.error(f'Enhance API error: {str(e)}')
        return jsonify({'error': f'AI service error: {str(e)}'}), 502


# ── Reviews Endpoints ──────────────────────────────────
@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    reviews = _load_reviews()
    return jsonify(reviews)


@app.route('/api/reviews', methods=['POST'])
def post_review():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    review = {
        'id': int(time.time() * 1000),
        'name': (data.get('name') or 'Anonymous').strip(),
        'rating': max(1, min(5, int(data.get('rating', 5)))),
        'feedback': (data.get('feedback') or '').strip(),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

    reviews = _load_reviews()
    reviews.insert(0, review)
    _save_reviews(reviews)

    return jsonify({'success': True, 'review': review}), 201


# ── Health Check ───────────────────────────────────────
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'api_key_configured': bool(OPENROUTER_API_KEY),
        'model': MODEL,
    })


# ── Run ────────────────────────────────────────────────
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    is_production = os.environ.get('RENDER') or os.environ.get('RAILWAY_ENVIRONMENT')
    print(f'\n  ✉️  MailSmith.AI — Backend Server')
    print(f'  🔑 API Key: {"configured" if OPENROUTER_API_KEY else '⚠️  MISSING — set OPENROUTER_API_KEY in .env or environment'}')
    print(f'  🌐 http://localhost:{port}')
    print(f'  📋 Reviews viewer: http://localhost:{port}/reviews\n')
    app.run(host='0.0.0.0', port=port, debug=not is_production)
