# Driver Drowsiness Detection with Dynamic EAR Calibration

## Project Overview

Keamanan berkendara adalah prioritas utama dalam industri transportasi. Proyek ini menghadirkan solusi berbasis **Computer Vision** untuk mendeteksi tanda-tanda kelelahan dan kantuk pada pengemudi secara real-time.

Sistem ini menggunakan algoritma **Eye Aspect Ratio (EAR)** yang dipadukan dengan **Dynamic Calibration** untuk memastikan akurasi yang tinggi bagi setiap profil mata pengemudi yang unik.

## Fitur-fitur

* **Dynamic Calibration:** Sistem mempelajari kondisi mata normal pengguna selama 5 detik pertama untuk menetapkan ambang batas (*threshold*) yang dipersonalisasi.
* **Real-time Monitoring:** Deteksi instan menggunakan MediaPipe Face Mesh (468 landmarks) yang ringan dan efisien.
* **Multi-tier Alert:**
  * **Visual Alert:** Bingkai merah pada layar saat kantuk terdeteksi.
  * **Audio Alert:** Peringatan suara (Beep) untuk membangunkan pengemudi.
* **Automated Data Logging:** Setiap insiden kantuk dicatat secara otomatis ke dalam file `log_kantuk.csv` untuk analisis keselamatan lebih lanjut.

## Cara Kerja

Sistem ini menghitung **Eye Aspect Ratio (EAR)** berdasarkan koordinat titik mata.

$$EAR = \frac{||p_2 - p_6|| + ||p_3 - p_5||}{2||p_1 - p_4||}$$

Ketika mata tertutup untuk jangka waktu yang lama, nilai EAR akan turun di bawah ambang batas yang telah dikalibrasi, memicu protokol alarm keselamatan.

## Tech Stack yang digunakan

* **Core:** Python
* **Computer Vision:** OpenCV, MediaPipe
* **Math & Data:** NumPy, SciPy (Euclidean Distance)
* **OS Interface:** Winsound (for Windows alerts)

## Instalasi dan Cara Penggunaan

1. Clone project:

   ```bash
   git clone [https://github.com/username/driver-drowsiness-detection.git](https://github.com/username/driver-drowsiness-detection.git)
   cd driver-drowsiness-detection
   ```

2. Instal Dependency yang diperlukan

   ```bash
   pip install opencv-python mediapipe scipy numpy
   ```

3. Jalankan project

   ```bash
   python app.py
   ```

## Struktur Project

 ```plaintext
 driver-drowsiness-detection
 |-- app.py
 |-- log_kantuk.csv
 |-- README.md
 |-- requirements.txt
 ```
