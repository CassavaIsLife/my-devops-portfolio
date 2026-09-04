"""Unit tests for URL Shortener API"""
import pytest
import os
import sqlite3
from app import app, init_db, DB_FILE

@pytest.fixture
def client():
    """Create test client with temporary database"""
    # Use a separate test database
    os.environ['DB_FILE'] = 'test_urls.db'
    init_db()
    
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    
    # Cleanup
    if os.path.exists('test_urls.db'):
        os.remove('test_urls.db')

def test_health(client):
    """Test health check endpoint"""
    rv = client.get('/health')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['status'] == 'healthy'

def test_homepage(client):
    """Test homepage loads"""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'URL Shortener' in rv.data

def test_shorten_url(client):
    """Test URL shortening"""
    rv = client.post('/shorten', json={'url': 'https://example.com'})
    assert rv.status_code == 201
    data = rv.get_json()
    assert 'short_code' in data
    assert data['original_url'] == 'https://example.com'

def test_shorten_url_missing_field(client):
    """Test shortening with missing URL"""
    rv = client.post('/shorten', json={})
    assert rv.status_code == 400

def test_redirect(client):
    """Test URL redirection"""
    # First shorten a URL
    rv = client.post('/shorten', json={'url': 'https://google.com'})
    short_code = rv.get_json()['short_code']
    
    # Then try to redirect
    rv = client.get(f'/{short_code}')
    assert rv.status_code == 302
    assert rv.headers['Location'] == 'https://google.com'

def test_redirect_not_found(client):
    """Test redirect for non-existent URL"""
    rv = client.get('/nonexistent')
    assert rv.status_code == 404

def test_stats(client):
    """Test statistics endpoint"""
    # Shorten a URL
    rv = client.post('/shorten', json={'url': 'https://example.com'})
    short_code = rv.get_json()['short_code']
    
    # Get stats
    rv = client.get(f'/stats/{short_code}')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['clicks'] == 0