FROM python:3.10-slim

COPY Docker/rootfs /
RUN apt-get update && \
    apt-get install -y --no-install-recommends procps curl git && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r /requirements.txt && \
    rm -rf /requirements.txt

CMD ["/app/main.py"]
