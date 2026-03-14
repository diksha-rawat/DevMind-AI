# Simple Flask web app
# This is the app that our pipeline will build and deploy
# It simulates a real application being reviewed by our AI agent

from flask import Flask, jsonify
import os

app = Flask(__name__)

# Home route - returns basic app info
@app.route("/")
def home():
    return jsonify({
        "message": "DevMind-AI is running!",
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "env": os.getenv("ENV", "development"),
    })

# Health check route - used by Kubernetes to check if app is alive
@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
