# requirements: pip install mediapipe opencv-python numpy scipy
import cv2, math, threading, winsound
import numpy as np
import mediapipe as mp
from scipy.spatial import distance as dist

# EAR function (expects list of 6 (x,y) points)
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C) if C != 0 else 0
    return ear

# MediaPipe indices for EAR (common selection)
RIGHT_EYE = [33, 160, 158, 133, 153, 144]   # right eye: p1..p6
LEFT_EYE  = [362, 385, 387, 263, 373, 380]  # left eye: p1..p6

mp_face = mp.solutions.face_mesh
mp_draw = mp.solutions.drawing_utils

# ==== Tunable parameters ====
EYE_AR_THRESH = 0.27        # more sensitive than 0.25
EYE_AR_CONSEC_FRAMES = 20   # ~0.8 sec at 25 FPS (was 48)

COUNTER = 0
ALARM_ON = False

def sound_alarm():
    winsound.PlaySound("alarm.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
    print("ALARM!")

def stop_alarm():
    winsound.PlaySound(None, winsound.SND_PURGE)

cap = cv2.VideoCapture(0)
with mp_face.FaceMesh(max_num_faces=1,
                      refine_landmarks=True,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5) as face_mesh:
    while True:
        ret, frame = cap.read()
        if not ret: break
        h, w = frame.shape[:2]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            lm = results.multi_face_landmarks[0].landmark
            def lm_to_xy(idx):
                x = int(lm[idx].x * w)
                y = int(lm[idx].y * h)
                return (x, y)
            # get eye points
            left_eye_pts = [lm_to_xy(i) for i in LEFT_EYE]
            right_eye_pts = [lm_to_xy(i) for i in RIGHT_EYE]
            # compute EAR for both eyes and average
            left_ear = eye_aspect_ratio(left_eye_pts)
            right_ear = eye_aspect_ratio(right_eye_pts)
            ear = (left_ear + right_ear) / 2.0

            # print EAR for debugging
            print(f"EAR={ear:.3f}")

            # drowsiness logic
            if ear < EYE_AR_THRESH:
                COUNTER += 1
                if COUNTER >= EYE_AR_CONSEC_FRAMES and not ALARM_ON:
                    ALARM_ON = True
                    t = threading.Thread(target=sound_alarm)
                    t.daemon = True
                    t.start()
            else:
                COUNTER = 0
                if ALARM_ON:
                    ALARM_ON = False
                    stop_alarm()

            # debug overlay
            cv2.putText(frame, f"EAR: {ear:.2f}", (10,30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)
            if ALARM_ON:
                cv2.putText(frame, "DROWSINESS ALERT!", (10,80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255),2)

        cv2.imshow("Drowsiness", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
cap.release()
cv2.destroyAllWindows()
