import bpy
import socket
import json
import threading
import queue

# Socket configuration
HOST = 'localhost'
PORT = 12349

# Thread-safe queue to handle incoming data
data_queue = queue.Queue()

# Function to handle incoming data from face.py
def receive_coordinates():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Listening for face.py on {HOST}:{PORT}")
    
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")
    
    while True:
        try:
            # Receive data
            data = conn.recv(1024).decode('utf-8')
            if not data:
                continue
            
            # Parse JSON data
            face_data = json.loads(data)
            x = face_data['x']
            y = face_data['y']

            # Debugging: Print received data
            print(f"Received from face.py: X={x}, Y={y}")
            
            # Add data to the queue
            data_queue.put((x, y))
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Invalid data received: {e}")
        except Exception as e:
            print(f"Error receiving data: {e}")
            break

# Function to update the Main Eye Con bone's position
import math
from mathutils import Euler

def update_eye_position():
    try:
        while not data_queue.empty():
            x, y = data_queue.get()

            armature = bpy.data.objects["RIG-rain"]
            main_eye_con = armature.pose.bones["TGT-Eyes"]

            # ✅ Scale for natural motion
            scale = 0.05

            # ✅ Correct mirrored directions
            main_eye_con.location.z = x * scale     # LEFT/RIGHT (Z axis, flipped back)
            main_eye_con.location.y = -y * scale    # UP/DOWN (Y axis, still mirrored)

            print(f"Moved TGT-Eyes: Z={x * scale:.2f}, Y={-y * scale:.2f}")
            bpy.context.view_layer.update()

    except Exception as e:
        print(f"Error updating bone location: {e}")




# Start a thread to listen for data
thread = threading.Thread(target=receive_coordinates, daemon=True)
thread.start()

# Timer to regularly call the update function
def timer_update():
    update_eye_position()
    return 0.1  # Update every 0.1 seconds

# Register the timer in Blender
bpy.app.timers.register(timer_update)