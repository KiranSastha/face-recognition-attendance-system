# Face Recognition Attendance System

A Python-based real-time face recognition system using OpenCV and face_recognition.  
Automatically loads users from folders, recognizes faces using webcam or IP camera, and logs results.

---

## 🚀 Features
- Real-time face recognition
- Auto-detect user folders (no code changes)
- Logs to TXT + CSV
- Confidence % display
- Frame-skip performance optimization

---

## 📁 Project Structure
face_recog_project/

├── train_and_recognize.py

├── requirements.txt

├── README.md

├── LICENSE

├── .gitignore

├── logs/

│ ├── recognition_log.txt

│ └── recognition_log.csv

│── kiran/

│└── images of the person

└── 


---

## ⚙️ Installation
git clone https://github.com/KiranSastha/face-recognition-attendance-system.git

cd YOUR_REPO

python -m venv venv

venv/Scripts/activate

pip install -r requirements.txt



---

## ▶️ Run the Project

python train_and_recognize.py



---

## 📸 Adding New Users
Just add a new photos and create folders  
Example:
john/

john1.jpg

john2.jpg


No code changes required.

---

## 🎯 Future Goals
- Add GUI registration system
- Build online attendance dashboard
- Multi-camera support for CCTV
- Deploy on Raspberry Pi for portable system
- Add encryption for face encodings
- Create installer (.exe)

---

## 🧾 License
MIT License (see LICENSE file)

---

## 👤 Author
**Kiran S K**
