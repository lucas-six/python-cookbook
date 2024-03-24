# Deploy App with Docker

## Recipes

```bash
pipenv requirements --exclude-markers --dev > requirements.txt
sed -i "1d" requirements.txt
```

```Dockerfile
# syntax=docker/dockerfile:1
FROM python:3.11

ARG PYPI_INDEX_URL=https://pypi.org/simple
ARG PYPI_TRUST_HOST=pypi.org
ARG PYPI_TIMEOUT=300

# ENV PYTHONUNBUFFERD 1

WORKDIR /app

COPY . .
RUN pip install \
    -i ${PYPI_INDEX_URL} \
    --trusted-host ${PYPI_TRUST_HOST} \
    --disable-pip-version-check \
    --no-cache \
    --retries 2 \
    --timeout ${PYPI_TIMEOUT} \
    -r requirements.txt
RUN python -m black . \
    && python -m isort . \
    && python -m mypy . \
    && python -m pylint .
```

OR

```Dockerfile
# syntax=docker/dockerfile:1
FROM python:3.11-alpine

ARG PYPI_INDEX_URL=https://pypi.org/simple
ARG PYPI_TRUST_HOST=pypi.org
ARG PYPI_TIMEOUT=300

# ENV PYTHONUNBUFFERD 1

# Aliyun mirrors
#RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
#RUN apk update && apk add git curl
```

```bash
docker build --network=host -t <DOCKER-IMAGE-NAME> . --build-arg PYPI_INDEX_URL=<PYPI_INDEX_URL> --build-arg PYPI_TRUST_HOST=<PYPI_TRUST_HOST>
docker run --rm <DOCKER-IMAGE-NAME> /bin/sh -c echo lint finished
```
