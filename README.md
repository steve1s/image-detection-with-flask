# Image Detection with Flask

** A lightweight web app built with Flask that performs image detection using Tensorflow and OpenCV **

---

## Table of Contents

- [Demo](#demo)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Local Python](#local-python)
- [Docker](#docker)
- [Deployment](#deployment)
- [License](#license)
- [Acknowledgement](#acknowledgement)

---

## Demo
Check out a live demo

---

## Features

- Upload an image via a web interface
- Detect objects using a TensorFlow model
- Annotate detected objects and display the results
- Built-in support for Docker deployment
- (Optional) Stream-based interface using Streamlit (`app_streamlit.py`)

## Project Structure
```
├── app.py # Main Flask application
├── app_streamlit.py # Alternative interface using Streamlit
├── requirements.txt # Python dependencies
├── Dockerfile # Docker build definition
├── Procfile # Deployment instructions (e.g. for Heroku)
├── runtime.txt # Runtime environment info (e.g. Python version)
├── /data # (Optional) Example or test images
├── /images # (Optional) Assets for UI
├── /saved_model # Pre-trained TensorFlow model
├── /templates # HTML templates for Flask
├── /static # Static files (CSS, JavaScript)
├── /uploads # Uploaded images storage
└── /utils # Helper modules (e.g., image preprocessing, model loading)
```
---

## Requirements

- Python 3.7 or higher
- Tensorflow (2.10.1)
- OpenCV (installed as `opencv-python`)
- Flask
- Optional: Streamlit (if using the Streamlit-based interface)

---

## Installation
1. Clone the repository:

   ```bash
   git clone https://github.com/steve1s/image-detection-with-flask.git
   cd image-detection-with-flask
   ```

2. Create and activate a virtual environment:
     ```bash
     python3 -m venv venv
     source venv/bin/activate    # on Uinx/MacOS
     #or
     venv\Scripts\activate      #on Windows
     ```
3. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage
Local Python Server

Start the Flask app:
   ``` bash
   python app.py
   ```
By default, the app runs on http://127.0.0.1:5000 . Visit that in your browser to upload images and view detections.
Optionally, try the streamlit interface:
   ```bash
   python app_streamlit.py
   ```

---
## Docker

Build and run via Docker:
   ```bash
   docker build -t flask-tf-app .
   docker run -p 5000:5000 flask-tf-app
   ```
Then navigate to http://localhost:5000 .
---
## Deployment

You can delpoy this app to hosting sevices like Heroku, or others supporting Docker or python apps. This include Procfile and runtime.txt may help with platforms like Heroku.

---

## Customising or Training your own Model
Want to swap the model or train your own?
1. Place your saved TensorFlow model in the ```bash saved_model/``` directory.
2. Update the model-loading logic to load and run inference on your model.
3. Adjust any preprocessing or postprocesing routines accordingly. (eg, via ```bash utils/ or in app.py ``` ).
