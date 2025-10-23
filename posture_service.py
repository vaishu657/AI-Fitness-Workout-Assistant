from PIL import Image
import os

try:
    import cv2
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False

try:
    import mediapipe as mp
    HAS_MEDIAPIPE = True
except ImportError:
    HAS_MEDIAPIPE = False


def analyze_image(path):
    try:
        img = Image.open(path)
        w, h = img.size
    except Exception as e:
        return {"ok": False, "error": f"Could not open image: {e}"}

    advice = []
    if w < 200 or h < 200:
        advice.append("Image is small — move camera back to capture full body.")
    advice.append("Ensure good lighting and that your whole body is visible.")
    advice.append("Tip: keep back straight, engage your core.")

    if HAS_MEDIAPIPE and HAS_OPENCV:
        try:
            mp_pose = mp.solutions.pose
            img_cv = cv2.imread(path)

            if img_cv is None:
                advice.append("Error: OpenCV could not read the image. Check the file path.")
            else:
                img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
                with mp_pose.Pose(static_image_mode=True) as pose:
                    results = pose.process(img_rgb)
                    if not results.pose_landmarks:
                        advice.append("Couldn't detect pose landmarks. Try a full-body photo.")
                    else:
                        advice.append("Pose detected — posture seems OK (basic check).")
        except Exception as e:
            advice.append(f"MediaPipe analysis error: {e}")
    else:
        advice.append("MediaPipe or OpenCV not available in this environment.")

    return {"ok": True, "size": [w, h], "advice": advice}
