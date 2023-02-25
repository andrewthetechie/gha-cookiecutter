FROM python:3.11-slim-bullseye as builder
WORKDIR /app

# install build requirements
RUN apt-get update && apt-get install -y binutils patchelf upx build-essential scons
RUN pip install --no-warn-script-location --upgrade virtualenv pip pyinstaller staticx

# copy the app
COPY Docker/builder/rootfs/requirements.txt ./
COPY main.py ./

## build the app
# install requirements
RUN pip install -r requirements.txt
# pyinstaller package the app
RUN python -OO -m PyInstaller -F main.py --name cookiecutter
# static link the repo-manager binary
RUN cd ./dist && \
    staticx cookiecutter cookiecutter-static
# will be copied over to the scratch container, pyinstaller needs a /tmp to exist
RUN mkdir /app/tmp

# Install some apt dependencies
RUN cd /tmp && \
    apt-get update && \
    apt-get download $(apt-cache depends --recurse --no-recommends --no-suggests \
    --no-conflicts --no-breaks --no-replaces --no-enhances \
    --no-pre-depends git | grep -v libc | grep "^\w") libcurl3-gnutls && \
    mkdir /dpkg && \
    for deb in *.deb; do dpkg --extract $deb /dpkg || exit 10; done

# use distroless/cc as the base for our final image
# lots of python depends on glibc
FROM scratch

# Copy python from the python-builder
# this carries more risk than installing it fully, but makes the image a lot smaller
COPY --from=builder /usr/local/lib/ /usr/local/lib/
COPY --from=builder /usr/local/bin/python /usr/local/bin/python
COPY --from=builder /etc/ld.so.cache /etc/ld.so.cache

# Add some common compiled libraries
# If seeing ImportErrors, check if in the builder already and copy as below
# required by lots of packages - e.g. six, numpy, wsgi
# *-linux-gnu makes this builder work with either linux/arm64 or linux/amd64
COPY --from=builder /lib/*-linux-gnu/libz.so.1 /lib/libs/
COPY --from=builder /lib/*-linux-gnu/libcom_err.so.2 /lib/libs/
COPY --from=builder /usr/lib/*-linux-gnu/libffi* /lib/libs/
COPY --from=builder /lib/*-linux-gnu/libexpat* /lib/libs/

# Copy over the app
COPY --from=builder /app/dist/cookiecutter-static /cookiecutter
COPY --from=builder /dpkg /
# Setup a tmp directory on scratch, used by the pyinstaller bootstrap
COPY --from=builder /app/tmp /tmp

# Add /lib/libs to our path
ENV LD_LIBRARY_PATH="/lib/libs:${LD_LIBRARY_PATH}" \
    PATH=/bin:/usr/bin:$PATH

ENTRYPOINT ["/cookiecutter"]
