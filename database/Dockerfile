# Use Python 3.11 as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code to the container
COPY . /app/

# Specify the command to run your application
CMD ["python", "launch.py"]
