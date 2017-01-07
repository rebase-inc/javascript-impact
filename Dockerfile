FROM alpine

ARG PYTHON_COMMONS_HOST
ARG PYTHON_COMMONS_SCHEME
ARG PYTHON_COMMONS_PORT

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
        --trusted-host ${PYTHON_COMMONS_HOST} \
        --extra-index-url ${PYTHON_COMMONS_SCHEME}${PYTHON_COMMONS_HOST}:${PYTHON_COMMONS_PORT} \
        --requirement /requirements.txt

COPY ./run.py /

CMD ["/venv/bin/python", "-m", "run"]
