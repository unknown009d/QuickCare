from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from utils.hemoglobin_estimator import estimate_hemoglobin

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files['image']

    if image.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    if not allowed_file(image.filename):
        return jsonify({"error": "Unsupported file format"}), 400

    # Get user_id from frontend
    user_id = request.form.get('user-id')
    if not user_id:
        return jsonify({"error": "Missing user-id"}), 400

    image.stream.seek(0)
    try:
        hgb = estimate_hemoglobin(image, save_debug=True, user_id=user_id)
        if hgb == 0:
            return jsonify({"error": "No eye region detected"}), 400
        return jsonify({
            "message": "Detection complete",
            "hemo": hgb
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
