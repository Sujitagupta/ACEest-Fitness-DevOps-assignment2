import os
import pytest
from app.main import create_app

@pytest.fixture
def client():
    os.environ['APP_VERSION'] = 'v1.2.3-test'
    app = create_app()
    app.testing = True
    with app.test_client() as c:
        yield c

def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['app'] == 'ACEest Fitness & Gym'
    assert 'version' in data

def test_health(client):
    rv = client.get('/health')
    assert rv.status_code == 200
    assert rv.get_json()['status'] == 'ok'

def test_get_members(client):
    rv = client.get('/members')
    assert rv.status_code == 200
    data = rv.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_create_member(client):
    rv = client.post('/members', json={'name': 'Charlie', 'membership': 'Gold'})
    assert rv.status_code == 201
    data = rv.get_json()
    assert data['name'] == 'Charlie'

def test_book_class(client):
    rv = client.post('/classes/1/book')
    assert rv.status_code in (200, 400)
    if rv.status_code == 200:
        assert rv.get_json()['message'] == 'booked'
