FROM python:3.11

WORKDIR /usr/src/app

COPY requirements.txt .

ARG DATABASE_URL

ENV DATABASE_URL=${DATABASE_URL}

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p staticfiles

ENV USE_SQLITE=true

RUN python manage.py collectstatic --noinput

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "bjumper_test.wsgi:application"]