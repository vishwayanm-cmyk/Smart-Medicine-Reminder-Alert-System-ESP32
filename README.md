
# Face Tracking Camera

This project uses Python, OpenCV, and MediaPipe to track a person's nose position from a webcam feed and optionally control pan/tilt servos using Arduino.

## Features

* Real-time pose landmark detection
* Nose-position tracking with on-screen debug overlay
* PID-based pan/tilt servo control
* Arduino-based serial servo control
* Works with webcam or external camera

## Requirements

* Python 3.7 or higher
* pip (Python package manager)
* Arduino IDE (for servo control)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/mr-priyam/face_tracking_camera.git
cd face_tracking_camera
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv mp_env
source mp_env/bin/activate   # Mac/Linux

# For Windows
mp_env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Run Face Tracking (Python)

```bash
python3 face_tracking_camera.py
```

The Python script opens the serial port configured in `SERIAL_PORT` before starting the webcam. Update this value in `face_tracking_camera.py` to match your Arduino port.

### Run Arduino Servo Control

1. Open `face_tracker.ino` in Arduino IDE
2. Select the correct board and port
3. Upload the code to your Arduino

## Testing

Run the unit tests from the project root:

```bash
python3 -m unittest discover -v
```

The tests cover the servo clamp helper and PID controller logic without requiring a webcam or Arduino.

## Notes

* If your webcam does not open, change camera index:

```python
cap = cv2.VideoCapture(0)
```

Try `1` or `2` if needed.

* Ensure proper lighting for better detection.
* Make sure the correct serial port is used in Python code when connecting to Arduino.

## Project Structure

```
face_tracking_camera/
│
├── face_tracking_camera.py   # Main Python script
├── face_tracker.ino          # Arduino code for servo control
├── requirements.txt
├── tests/                    # Unit tests
├── README.md
```

## Future Improvements

* Multi-face tracking
* Better smoothing for servo movement
* Integration with mobile camera
* Gesture-based control

---
