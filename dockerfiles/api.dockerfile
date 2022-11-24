FROM python:3.9.15

WORKDIR /chatbot

COPY ./chatbot/requirements.txt .

RUN pip install --no-cache-dir -r /chatbot/requirements.txt

COPY ./chatbot .

CMD [ "sh","-c","python manage.py migrate;python manage.py collectstatic; gunicorn chatbot.wsgi -b 0.0.0.0:8000" ]

EXPOSE 8000
