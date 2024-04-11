# Use an official Python runtime as a parent image
FROM nageshbhad/opencv-python310:latest

# Set working directory in the container
WORKDIR /app

# Add application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Add application files
COPY . .

# Run the application
CMD ["python3", "SLT_API.py"]