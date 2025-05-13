import subprocess
import time


BLENDER_PATH = "/Applications/Blender.app/Contents/MacOS/Blender"  
BLEND_FILE_PATH = "/Users/coding/blendertracking_final/face.blend"  
BLEND_FILE_PATH = "/Users/coding/blendertracking_final/face.blend"  
BLENDER_SCRIPT_PATH = "/Users/coding/blendertracking_final/blender_receiver.py"  
FACE_TRACKING_SCRIPT = "/Users/coding/blendertracking_final/face.py"  
VENV_ACTIVATE_PATH = "/Users/coding/blendertracking_final/venv/bin/activate"  


print("Starting Blender...")
blender_process = subprocess.Popen([BLENDER_PATH, BLEND_FILE_PATH, "--python", BLENDER_SCRIPT_PATH])


time.sleep(5)


print("Starting face tracking script...")
face_tracking_process = subprocess.Popen(
    f"source {VENV_ACTIVATE_PATH} && python3 {FACE_TRACKING_SCRIPT}",
    shell=True,
    executable="/bin/bash"  
)

try:
    blender_process.wait()
    face_tracking_process.wait()
except KeyboardInterrupt:
    print("Shutting down...")
    blender_process.terminate()
    face_tracking_process.terminate()
