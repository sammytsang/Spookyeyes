import cv2
import numpy as np
import socket
import json
import time
import signal
import sys


def signal_handler(sig, frame):
    print("Exiting...")
    cap.release()
    cv2.destroyAllWindows()
    client_socket.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


cap = cv2.VideoCapture(0)


model_file = "/Users/coding/blendertracking/models/deploy.prototxt"
weights_file = "/Users/coding/blendertracking/models/res10_300x300_ssd_iter_140000_fp16.caffemodel"
face_net = cv2.dnn.readNetFromCaffe(model_file, weights_file)


MIN_FACE_WIDTH = 80
MIN_FACE_HEIGHT = 80


smoothed_x, smoothed_y = None, None
alpha = 0.5  


movement_threshold = 5  


prev_frame_time = 0
new_frame_time = 0


while True:
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12349))  
        print("Connected to Blender")
        break
    except ConnectionRefusedError:
        print("Blender not ready, retrying in 2 seconds...")
        time.sleep(2)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    
    frame = cv2.flip(frame, 1)

    
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))

   
    face_net.setInput(blob)
    detections = face_net.forward()

    detected_faces = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > 0.7:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x, y, x1, y1) = box.astype("int")

            face_width = x1 - x
            face_height = y1 - y

            if face_width >= MIN_FACE_WIDTH and face_height >= MIN_FACE_HEIGHT:
                detected_faces.append((x, y, x1, y1))

    if detected_faces:
        (x, y, x1, y1) = detected_faces[0]

        center_x, center_y = (x + x1) // 2, (y + y1) // 2

        offset_x = center_x - (w // 2)
        offset_y = center_y - (h // 2)

        if smoothed_x is None or smoothed_y is None:
            smoothed_x, smoothed_y = offset_x, offset_y
        else:
            smoothed_x = alpha * offset_x + (1 - alpha) * smoothed_x
            smoothed_y = alpha * offset_y + (1 - alpha) * smoothed_y

        if abs(smoothed_x - offset_x) > movement_threshold or abs(smoothed_y - offset_y) > movement_threshold:
            smoothed_x, smoothed_y = offset_x, offset_y

        print(f"Scaled and Sending to Blender: X={smoothed_x * 0.01:.2f}, Y={smoothed_y * 0.01:.2f}")

        face_data = {
            'x': smoothed_x * 0.01,
            'y': smoothed_y * 0.01
        }
        try:
            client_socket.sendall(json.dumps(face_data).encode('utf-8'))
            time.sleep(0.05)
        except Exception as e:
            print(f"Error sending data: {e}")

        cv2.rectangle(frame, (x, y), (x1, y1), (255, 0, 0), 2)
        cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)
    else:
        face_data = {'x': 0, 'y': 0}
        try:
            client_socket.sendall(json.dumps(face_data).encode('utf-8'))
            time.sleep(0.05)
        except Exception as e:
            print(f"Error sending data: {e}")

    
    new_frame_time = time.time()
    fps = 1 / (new_frame_time - prev_frame_time + 1e-8)
    prev_frame_time = new_frame_time
    print(f"FPS: {fps:.2f}")  
    cv2.putText(frame, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
            0.8, (0, 255, 0), 2, cv2.LINE_AA)
# -----------------------------------

    # -----------------------------------

    
    cv2.imshow('Face Tracking (Mirrored)', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
client_socket.close()
