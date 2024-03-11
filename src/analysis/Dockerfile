# syntax=docker/dockerfile:1
# Note: due to '-f' target in the build command,
# all host filepaths are relative to the project root

FROM python:3.9-slim

# OCI labels
LABEL "org.opencontainers.image.title"="Sightings Analysis"
LABEL "org.opencontainers.image.description"="Analysis component of Sightings project"
LABEL "org.opencontainers.image.url"="https://ctid.mitre-engenuity.org/"

ENV APP_DIR /analysis
ENV PYTHONUNBUFFERED 1

#ENV sighting_db_conn_str="postgresql://sightings:sightings@host.docker.internal:5432/sightings"

# setup venv
RUN mkdir /${APP_DIR} && \
    python -m venv /${APP_DIR}/.venv && \
    /${APP_DIR}/.venv/bin/python -m pip install -U pip wheel setuptools

# add to path
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8 \
    PATH=/${APP_DIR}/.venv/bin:${PATH}

WORKDIR ${APP_DIR}

RUN curl -sSL https://install.python-poetry.org/ | python -
ENV PATH PATH:$HOME/.poetry/bin
COPY pyproject.toml poetry.lock ./
RUN poetry install --with analysis
COPY src/analysis/ .

# create unprivileged service account
RUN useradd -r -u 1001 sightings_analysis
EXPOSE 8050
USER sightings_analysis

CMD ["python", "/analysis/sightings_dash.py"]
