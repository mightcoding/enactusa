import cv2
import numpy as np
import sqlite3

# Initialize the face recognizer and load the trained data
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('recognizer/trainingData.yml')

# Load the pre-trained face detection model
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def getProfile(id):
    profile = None
    try:
        with sqlite3.connect("FaceBase.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Users WHERE ID = ?", (id,))
            profile = cursor.fetchone()  # Retrieves the first entry if multiple are found
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"General exception: {e}")
    finally:
        return profile

# Open the default camera
cam = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret, img = cam.read()
    if ret:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            print(id, conf)
            if conf < 100:  # Threshold may need adjustment
                profile = getProfile(id)
                if profile:
                    # Display user information
                    cv2.putText(img, "Name: " + str(profile[1]), (x, y-40), font, 1, (0, 255, 0), 2)
                    cv2.putText(img, "Age: " + str(profile[2]), (x, y-20), font, 1, (0, 255, 0), 2)
                    cv2.putText(img, "Addiction stage: " + str(profile[4]), (x, y), font, 1, (0, 255, 0), 2)
            else:
                cv2.putText(img, "Unknown", (x, y-10), font, 1, (0, 0, 255), 2)

        cv2.imshow('Face', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cam.release()
cv2.destroyAllWindows()
