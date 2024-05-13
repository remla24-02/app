FROM python:3.12

# Set up the requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# To fix a Django install bug
ENV PYTHONUNBUFFERED=1
