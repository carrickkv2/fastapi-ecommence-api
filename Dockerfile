# pull official base image
FROM python:3.10.8-slim-buster

# set working directory
WORKDIR /usr/src/fast_api

# Expose the required port
EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Add the current directory to the PYTHONPATH
RUN export PYTHONPATH="$PYTHONPATH:/usr/src/fast_api"

# install system dependencies
RUN apt-get update \
    && apt-get -y install netcat gcc \
    && apt-get clean

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . .

# Creates a non-root user with an explicit UID and adds permission to access the /fast_api folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /usr/src/fast_api
USER appuser
WORKDIR /usr/src/fast_api

# Run this during production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "app.main:app"]

# Run this during development
# CMD ["uvicorn", "app.main:app", "--reload", "--workers", "1", "--host", "0.0.0.0", "--port", "8000"]
