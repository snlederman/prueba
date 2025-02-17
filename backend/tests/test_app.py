import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_transactions_summary(client):
    response = client.get('/api/transactions/summary')
    assert response.status_code == 200
    data = response.get_json()
    assert "results" in data

def test_predict_rating(client):
    response = client.post('/api/predict-rating/', json={"var1": 1, "var2": 2})
    assert response.status_code == 200
    data = response.get_json()
    assert "predicted_rating" in data