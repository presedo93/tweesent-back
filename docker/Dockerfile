FROM python:3.9-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Labels the NVIDIA GPUs
LABEL com.nvidia.volumes.needed=nvidia_driver

# Create and use an USER and add to the PATH
RUN useradd -ms /bin/bash back
USER back
ENV PATH="/home/back/.local/bin:${PATH}"

# Install pip requirements
ADD requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Set the work directory and add the code
WORKDIR /backend
ADD . /backend

# The backend port for HTTP and WebSockets comms.
EXPOSE 8000

CMD [ "uvicorn", "--host", "0.0.0.0", "app:app" ]
