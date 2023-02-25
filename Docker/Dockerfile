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

# Install some apt dependencies to /dpkg to copy over
RUN cd /tmp && \
    apt-get update && \
    apt-get download $(apt-cache depends --recurse --no-recommends --no-suggests \
    --no-conflicts --no-breaks --no-replaces --no-enhances \
    --no-pre-depends git | grep -v libc | grep "^\w") libcurl3-gnutls && \
    mkdir /dpkg && \
    for deb in *.deb; do dpkg --extract $deb /dpkg || exit 10; done

# final image based on distroless with glibc for git
FROM gcr.io/distroless/cc-debian11

# Copy over the app
COPY --from=builder /app/dist/cookiecutter-static /cookiecutter
# Copy over our unpacked dpkgs to get git
COPY --from=builder /dpkg /
# COPY over some required libraries
COPY --from=builder /lib/*-linux-gnu/libcom_err.so.2 /lib/libs/
COPY --from=python-base /usr/lib/*-linux-gnu/libffi* /lib/libs/
COPY --from=python-base /lib/*-linux-gnu/libexpat* /lib/libs/


# Add /lib/libs to our path
ENV LD_LIBRARY_PATH="/lib/libs:${LD_LIBRARY_PATH}"

ENTRYPOINT ["/cookiecutter"]
