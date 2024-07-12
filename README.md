# Screen-Time-Recorder-via-Face-Tracker

This Python application monitors your screen time and reminds you to stay active using a combination of Tkinter for the GUI, OpenCV for face detection, and PyAutoGUI for detecting active windows. It provides real-time tracking of application usage and user activity, ensuring you maintain healthy screen habits.

## Features
- **Face Detection:** Uses your webcam to detect if you are facing the screen.
- **Screen Time Tracking:** Records the time spent on different applications.
- **Idle Reminder:** Reminds you to stay active if no mouse movement is detected for a specified period.
- **Usage Summary:** Displays the total screen time and time facing the camera when exiting the program.
- **Simple GUI:** A user-friendly interface to start/stop recording and view usage statistics.

## Requirements
- Python 3.x
- Tkinter
- OpenCV
- PyAutoGUI

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/screen-time-tracker.git
   ```
2. Install the required packages:
   ```bash
   pip install opencv-python pyautogui
   ```

## Usage
1. Run the application:
   ```bash
   python screen_time_tracker.py
   ```
2. Click "Start Recording" to begin tracking your screen time and activity.
3. View the real-time statistics in the GUI.
4. Click "Exit" to stop recording and see the summary of your usage.
