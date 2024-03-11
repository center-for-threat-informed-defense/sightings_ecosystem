# syntax=docker/dockerfile:1

# Note: due to '-f' target in the build command,
# all host filepaths are relative to the project root

FROM python:3.9-slim

# OCI labels
LABEL "org.opencontainers.image.title"="Sightings Pipeline"
LABEL "org.opencontainers.image.description"="Pipeline component of Sightings project"
LABEL "org.opencontainers.image.url"="https://ctid.mitre-engenuity.org/"

ENV APP_DIR /pipeline
ENV IN_CONTAINER 1
ENV PYTHONUNBUFFERED 1

# setup venv
RUN mkdir /${APP_DIR} && \
    python -m venv /${APP_DIR}/.venv && \
    /${APP_DIR}/.venv/bin/python -m pip install -U pip wheel setuptools

# add to path
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8 \
    PATH=/${APP_DIR}/.venv/bin:${PATH}

WORKDIR ${APP_DIR}

# Install dependencies
RUN curl -sSL https://install.python-poetry.org/ | python -
ENV PATH PATH:$HOME/.poetry/bin
COPY pyproject.toml poetry.lock ./
RUN poetry install --with pipeline
COPY src/pipeline/ .

# create unprivileged service account
RUN useradd -r -u 1002 sightings_pipeline
USER sightings_pipeline

CMD ["python", "pipeline.py", "-i", "/data"]
