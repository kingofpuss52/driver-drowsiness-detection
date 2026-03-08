# Driver Drowsiness Detection with Dynamic EAR Calibration

## Project Overview

Driving safety is a top priority in the transportation industry. This project presents a **Computer Vision**-based solution to detect signs of fatigue and drowsiness in drivers in real time.

The system uses an **Eye Aspect Ratio (EAR)** algorithm combined with Dynamic Calibration to ensure high accuracy for each driver's unique eye profile.

## Key Features

* **Dynamic Calibration:** The system studies the user's normal eye condition during the first 5 seconds to set a personalized threshold.
* **Real-time Monitoring:** Instant detection using lightweight and efficient MediaPipe Face Mesh (468 landmarks).
* **Multi-tier Alert:**
  * **Visual Alert:** A red frame appears on the screen when drowsiness is detected.
  * **Audio Alert:** Audible warning (Beep) to wake up the driver.
* **Automated Data Logging:** Every drowsiness incident is automatically recorded in the `log_drowsiness.csv` file for further safety analysis.

## How It Works

This system calculates the **Eye Aspect Ratio (EAR)** based on the coordinates of the eye point.

$$EAR = \frac{||p_2 - p_6|| + ||p_3 - p_5||}{2||p_1 - p_4||}$$

When the eyes are closed for an extended period of time, the EAR value will fall below the calibrated threshold, triggering the safety alarm protocol.

## Tech Stacks

* **Core:** Python
* **Computer Vision:** OpenCV, MediaPipe
* **Math & Data:** NumPy, SciPy (Euclidean Distance)
* **OS Interface:** Winsound (for Windows alerts)

## Installation and Usage

1. Clone the project:

   ```bash
   git clone [https://github.com/username/driver-drowsiness-detection.git](https://github.com/username/driver-drowsiness-detection.git)
   cd driver-drowsiness-detection
   ```

2. Install dependencies from ```requirements.txt``` file

   ```bash
   pip install -r requirements.txt
   ```

3. Run the project

   ```bash
   python app.py
   ```

## Project Structure

 ```plaintext
 driver-drowsiness-detection
 |-- app.py
 |-- log_drowsiness.csv
 |-- README.md
 |-- requirements.txt
 ```
