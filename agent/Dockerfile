# Use a lightweight Python base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the agent script and requirements file into the container
COPY agent.py .
COPY executor.py .
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# The command to run when the container starts.
# Environment variables will be passed in at runtime.
CMD [ "python", "agent.py" ]
