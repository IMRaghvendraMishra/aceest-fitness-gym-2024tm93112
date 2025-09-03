from src.app import app

def test_home():
    client = app.test_client()
    response = client.get("/")
    assert b"Welcome to ACEest Fitness & Gym API!" in response.data
    assert response.status_code == 200

def test_members():
    client = app.test_client()
    response = client.get("/members")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    members = response.json
    assert isinstance(members, list)
    assert len(members) > 0
    assert any(m.get("name") == "John" for m in members)

def test_add_member():
    client = app.test_client()
    new_member = {"name": "Alice", "age": 28, "email": "alice@example.com"}
    response = client.post("/members", json=new_member)
    assert response.status_code == 201
    assert response.json["name"] == "Alice"
    assert response.json["age"] == 28

def test_get_member():
    client = app.test_client()
    # First, add a member to ensure it exists
    new_member = {"name": "Bob", "age": 30, "email": "bob@example.com"}
    add_resp = client.post("/members", json=new_member)
    member_id = add_resp.json["id"]
    response = client.get(f"/members/{member_id}")
    assert response.status_code == 200
    assert response.json["name"] == "Bob"

def test_get_workouts():
    client = app.test_client()
    response = client.get("/workouts")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    # Check that at least one expected workout is present
    assert any(w.get("name") == "Cardio" for w in response.json)

def test_assign_workout():
    client = app.test_client()
    # Add a member and a workout first
    member = client.post("/members", json={"name": "Carl", "age": 25, "email": "carl@example.com"}).json
    member_id = member["id"]
    workout_data = {"name": "Cardio", "description": "Cardio session"}
    workout_resp = client.post("/workouts", json=workout_data)
    if workout_resp.status_code == 201:
        workout_id = workout_resp.json["workout"]["id"]
    else:
        # fallback: use first workout from list
        workout_id = client.get("/workouts").json[0]["id"]
    assign_resp = client.post(f"/members/{member_id}/workouts", json={"workout_id": workout_id})
    assert assign_resp.status_code == 200
    # The API now returns the updated member object; check that the assigned workout is in the member's workouts list
    assert "workouts" in assign_resp.json
    assert any(w["id"] == workout_id for w in assign_resp.json["workouts"])

def test_get_plans():
    client = app.test_client()
    response = client.get("/plans")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    # Check that the list contains expected plan names
    plan_names = [plan.get("name") for plan in response.json]
    assert "Silver" in plan_names
    assert "Gold" in plan_names
    assert "Platinum" in plan_names

def test_get_payments():
    client = app.test_client()
    response = client.get("/payments")
    assert response.status_code == 200
    assert isinstance(response.json, list)
    # Check that each payment entry has expected keys
    for payment in response.json:
        assert "member_id" in payment
        assert "status" in payment