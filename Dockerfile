# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim
EXPOSE 80

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip3 install --upgrade pip
RUN pip install -e .[all]

# Run the web service on container startup. Here we use the uvicorn
# webserver, with four worker processes
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.

CMD ["uvicorn", "recommender_engine.main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "4"]

