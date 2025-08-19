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
