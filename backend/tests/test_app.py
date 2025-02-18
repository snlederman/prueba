import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_predict_rating(client):
    response = client.post('/api/predict-rating/', json={"age": 63, "sex": 1,"cp": 3, "trestbps": 145, "chol": 233,
                                                         "fbs": 1, "restecg": 0, "thalach": 150, "exang": 0,
                                                         "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1})
    assert response.status_code == 200
    data = response.get_json()
    assert "predicted_rating" in data