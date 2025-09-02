from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, ACEest Fitness!"

@app.route("/members")
def members():
    return {"members": ["John", "Sara", "Mike"]}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999)