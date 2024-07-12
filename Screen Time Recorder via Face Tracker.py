import tkinter as tk
import time
import pyautogui
import cv2
import tkinter.messagebox as msgbox

app_usage_times = {}
recording = False
start_time = None
total_time = 0  # Total time spent on the screen
paused_time = 0  # Time when the user is not facing the camera
facing_time = 0  # Time when the user is facing the camera

# Define the time interval for recording screen time (in seconds)
interval = 1  # 1 second

# Define the time threshold for reminding the user to be active (in seconds)
reminder_threshold = 30

# Create a VideoCapture object for the default camera (usually the webcam)
cap = cv2.VideoCapture(0)

# Store the last time the mouse was moved
last_mouse_move_time = time.time()

# Flag to check if the warning message has been shown
warning_message_shown = False


def detect_face(image):
    # Load a pre-trained face detection classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Convert the image to grayscale for face detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return image, len(faces) > 0


def check_mouse_activity():
    global last_mouse_move_time

    current_time = time.time()

    if (current_time - last_mouse_move_time) > reminder_threshold:
        remind_user_to_be_active()

    root.after(1000, check_mouse_activity)


def remind_user_to_be_active():
    global last_mouse_move_time, warning_message_shown

    if not warning_message_shown:
        msgbox.showinfo("Reminder", "Be active! .")
        # Update the last mouse move time after the message box is closed
        last_mouse_move_time = time.time()


def update_usage_time():
    global app_usage_times, recording, start_time, total_time, paused_time, facing_time, warning_message_shown

    ret, frame = cap.read()

    if ret:
        frame, is_user_facing_camera = detect_face(frame)

        if recording:
            active_window = pyautogui.getActiveWindow()
            if active_window:
                window_title = active_window.title
            else:
                window_title = "Desktop"

            if is_user_facing_camera:
                current_time = time.time()
                elapsed_time = current_time - start_time
                app_usage_times[window_title] = app_usage_times.get(window_title, 0) + elapsed_time

                facing_time += elapsed_time
                total_time += elapsed_time
                start_time = current_time

                # Check if total time exceeds the threshold
                if total_time > reminder_threshold and not warning_message_shown:
                    msgbox.showwarning("Warning", "You have exceeded 20 seconds of screen time! Take a break.")
                    warning_message_shown = True

            else:
                paused_time = time.time() - start_time

        cv2.imshow('Face Detection', frame)
        cv2.waitKey(1)

    update_display()
    root.after(interval * 1000, update_usage_time)


def start_recording():
    global recording, start_time, warning_message_shown
    recording = True
    start_time = time.time()
    warning_message_shown = False  # Reset the warning flag
    update_usage_time()


def exit_program():
    global recording, start_time, total_time, paused_time, facing_time
    if recording:
        total_time = sum(app_usage_times.values()) + paused_time
        msgbox.showinfo("Screen Time Summary", f"Total Time Spent on Screen: {total_time:.2f} seconds\n"
                                               f"Time Facing Camera: {facing_time:.2f} seconds")
    cap.release()
    cv2.destroyAllWindows()
    root.destroy()


def update_display():
    text.delete('1.0', tk.END)
    text.insert(tk.END, "Application Usage Times:\n")
    for app, time_used in app_usage_times.items():
        text.insert(tk.END, f"{app}: {time_used:.2f} seconds\n")

    facing_time_label.config(text=f"Time Facing Camera: {facing_time:.2f} seconds")


root = tk.Tk()
root.title("Screen Time Recorder")

text = tk.Text(root)
text.pack()

start_button = tk.Button(root, text="Start Recording", command=start_recording)
start_button.pack()

exit_button = tk.Button(root, text="Exit", command=exit_program)
exit_button.pack()

# Create a label for the facing time
facing_time_label = tk.Label(root, text="Time Facing Camera: 0.00 seconds")
facing_time_label.pack()

update_display()

root.after(100, update_usage_time)  # Start the screen time tracking after a short delay
root.after(1000, check_mouse_activity)  # Start checking mouse activity after a short delay

root.mainloop()