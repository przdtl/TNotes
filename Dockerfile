FROM python:3.10

WORKDIR /app

ENV PYTHONPATH="$PYTHONPATH:/app"

# copy and install requirements modules
COPY ./requirements.txt .

RUN pip install  --no-cache-dir --upgrade -r requirements.txt

# copy project folders and files
COPY ./.env /app

COPY ./alembic.ini /app

COPY ./migrations /app/migrations

COPY ./src /app/src

# run script
CMD ["python3", "src/main.py"]