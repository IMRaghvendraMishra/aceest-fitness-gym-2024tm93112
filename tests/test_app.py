from src.app import app

def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.data == b"Hello, ACEest Fitness!"
    assert response.status_code == 200

def test_members():
    client = app.test_client()
    response = client.get("/members")
    assert "John" in response.json["members"]