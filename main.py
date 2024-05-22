import time
import cv2
import face_recognition
import requests

# Load and encode the image of "Aditi"
img1 = cv2.imread("images_facerec/aditi.jpeg")
rgb_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
img_encoded1 = face_recognition.face_encodings(rgb_img1)[0]

known_face_encodings = [img_encoded1]
known_face_names = ["Aditi"]

video_capture = cv2.VideoCapture(0)

start_time = time.time()  # Record the start time

name = "Unknown"  # Default name if no match is found

while True:
    ret, frame = video_capture.read()

    key = cv2.waitKey(1)
    if key == 27:
        break

    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for face_encoding in face_encodings:
        match = face_recognition.compare_faces(known_face_encodings, face_encoding)

        if True in match:
            first_match_index = match.index(True)
            name = known_face_names[first_match_index]
            
            # Send the recognized name to the Flask server
            requests.post('http://127.0.0.1:5000/update_name', json={'name': name})

            cv2.putText(frame, name, (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            
            # Close the application once a match is found
            video_capture.release()
            cv2.destroyAllWindows()
            exit()

    if time.time() - start_time > 5:
       break

    # cv2.imshow("video", frame) 

# Send the default name "Unknown" to the Flask server if "Aditi" is not found
requests.post('http://127.0.0.1:5000/update_name', json={'name': name})

video_capture.release()
cv2.destroyAllWindows()
