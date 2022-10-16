# syntax=docker/dockerfile:1
FROM python:3.10-slim@sha256:502f6626d909ab4ce182d85fcaeb5f73cf93fcb4e4a5456e83380f7b146b12d3

# Serves for both LSP and test runner. Assuming relaton-py as pwd.
#
# For LSP purposes, mount `pwd` under `pwd` and set workdir to it:
# (`--workdir="$(pwd)" --volume="$(pwd):$(pwd):z"`)
#
# For test runner purposes, mount `pwd` under /code
# and pass `coverage` as the command (see Makefile)

ENV PYTHONUNBUFFERED=1

RUN ["python", "-m", "pip", "install", "--upgrade", "pip"]

RUN pip install "python-lsp-server[all]" pylsp-mypy

COPY requirements.txt /code/requirements.txt
COPY requirements_dev.txt /code/requirements_dev.txt

WORKDIR /code

RUN ["pip", "install", "-r", "requirements_dev.txt"]
RUN ["pip", "install", "-r", "requirements.txt"]

CMD ["pylsp"]
