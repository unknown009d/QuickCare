import cv2
import numpy as np
from config import (
    UPLOAD_FOLDER, EYE_DETECTION, CONJUNCTIVA_CROP,
    HSV_THRESHOLDS, HGB_SCALE, HGB_CALIBRATION
)
import os

def estimate_hemoglobin(image_stream, save_debug=True, user_id=None):
    """Detects eye region, extracts conjunctiva, estimates hemoglobin."""

    if not user_id:
        raise ValueError("Missing user_id — required for per-user file separation")

    file_bytes = np.frombuffer(image_stream.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode uploaded image")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    eyes = eye_cascade.detectMultiScale(
        gray,
        scaleFactor=EYE_DETECTION["scaleFactor"],
        minNeighbors=EYE_DETECTION["minNeighbors"],
        minSize=EYE_DETECTION["minSize"]
    )

    if save_debug:
        cv2.imwrite(os.path.join(UPLOAD_FOLDER, f"original_{user_id}.jpg"), img)

    if len(eyes) == 0:
        return 0

    for (ex, ey, ew, eh) in eyes:
        eye_roi = img[ey:ey+eh, ex:ex+ew]
        h, w = eye_roi.shape[:2]

        lc = int(h / CONJUNCTIVA_CROP["lower_crop_ratio"])
        lt = int(w / CONJUNCTIVA_CROP["left_trim_ratio"])
        rt = int(w / CONJUNCTIVA_CROP["right_trim_ratio"])
        eye_roi = eye_roi[lc:h, lt:(w - rt)]

        hsv = cv2.cvtColor(eye_roi, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(hsv, HSV_THRESHOLDS["lower_red1"], HSV_THRESHOLDS["upper_red1"])
        mask2 = cv2.inRange(hsv, HSV_THRESHOLDS["lower_red2"], HSV_THRESHOLDS["upper_red2"])
        mask = cv2.bitwise_or(mask1, mask2)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        mask = cv2.GaussianBlur(mask, (5, 5), 0)

        cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not cnts:
            continue

        c = max(cnts, key=cv2.contourArea)
        mask_contour = np.zeros_like(mask)
        cv2.drawContours(mask_contour, [c], -1, 255, thickness=cv2.FILLED)
        conjunctiva = cv2.bitwise_and(eye_roi, eye_roi, mask=mask_contour)

        if save_debug:
            cv2.imwrite(os.path.join(UPLOAD_FOLDER, f"eye_0_{user_id}.jpg"), eye_roi)
            cv2.imwrite(os.path.join(UPLOAD_FOLDER, f"mask_0_{user_id}.jpg"), mask)
            cv2.imwrite(os.path.join(UPLOAD_FOLDER, f"conjunctiva_0_{user_id}.jpg"), conjunctiva)

        non_black = cv2.inRange(conjunctiva, np.array([10, 10, 10]), np.array([255, 255, 255]))
        mean_bgr = cv2.mean(conjunctiva, mask=non_black)
        b, g, r = mean_bgr[:3]

        color_intensity = (r - g * 0.5 - b * 0.25)
        Hgb = HGB_CALIBRATION["offset"] + (color_intensity / HGB_CALIBRATION["scale_divisor"]) * HGB_CALIBRATION["scale_factor"]
        Hgb = round(max(HGB_SCALE["min"], min(HGB_SCALE["max"], Hgb)), 1)

        return Hgb

    return 0