import os
import tempfile

# Point the app at a throwaway DB *before* importing it
_TMP = tempfile.mkdtemp()
os.environ['DB_FILE'] = os.path.join(_TMP, 'import_time.db')

import pytest
import app as app_module


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('DB_FILE', str(tmp_path / 'test.db'))
    app_module.init_db()
    app_module.app.config['TESTING'] = True
    with app_module.app.test_client() as c:
        yield c


def create(client, url='https://example.com'):
    return client.post('/shorten', json={'url': url})


def test_home(client):
    assert client.get('/').status_code == 200


def test_health(client):
    r = client.get('/health')
    assert r.status_code == 200
    assert r.get_json()['status'] == 'healthy'


def test_shorten_success(client):
    r = create(client)
    assert r.status_code == 201
    data = r.get_json()
    assert len(data['short_code']) == 6
    assert data['short_url'].endswith('/' + data['short_code'])
    assert data['original_url'] == 'https://example.com'


def test_shorten_adds_scheme(client):
    assert create(client, 'example.com').get_json()['original_url'] == 'https://example.com'


@pytest.mark.parametrize('bad', ['', '   ', 'javascript:alert(1)', 'ftp://x.com',
                                 'https://', 123, None, ['a']])
def test_shorten_invalid_url(client, bad):
    assert create(client, bad).status_code == 400


def test_shorten_missing_field_and_bad_body(client):
    assert client.post('/shorten', json={}).status_code == 400
    assert client.post('/shorten', data='nope').status_code == 400   # non-JSON
    assert client.post('/shorten', json=[1, 2]).status_code == 400   # JSON non-object


def test_redirect_and_click_count(client):
    code = create(client).get_json()['short_code']
    r = client.get(f'/{code}')
    assert r.status_code == 302
    assert r.headers['Location'] == 'https://example.com'
    assert client.get(f'/stats/{code}').get_json()['clicks'] == 1


def test_redirect_not_found(client):
    assert client.get('/nope123').status_code == 404


def test_stats_initial_clicks_zero(client):
    code = create(client).get_json()['short_code']
    r = client.get(f'/stats/{code}')
    assert r.status_code == 200
    data = r.get_json()
    assert data['short_code'] == code
    assert data['original_url'] == 'https://example.com'
    assert data['clicks'] == 0          # <- your original assertion


def test_stats_not_found(client):
    assert client.get('/stats/missing').status_code == 404


def test_codes_are_unique(client):
    codes = {create(client).get_json()['short_code'] for _ in range(50)}
    assert len(codes) == 50


def test_collision_retry(client, monkeypatch):
    first = create(client).get_json()['short_code']
    seq = iter([first, first, 'AAAAAA'])
    monkeypatch.setattr(app_module, 'generate_short_code', lambda: next(seq))
    assert create(client, 'https://other.com').get_json()['short_code'] == 'AAAAAA'


def test_health_reports_db_failure(client, monkeypatch):
    monkeypatch.setenv('DB_FILE', '/nonexistent_dir/x.db')
    assert client.get('/health').status_code == 503