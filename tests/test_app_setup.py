from src.app_setup import app

def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.data == b"Hello, ACEest Fitness!"
    assert response.status_code == 200