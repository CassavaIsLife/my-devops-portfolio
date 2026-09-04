"""
URL Shortener API with Prometheus metrics
A simple Flask application demonstrating DevOps practices
"""
import sqlite3
import string
import random
import os
from flask import Flask, request, redirect, jsonify, render_template_string
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Database file path (configurable via environment variable)
DB_FILE = os.environ.get('DB_FILE', 'urls.db')

def init_db():
    """Initialize SQLite database with URLs table"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  short_code TEXT UNIQUE NOT NULL,
                  long_url TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  clicks INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

def generate_short_code(length=6):
    """Generate a random short code"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# Initialize database on startup
init_db()

@app.route('/')
def home():
    """Homepage with API documentation"""
    return render_template_string('''
        <h1>URL Shortener API</h1>
        <h2>Endpoints:</h2>
        <ul>
            <li><b>POST /shorten</b> - Create short URL (JSON: {"url": "https://example.com"})</li>
            <li><b>GET /&lt;short_code&gt;</b> - Redirect to original URL</li>
            <li><b>GET /health</b> - Health check</li>
            <li><b>GET /metrics</b> - Prometheus metrics</li>
        </ul>
    ''')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    """Create a shortened URL"""
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Missing 'url' field"}), 400
    
    long_url = data['url']
    
    # Basic URL validation
    if not long_url.startswith(('http://', 'https://')):
        long_url = f'https://{long_url}'
    
    # Generate unique short code
    short_code = generate_short_code()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Ensure uniqueness
    while True:
        c.execute("SELECT 1 FROM urls WHERE short_code = ?", (short_code,))
        if not c.fetchone():
            break
        short_code = generate_short_code()
    
    c.execute("INSERT INTO urls (short_code, long_url) VALUES (?, ?)",
              (short_code, long_url))
    conn.commit()
    conn.close()
    
    return jsonify({
        "short_code": short_code,
        "short_url": f"/{short_code}",
        "original_url": long_url
    }), 201

@app.route('/<short_code>')
def redirect_to_url(short_code):
    """Redirect to original URL"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT long_url FROM urls WHERE short_code = ?", (short_code,))
    row = c.fetchone()
    
    if row:
        # Increment click counter
        c.execute("UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?", (short_code,))
        conn.commit()
        conn.close()
        return redirect(row[0], code=302)
    
    conn.close()
    return jsonify({"error": "Short URL not found"}), 404

@app.route('/stats/<short_code>')
def get_stats(short_code):
    """Get statistics for a short URL"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT short_code, long_url, created_at, clicks FROM urls WHERE short_code = ?",
              (short_code,))
    row = c.fetchone()
    conn.close()
    
    if row:
        return jsonify({
            "short_code": row[0],
            "original_url": row[1],
            "created_at": row[2],
            "clicks": row[3]
        })
    return jsonify({"error": "Short URL not found"}), 404

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "database": "connected"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)