# Distroless runs python 3.9.2
FROM python:3.11-slim-bullseye as python-base
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

# use distroless/cc as the base for our final image
# lots of python depends on glibc
FROM gcr.io/distroless/cc-debian11

# Copy python from the python-builder
# this carries more risk than installing it fully, but makes the image a lot smaller
COPY --from=python-base /usr/local/lib/ /usr/local/lib/
COPY --from=python-base /usr/local/bin/python /usr/local/bin/python
COPY --from=python-base /etc/ld.so.cache /etc/ld.so.cache

# Add some common compiled libraries
# If seeing ImportErrors, check if in the python-base already and copy as below
# required by lots of packages - e.g. six, numpy, wsgi
# *-linux-gnu makes this builder work with either linux/arm64 or linux/amd64
COPY --from=python-base /lib/*-linux-gnu/libz.so.1 /lib/libs/
COPY --from=python-base /usr/lib/*-linux-gnu/libffi* /lib/libs/
COPY --from=python-base /lib/*-linux-gnu/libexpat* /lib/libs/

# Copy over the app
COPY --from=python-base /app /app
COPY --from=python-base /dpkg /
WORKDIR /app

# Add /lib/libs to our path
ENV LD_LIBRARY_PATH="/lib/libs:${LD_LIBRARY_PATH}" \
# Add the app path to our path
    PATH="/app/bin:${PATH}" \
# Add the app path to your python path
    PYTHONPATH="/app:${PYTHONPATH}" \
# standardise on locale, don't generate .pyc, enable tracebacks on seg faults
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1

CMD ["python", "/app/main.py"]
