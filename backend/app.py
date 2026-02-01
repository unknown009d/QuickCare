from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from flask import abort
import os

from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from utils.hemoglobin_estimator import (
    save_uploaded_image,
    detect_eye_region,
    crop_conjunctiva,
    calculate_hemoglobin
)

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template("index.html")
    #abort(403)


@app.route('/upload', methods=['POST'])
def upload():
    image = request.files['image']
    user_id = request.form.get('user-id')

    save_uploaded_image(image, user_id)
    return jsonify({"message": "Image uploaded successfully"})


@app.route('/detect', methods=['POST'])
def detect():
    user_id = request.json.get('user-id')
    success = detect_eye_region(user_id)
    if not success:
        return jsonify({"error": "No eye detected"}), 400
    return jsonify({"message": "Eye detected"})


@app.route('/crop', methods=['POST'])
def crop():
    user_id = request.json.get('user-id')
    crop_conjunctiva(user_id)
    return jsonify({"message": "Conjunctiva cropped"})


@app.route('/calculate', methods=['POST'])
def calculate():
    user_id = request.json.get('user-id')
    hgb = calculate_hemoglobin(user_id)
    print(hgb)
    return jsonify({"message": "Hemoglobin estimated", "hemo": hgb})


@app.route('/get_images', methods=['POST'])
def get_images():
    user_id = request.json.get('user-id')
    user_dir = os.path.join(app.config['UPLOAD_FOLDER'], user_id)

    if not os.path.exists(user_dir):
        return jsonify({"error": "No images found for this user"}), 404

    files = [f for f in os.listdir(user_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    image_urls = [f"/user_image/{user_id}/{f}" for f in files]

    return jsonify({"images": image_urls})


@app.route('/user_image/<user_id>/<filename>')
def user_image(user_id, filename):
    user_dir = os.path.join(app.config['UPLOAD_FOLDER'], user_id)
    return send_from_directory(user_dir, filename)

@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200

if __name__ == '__main__':
    # Ensure base upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
