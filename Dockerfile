# Distroless runs python 3.9.2
FROM python:3.9.2-slim as builder
ADD Docker/builder/rootfs /
ADD main.py /app/main.py
ADD action.yml /app/action.yml

# We are installing a dependency here directly into our app source dir
RUN pip install --target=/app -r /requirements.txt
RUN cd /tmp && \
    apt-get update && \
    apt-get download $(apt-cache depends --recurse --no-recommends --no-suggests \
    --no-conflicts --no-breaks --no-replaces --no-enhances \
    --no-pre-depends git | grep -v libc | grep "^\w") libcurl3-gnutls && \
    mkdir /dpkg && \
    for deb in *.deb; do dpkg --extract $deb /dpkg || exit 10; done

# A distroless container image with Python and some basics like SSL certificates
# https://github.com/GoogleContainerTools/distroless
FROM gcr.io/distroless/python3:debug
COPY --from=builder /app /app
COPY --from=builder /dpkg /
WORKDIR /app
ENV PYTHONPATH /app
CMD ["/app/main.py"]
