#FROM python:3.14-slim
#
#ENV POETRY_VERSION=1.8.2
#RUN pip install "poetry==%POETRY_VERSION"
#
#WORKDIR /app
#
#COPY pyproject.toml poetry.lock ./
#
#RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi
#
#COPY services/ ./services/
#
#EXPOSE 8080
#
#CMD ["python", "-m", "services.api.src.main"]