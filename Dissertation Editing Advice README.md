# Spookyeyes 👁️

**Spookyeyes** is a real-time face tracking and gaze animation system that dynamically controls the eyes of a 3D character in Blender based on the user’s face position, captured via webcam. Built entirely with open-source tools and designed for use on consumer hardware, this project enables lifelike gaze simulation for digital avatars, installations, and interactive media.

## 📸 Features

- Real-time face detection using OpenCV's deep neural network (DNN)
- Socket-based data transmission from Python to Blender
- Dynamic eye animation in a fully rigged 3D character model
- No external GPU or specialist hardware required
- Fully offline/local processing (no server dependency)

## 🖥️ System Requirements

- macOS or Windows with Python 3.9+ (tested on macOS M1)
- Blender 4.2.3 or newer
- Webcam (built-in or external)

## 🧰 Installation

1. **Clone the Repository**
   ```
   git clone https://github.com/sammytsang/Spookyeyes.git
   cd Spookyeyes
   ```

2. **Install Python Dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Make Sure Blender is Installed**
   Download the latest version of Blender: https://www.blender.org/download/

## 🚀 Running the Project

1. Open a terminal in the `Spookyeyes` folder.
2. Launch the system with:
   ```
   python launcher.py
   ```
   This will:
   - Open the preconfigured Blender file
   - Start the face detection script
   - Begin live tracking and animation

## 📁 Folder Structure

```
Spookyeyes/
├── blender_receiver.py       # Blender-side socket listener
├── face.py                   # Real-time face detection and coordinate tracking
├── launcher.py               # Orchestrator to launch Blender and tracking
├── face.blend                # Pre-rigged Blender file with stylised model
├── models/                   # DNN model files (Caffe format)
├── textures/                 # Character texture assets
├── requirements.txt          # List of required Python packages
```

## 🧪 Performance

- Average FPS: ~9–10
- Latency: ~100–150 ms
- CPU usage: ~70% (Blender and Python processes combined)
- Optimised for real-time performance on mid-range laptops

## 📸 Example

![Preview](docs/screenshot.png)  
*A stylised character with eyes responding to user head movements in real time.*

## 🧠 Credits

- Developed by **Chun Kit Sam Tsang**
- Supervisor: Prof. Simon Sherratt  
- Tools used: Python, OpenCV, Blender

## 📄 License

This project is open-source and available for educational and research purposes.
