import cv2
import numpy as np
import os
from config import UPLOAD_FOLDER, EYE_DETECTION, CONJUNCTIVA_CROP, HSV_THRESHOLDS, HGB_SCALE, HGB_CALIBRATION


def get_user_dir(user_id):
    """Ensure each user has a dedicated folder."""
    user_dir = os.path.join(UPLOAD_FOLDER, user_id)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir


def save_uploaded_image(image_stream, user_id):
    user_dir = get_user_dir(user_id)
    file_bytes = np.frombuffer(image_stream.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode uploaded image")

    path = os.path.join(user_dir, "original.jpg")
    cv2.imwrite(path, img)
    return path


def detect_eye_region(user_id):
    user_dir = get_user_dir(user_id)
    img_path = os.path.join(user_dir, "original.jpg")

    img = cv2.imread(img_path)
    if img is None:
        return False

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    eyes = eye_cascade.detectMultiScale(
        gray,
        scaleFactor=EYE_DETECTION["scaleFactor"],
        minNeighbors=EYE_DETECTION["minNeighbors"],
        minSize=EYE_DETECTION["minSize"]
    )

    if len(eyes) == 0:
        return False

    (ex, ey, ew, eh) = eyes[0]
    eye_roi = img[ey:ey+eh, ex:ex+ew]
    cv2.imwrite(os.path.join(user_dir, "eye.jpg"), eye_roi)
    return True


def crop_conjunctiva(user_id):
    user_dir = get_user_dir(user_id)
    eye_path = os.path.join(user_dir, "eye.jpg")

    eye_roi = cv2.imread(eye_path)
    if eye_roi is None:
        return False

    h, w = eye_roi.shape[:2]
    lc = int(h / CONJUNCTIVA_CROP["lower_crop_ratio"])
    lt = int(w / CONJUNCTIVA_CROP["left_trim_ratio"])
    rt = int(w / CONJUNCTIVA_CROP["right_trim_ratio"])
    cropped = eye_roi[lc:h, lt:(w - rt)]

    hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, HSV_THRESHOLDS["lower_red1"], HSV_THRESHOLDS["upper_red1"])
    mask2 = cv2.inRange(hsv, HSV_THRESHOLDS["lower_red2"], HSV_THRESHOLDS["upper_red2"])
    mask = cv2.bitwise_or(mask1, mask2)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)

    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cnts:
        cv2.imwrite(os.path.join(user_dir, "cropped.jpg"), cropped)
        return True

    c = max(cnts, key=cv2.contourArea)
    mask_contour = np.zeros_like(mask)
    cv2.drawContours(mask_contour, [c], -1, 255, thickness=cv2.FILLED)
    conjunctiva = cv2.bitwise_and(cropped, cropped, mask=mask_contour)

    cv2.imwrite(os.path.join(user_dir, "cropped.jpg"), conjunctiva)
    return True


def calculate_hemoglobin(user_id):
    import time
    time.sleep(2)  # Simulate small delay

    user_dir = get_user_dir(user_id)
    img_path = os.path.join(user_dir, "cropped.jpg")
    eye_roi = cv2.imread(img_path)
    if eye_roi is None:
        return 0

    hsv = cv2.cvtColor(eye_roi, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, HSV_THRESHOLDS["lower_red1"], HSV_THRESHOLDS["upper_red1"])
    mask2 = cv2.inRange(hsv, HSV_THRESHOLDS["lower_red2"], HSV_THRESHOLDS["upper_red2"])
    mask = cv2.bitwise_or(mask1, mask2)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)

    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cnts:
        return 0

    c = max(cnts, key=cv2.contourArea)
    mask_contour = np.zeros_like(mask)
    cv2.drawContours(mask_contour, [c], -1, 255, thickness=cv2.FILLED)
    conjunctiva = cv2.bitwise_and(eye_roi, eye_roi, mask=mask_contour)

    non_black = cv2.inRange(conjunctiva, np.array([10, 10, 10]), np.array([255, 255, 255]))
    mean_bgr = cv2.mean(conjunctiva, mask=non_black)
    b, g, r = mean_bgr[:3]

    color_intensity = (r - g * 0.5 - b * 0.25)
    Hgb = HGB_CALIBRATION["offset"] + (color_intensity / HGB_CALIBRATION["scale_divisor"]) * HGB_CALIBRATION["scale_factor"]
    Hgb = round(max(HGB_SCALE["min"], min(HGB_SCALE["max"], Hgb)), 1)

    return Hgb
