ARG GIT_VERSION="2.36.1"

# Distroless runs python 3.9.2
FROM python:3.9.2-slim as builder-base
ARG GIT_VERSION

RUN apt-get update && apt-get -y install wget unzip libz-dev libssl-dev libcurl4-gnutls-dev libexpat1-dev gettext cmake gcc libssh2-1-dev autoconf tcl-dev gettext
ADD https://github.com/git/git/archive/refs/tags/v$GIT_VERSION.zip /git.zip
RUN unzip /git.zip && \
    mkdir /git-static

# Distroless runs python 3.9.2
FROM builder-base as builder
ARG GIT_VERSION

ADD Docker/rootfs /
ADD main.py /app/main.py
ADD action.yml /app/action.yml


RUN cd /git-$GIT_VERSION && \
     make configure && \
    ./configure prefix=/git-static CFLAGS="${CFLAGS} -static" && \
    make && \
    make install
WORKDIR /app

# We are installing a dependency here directly into our app source dir
RUN pip install --target=/app -r /requirements.txt



# A distroless container image with Python and some basics like SSL certificates
# https://github.com/GoogleContainerTools/distroless
FROM gcr.io/distroless/python3
COPY --from=builder /app /app
COPY --from=builder /git-static /
WORKDIR /app
ENV PYTHONPATH /app
CMD ["/app/main.py"]


# FROM python:3.10-slim

# COPY Docker/rootfs /
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends procps curl git && \
#     rm -rf /var/lib/apt/lists/* && \
#     pip install --no-cache-dir -r /requirements.txt && \
#     rm -rf /requirements.txt

# CMD ["/app/main.py"]
