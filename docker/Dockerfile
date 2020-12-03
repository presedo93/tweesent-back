# For more information, please refer to https://aka.ms/vscode-docker-python
FROM pytorch/pytorch:latest

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
ADD requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /backend
ADD . /backend

RUN mkdir assets/ && ./scripts/download_model

EXPOSE 5000

# During debugging, this entry point will be overridden.
CMD [ "uvicorn", "--host", "0.0.0.0", "--port", "5000", "app:app" ]
