# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# install system dependencies for Opencv
#RUN apt-get update && apt-get install -y libgl1
# RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0


# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Force TensorFlow to use CPU only
ENV CUDA_VISIBLE_DEVICES="-1"

# Create uploads directory
RUN mkdir -p uploads

# Expose Flask port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
