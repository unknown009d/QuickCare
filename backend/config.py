import numpy as np
import os

# Upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Eye detection
EYE_DETECTION = {
    "scaleFactor": 1.1,
    "minNeighbors": 4,
    "minSize": (40, 40)
}

# Conjunctiva cropping ratios
CONJUNCTIVA_CROP = {
    "lower_crop_ratio": 1.7,
    "left_trim_ratio": 6,
    "right_trim_ratio": 10
}

# HSV thresholds
HSV_THRESHOLDS = {
    "lower_red1": np.array([0, 40, 60]),
    "upper_red1": np.array([10, 255, 255]),
    "lower_red2": np.array([160, 40, 60]),
    "upper_red2": np.array([180, 255, 255])
}

# Hemoglobin scaling
HGB_SCALE = {
    "min": 8.0,
    "max": 16.5,
    "offset": 8,
    "factor": 8
}

HGB_CALIBRATION = {
    "offset": 11,
    "scale_divisor": 160,
    "scale_factor": 7
}