FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 7860

CMD ["gunicorn", "--bind", "0.0.0.0:7860", "smartfarm_project.wsgi:application"]