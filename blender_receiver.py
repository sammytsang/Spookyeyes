import bpy
import socket
import json
import threading
import queue


HOST = 'localhost'
PORT = 12349

data_queue = queue.Queue()


def receive_coordinates():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Listening for face.py on {HOST}:{PORT}")
    
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")
    
    while True:
        try:
            
            data = conn.recv(1024).decode('utf-8')
            if not data:
                continue
            
            
            face_data = json.loads(data)
            x = face_data['x']
            y = face_data['y']

            
            print(f"Received from face.py: X={x}, Y={y}")
            
            
            data_queue.put((x, y))
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Invalid data received: {e}")
        except Exception as e:
            print(f"Error receiving data: {e}")
            break


import math
from mathutils import Euler

def update_eye_position():
    try:
        while not data_queue.empty():
            x, y = data_queue.get()

            armature = bpy.data.objects["RIG-rain"]
            main_eye_con = armature.pose.bones["TGT-Eyes"]

            
            scale = 0.05

            
            main_eye_con.location.z = x * scale     
            main_eye_con.location.y = -y * scale    

            print(f"Moved TGT-Eyes: Z={x * scale:.2f}, Y={-y * scale:.2f}")
            bpy.context.view_layer.update()

    except Exception as e:
        print(f"Error updating bone location: {e}")




thread = threading.Thread(target=receive_coordinates, daemon=True)
thread.start()


def timer_update():
    update_eye_position()
    return 0.1  


bpy.app.timers.register(timer_update)