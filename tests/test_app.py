import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from crm import app, db
from crm.routes import Client


def setup_app(tmp_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(tmp_path / "test.db")
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
    return app.test_client()


def test_create_and_list_client(tmp_path):
    client = setup_app(tmp_path)
    response = client.post('/clients', json={'name': 'Alice', 'email': 'alice@example.com'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Alice'

    response = client.get('/clients')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['email'] == 'alice@example.com'
