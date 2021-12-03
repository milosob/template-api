FROM ubuntu:latest
WORKDIR /app
COPY . .
COPY requirements.txt requirements.txt
RUN apt update -y && \
    apt install -y python3.9-venv python3-distutils
RUN python3 -m venv venv && \
    . ./venv/bin/activate && \
    python -m pip install -e .
ENV PATH="/app/venv/bin:${PATH}"
ENTRYPOINT app --config-path /config.json
