# FROM tiangolo/uvicorn-gunicorn:python3.11-slim
FROM python:3.9.13-slim

WORKDIR /code
RUN pip install poetry

COPY ./poetry.lock ./pyproject.toml ./config.yaml /code/
RUN poetry install --no-root
    
COPY ./src /code/src
ENV PYTHONPATH "${PYTHONPATH}:/code/src"

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0"]