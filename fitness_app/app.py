from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory "database"
members = [
    {"id": 1, "name": "John", "age": 28, "membership": "Gold", "workouts": []},
    {"id": 2, "name": "Sara", "age": 25, "membership": "Silver", "workouts": []},
    {"id": 3, "name": "Mike", "age": 30, "membership": "Platinum", "workouts": []},
]

workouts = [
    {"id": 1, "name": "Cardio"},
    {"id": 2, "name": "Strength Training"},
    {"id": 3, "name": "Yoga"},
]

plans = [
    {"id": 1, "name": "Silver", "price": 50},
    {"id": 2, "name": "Gold", "price": 80},
    {"id": 3, "name": "Platinum", "price": 120},
]

payments = [
    {"member_id": 1, "status": "Paid"},
    {"member_id": 2, "status": "Pending"},
    {"member_id": 3, "status": "Paid"},
]


@app.route("/")
def home():
    return "Welcome to ACEest Fitness & Gym API!"


# ---------------- Members ----------------
@app.route("/members", methods=["GET"])
def get_members():
    return jsonify(members)


@app.route("/members", methods=["POST"])
def add_member():
    data = request.get_json()
    new_id = max(m["id"] for m in members) + 1 if members else 1
    new_member = {
        "id": new_id,
        "name": data.get("name"),
        "age": data.get("age"),
        "membership": data.get("membership", "Silver"),
        "workouts": [],
    }
    members.append(new_member)
    return jsonify(new_member), 201


@app.route("/members/<int:member_id>", methods=["GET"])
def get_member(member_id):
    member = next((m for m in members if m["id"] == member_id), None)
    if member:
        return jsonify(member)
    return jsonify({"error": "Member not found"}), 404


# ---------------- Workouts ----------------
@app.route("/workouts", methods=["GET"])
def get_workouts():
    return jsonify(workouts)


@app.route("/members/<int:member_id>/workouts", methods=["POST"])
def assign_workout(member_id):
    data = request.get_json()
    workout_id = data.get("workout_id")
    member = next((m for m in members if m["id"] == member_id), None)
    workout = next((w for w in workouts if w["id"] == workout_id), None)

    if not member:
        return jsonify({"error": "Member not found"}), 404
    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    member["workouts"].append(workout)
    return jsonify(member)


# ---------------- Membership Plans ----------------
@app.route("/plans", methods=["GET"])
def get_plans():
    return jsonify(plans)


# ---------------- Payments ----------------
@app.route("/payments", methods=["GET"])
def get_payments():
    return jsonify(payments)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999)