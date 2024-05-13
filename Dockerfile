FROM python:3.12

WORKDIR /app

# Set up the requirements
COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

# To fix a Django install bug
ENV PYTHONUNBUFFERED=1
