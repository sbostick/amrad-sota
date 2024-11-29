########################################################################
FROM python:3.11-alpine3.18 as builder
RUN mkdir /app
COPY src /app
WORKDIR /app
COPY requirements.txt ./
ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV /venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN apk add build-base musl-dev linux-headers
RUN python -m venv $VIRTUAL_ENV \
    && pip install wheel \
    && pip install -r requirements.txt


########################################################################
FROM python:3.11-alpine3.18

# Embed the app version into the image
ARG APP_VERSION
ENV APP_VERSION=$APP_VERSION

# Embed the build timestamp into the image
ARG BUILD_TIME
ENV BUILD_TIME=$BUILD_TIME

# Bootstrap environment
ENV TERM="xterm"
ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV /venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY --from=builder /venv /venv
COPY --from=builder /app /app
COPY files/root/* /root
COPY files/home/app-server/* /home/app-server

RUN echo "Final provisioning" \
    && echo "Etc/UTC" > /etc/timezone \
    && addgroup --gid 1000 --system app-server \
    && adduser --system --shell /bin/sh --ingroup app-server --uid 1000 app-server \
    && chown -R app-server:app-server /venv /app /home/app-server

WORKDIR /app
USER app-server
CMD ["./main.py", "--project", "foo", "--self-test", "42"]
