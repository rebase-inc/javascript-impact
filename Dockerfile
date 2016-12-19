FROM alpine

ARG PYPI_SERVER_HOST
ARG PYPI_SERVER_SCHEME
ARG PYPI_SERVER_PORT

COPY ./requirements.txt /requirements.txt

RUN apk --quiet update && \
    apk --quiet add \
        --no-cache \
        ca-certificates \
        python3 && \
    pyvenv /venv && \
    source /venv/bin/activate && \
    pip --quiet install \
        --no-cache-dir \
        --trusted-host ${PYPI_SERVER_HOST} \
        --extra-index-url ${PYPI_SERVER_SCHEME}${PYPI_SERVER_HOST}:${PYPI_SERVER_PORT} \
        --requirement /requirements.txt

COPY ./run.py /

CMD ["/venv/bin/python", "-m", "run"]
