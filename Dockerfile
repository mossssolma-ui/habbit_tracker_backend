FROM python:3.13-slim

WORKDIR /habits

RUN pip install poetry==2.4.1

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --only main

COPY . .

RUN mkdir -p /habits/media
RUN mkdir -p /habits/staticfiles

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]