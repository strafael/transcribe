FROM python:3.9-slim-bullseye

RUN python -m venv venv \
 && venv/bin/pip install --upgrade pip

COPY src/transcribe/__init__.py /src/transcribe/__init__.py
COPY setup.py setup.cfg /
RUN venv/bin/pip install -e .[dev]

COPY main.py /
COPY src/ /src
COPY tests/ /tests

ENTRYPOINT ["venv/bin/python", "main.py"]
