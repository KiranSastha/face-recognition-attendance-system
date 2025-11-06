import os
import cv2
import face_recognition
import numpy as np
import csv
from datetime import datetime

# ---------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------
base_dir = os.path.dirname(os.path.abspath(__file__))

# Automatically detect all subfolders (each folder = person)
people = [folder for folder in os.listdir(base_dir)
          if os.path.isdir(os.path.join(base_dir, folder)) and not folder.startswith("logs")]

# Make sure a log folder exists
log_dir = os.path.join(base_dir, "logs")
os.makedirs(log_dir, exist_ok=True)

txt_log_file = os.path.join(log_dir, "recognition_log.txt")
csv_log_file = os.path.join(log_dir, "recognition_log.csv")

# Initialize CSV log (if not already)
if not os.path.exists(csv_log_file):
    with open(csv_log_file, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Name", "Confidence (%)"])

def log_recognition(name, confidence):
    """Log recognized face with timestamp."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(txt_log_file, "a") as f:
        f.write(f"{now} - {name} ({confidence:.2f}%)\n")
    with open(csv_log_file, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([now, name, f"{confidence:.2f}"])
    print(f"🕒 {now} - Logged: {name} ({confidence:.2f}%)")

# ---------------------------------------------------
# LOAD KNOWN FACES
# ---------------------------------------------------
known_encodings = []
known_names = []

print("🔍 Auto-detecting folders and loading training images...")

for person in people:
    folder_path = os.path.join(base_dir, person)
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(folder_path, file_name)
            image = face_recognition.load_image_file(img_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(person)
                print(f"✅ Added {person}'s face from {file_name}")
            else:
                print(f"⚠️ No face found in {img_path}")

if not known_encodings:
    print("❌ No valid training images found! Please check your folders.")
    exit()

print(f"\n✅ Training complete for {len(known_encodings)} faces.")
print("🎥 Starting webcam... (Press 'Q' to quit)")

# ---------------------------------------------------
# START CAMERA
# ---------------------------------------------------
video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
video.set(cv2.CAP_PROP_FPS, 30)  # performance boost

recognized_recently = {}

# ---------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------
while True:
    ret, frame = video.read()
    if not ret:
        print("⚠️ Could not access camera.")
        break

    # Resize for faster processing (¼ size)
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Process every 2nd frame for smooth performance
    face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        name = "Unknown"
        confidence = 0.0

        # Compare and calculate confidence
        if known_encodings:
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            match = face_recognition.compare_faces([known_encodings[best_match_index]], face_encoding)[0]

            if match:
                name = known_names[best_match_index]
                distance = face_distances[best_match_index]
                # Confidence curve — better accuracy mapping
                confidence = (1 - distance) * 100
                confidence = round(confidence, 2)

        # Avoid duplicate logs within 10s
        current_time = datetime.now()
        if name != "Unknown":
            last_seen = recognized_recently.get(name)
            if not last_seen or (current_time - last_seen).seconds > 10:
                log_recognition(name, confidence)
                recognized_recently[name] = current_time

        # Scale coordinates back to original frame size
        top *= 4; right *= 4; bottom *= 4; left *= 4

        # Draw rectangle and info
        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, f"{name} ({confidence:.2f}%)", (left, top - 10),
                    cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Face Recognition (Press Q to quit)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()

print("\n📁 Logs saved successfully to:")
print(f"📝 Text log: {txt_log_file}")
print(f"📊 CSV log: {csv_log_file}")
