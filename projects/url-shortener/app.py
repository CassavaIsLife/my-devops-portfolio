import os
import secrets
import sqlite3
import string
from contextlib import contextmanager
from urllib.parse import urlparse

from flask import Flask, request, jsonify, render_template_string, redirect

app = Flask(__name__)
DB_FILE = 'urls.db'

ALPHABET = string.ascii_letters + string.digits
RESERVED_CODES = {'health', 'stats', 'shorten', 'static'}
MAX_URL_LENGTH = 2048


def get_db_path():
    return os.environ.get('DB_FILE', DB_FILE)


@contextmanager
def get_db():
    """Open a connection, commit on success, always close."""
    conn = sqlite3.connect(get_db_path())
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Initialize the SQLite database schema"""
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS urls
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         short_code TEXT UNIQUE NOT NULL,
                         long_url TEXT NOT NULL,
                         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                         clicks INTEGER DEFAULT 0)''')


def generate_short_code(length=6):
    """Generate a cryptographically random short code"""
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))


def normalize_url(raw):
    """Return a valid http(s) URL or None."""
    if not isinstance(raw, str):
        return None
    url = raw.strip()
    if not url or len(url) > MAX_URL_LENGTH:
        return None
    if '://' not in url:
        url = f'https://{url}'
    try:
        parsed = urlparse(url)
        _ = parsed.port  # raises ValueError on a non-numeric/out-of-range port
    except ValueError:
        return None
    if parsed.scheme not in ('http', 'https') or not parsed.hostname:
        return None
    return url


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
            <li><b>GET /stats/&lt;short_code&gt;</b> - Click statistics</li>
            <li><b>GET /health</b> - Health check</li>
        </ul>
    ''')


@app.route('/shorten', methods=['POST'])
def shorten_url():
    """Create a shortened URL"""
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or 'url' not in data:
        return jsonify({"error": "Missing 'url' field"}), 400

    long_url = normalize_url(data['url'])
    if long_url is None:
        return jsonify({"error": "Invalid URL"}), 400

    with get_db() as conn:
        # Rely on the UNIQUE constraint instead of check-then-insert (race-free)
        for _ in range(10):
            short_code = generate_short_code()
            if short_code in RESERVED_CODES:
                continue
            try:
                conn.execute("INSERT INTO urls (short_code, long_url) VALUES (?, ?)",
                             (short_code, long_url))
                break
            except sqlite3.IntegrityError:
                continue
        else:
            return jsonify({"error": "Could not generate a unique code"}), 500

    return jsonify({
        "short_code": short_code,
        "short_url": f"{request.host_url}{short_code}",
        "original_url": long_url
    }), 201


@app.route('/<short_code>')
def redirect_to_url(short_code):
    """Redirect to original URL"""
    with get_db() as conn:
        cur = conn.execute(
            "UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?", (short_code,))
        if cur.rowcount == 0:
            return jsonify({"error": "Short URL not found"}), 404
        row = conn.execute(
            "SELECT long_url FROM urls WHERE short_code = ?", (short_code,)).fetchone()
    return redirect(row[0], code=302)


@app.route('/stats/<short_code>')
def get_stats(short_code):
    """Get statistics for a short URL"""
    with get_db() as conn:
        row = conn.execute(
            "SELECT short_code, long_url, created_at, clicks FROM urls WHERE short_code = ?",
            (short_code,)).fetchone()

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
    """Health check endpoint that actually touches the database"""
    try:
        with get_db() as conn:
            conn.execute("SELECT 1 FROM urls LIMIT 1")
    except sqlite3.Error:
        return jsonify({"status": "unhealthy", "database": "error"}), 503
    return jsonify({"status": "healthy", "database": "connected"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)