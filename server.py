from flask import Flask, request, send_file
import os
import time

app = Flask(__name__)

UPLOAD_DIR = "images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

API_KEY = "secret123"

@app.route("/upload", methods=["POST"])
def upload():
    if request.headers.get("X-API-Key") != API_KEY:
        return "Unauthorized", 401

    filename = f"{int(time.time())}.jpg"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as f:
        f.write(request.data)

    return "OK", 200


@app.route("/latest")
def latest():
    files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(".jpg")]
    if not files:
        return "No image yet", 404

    latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(UPLOAD_DIR, f)))
    return send_file(os.path.join(UPLOAD_DIR, latest_file), mimetype="image/jpeg")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
