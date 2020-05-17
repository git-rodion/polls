FROM python:3.8
WORKDIR /usr/src/app
COPY requirements.txt .
RUN python -m pip install --requirement requirements.txt && rm requirements.txt
COPY source /usr/src/app