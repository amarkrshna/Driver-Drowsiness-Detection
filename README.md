# Drowsiness Detection System

This project implements a **real-time drowsiness detection system** using **MediaPipe FaceMesh** and **Eye Aspect Ratio (EAR)**.  
If the driver's eyes remain closed beyond a certain threshold, an alarm sound is triggered to alert them.

## Features
- Real-time eye-tracking using **MediaPipe FaceMesh**.
- Calculates **Eye Aspect Ratio (EAR)** to detect drowsiness.
- Plays an alarm (`alarm.wav`) when drowsiness is detected.
- Configurable sensitivity thresholds.

## Requirements
- Python **3.10** (recommended for compatibility)
- A working webcam
- `alarm.wav` sound file in the project directory (used for the alarm)


## Installation & Setup

### 1. Clone the repository
```
git clone https://github.com/yourusername/Driver-Drowsiness-Detection.git
cd Driver-Drowsiness-Detection
````

### 2. Create a Virtual Environment (Python 3.10)

```
python3.10 -m venv venv
```

### 3. Activate the Virtual Environment

* **Windows (PowerShell)**

  ```
  venv\Scripts\activate
  ```
* **Linux / macOS**

  ```
  source venv/bin/activate
  ```

### 4. Install Dependencies

```
pip install --upgrade pip
pip install -r requirements.txt
```

## Usage

### Run the App

```
python main.py
```

### Controls

* Press **`q`** to quit the application.

## Configuration

You can tweak sensitivity by editing `main.py`:

```python
EYE_AR_THRESH = 0.27        # Eye aspect ratio threshold (lower = stricter)
EYE_AR_CONSEC_FRAMES = 20   # Consecutive frames before alarm triggers
```

## Troubleshooting

* **Alarm not playing?**

  * Ensure `alarm.wav` is in the same folder as `main.py`.
  * Windows users must keep `winsound` (default module).
* **Webcam not opening?**

  * If `cv2.VideoCapture(0)` doesn’t work, try `cv2.VideoCapture(1)` for an external webcam.


## Example Output

* EAR values are displayed in the console.
* The app window shows:

  * **EAR value overlay**
  * **DROWSINESS ALERT!** text if detected

## License

This project is licensed under the MIT License.

