import cv2
import mediapipe as mp
from scipy.spatial import distance as dist
import numpy as np
import time
import winsound
import csv
from datetime import datetime

# 1. Konfigurasi & Parameter
RIGHT_EYE = [33, 160, 158, 133, 153, 144]
LEFT_EYE = [362, 385, 387, 263, 373, 380]
CONSECUTIVE_FRAMES = 25  # Berapa fps mata tertutup sebelum alarm berbunyi
CALIBRATION_TIME = 5     # Durasi kalibrasi dalam detik

# Inisialisasi Variabel
counter = 0
calibration_done = False
normal_ears = []
best_threshold = 0.25 # Nilai default

# 2. Fungsi Hitung EAR untuk menghitung seberapa tinggi mata dibandingkan lebar mata
def calculate_ear(eye_points):
    # Jarak vertikal
    v1 = dist.euclidean(eye_points[1], eye_points[5])
    v2 = dist.euclidean(eye_points[2], eye_points[4])
    # Jarak horizontal
    h = dist.euclidean(eye_points[0], eye_points[3])
    ear = (v1 + v2) / (2.0 * h)
    return ear

# 3. Setup MediaPipe & Kamera
mp_face_mesh = mp.solutions.face_mesh

# beri nilai refine_landmarks = True agar area mata dan bibir dapat ditangkap dengan lebih detail
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)
cap = cv2.VideoCapture(0)

print("Program Dimulai. Siapkan posisi mata melek normal untuk kalibrasi...")
start_time = time.time()

# Siapkan file CSV untuk log
with open('log_drowsiness.csv', mode='a', newline='') as file:
    writer = csv.writer(file)
    # Tulis header jika file baru
    # writer.writerow(['Timestamp', 'EAR_Value', 'Status'])

    while cap.isOpened():
        success, image = cap.read()
        if not success: break

        image = cv2.flip(image, 1)
        h, w, _ = image.shape
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_image)
        
        current_time = time.time()

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                coords = [(lm.x * w, lm.y * h) for lm in face_landmarks.landmark]
                
                left_points = [coords[i] for i in LEFT_EYE]
                right_points = [coords[i] for i in RIGHT_EYE]
                
                avg_ear = (calculate_ear(left_points) + calculate_ear(right_points)) / 2.0

                # --- FASE 1: KALIBRASI DINAMIS ---
                if not calibration_done:
                    if current_time - start_time < CALIBRATION_TIME:
                        normal_ears.append(avg_ear)
                        cv2.putText(image, f"KALIBRASI: {int(CALIBRATION_TIME - (current_time-start_time))}s", 
                                    (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                    else:
                        best_threshold = np.mean(normal_ears) * 0.75
                        calibration_done = True
                        print(f"Kalibrasi Selesai! Threshold diset ke: {best_threshold:.2f}")

                # --- FASE 2: MONITORING ---
                else:
                    cv2.putText(image, f"EAR: {avg_ear:.2f} | Thr: {best_threshold:.2f}", 
                                (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

                    if avg_ear < best_threshold:
                        counter += 1
                        if counter >= CONSECUTIVE_FRAMES:
                            # EFEK ALARM
                            cv2.rectangle(image, (0,0), (w,h), (0,0,255), 10) # Frame Merah
                            cv2.putText(image, "BAHAYA: ANDA MENGANTUK!", (50, h//2), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 4)
                            
                            # Suara Beep (Frekuensi, Durasi ms)
                            winsound.Beep(1000, 500) 
                            
                            # Logging ke CSV
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            writer.writerow([timestamp, f"{avg_ear:.2f}", "Drowsy"])
                    else:
                        counter = 0

        cv2.imshow('Safety Drive AI - Drowsiness Detection', image)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()