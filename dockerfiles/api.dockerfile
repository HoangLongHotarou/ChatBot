FROM python

WORKDIR /api

COPY ./ChatBot/requirements.txt .

RUN pip install --no-cache-dir -r /api/requirements.txt

COPY ./ChatBot .

CMD [ "sh","-c","python manage.py migrate;python manage.py collectstatic; gunicorn chatbot.wsgi -b 0.0.0.0:8000" ]

EXPOSE 8000
