FROM python:3.10-alpine

RUN apk add --no-cache --virtual .build-deps gcc musl-dev python3-dev libffi-dev openssl-dev
WORKDIR myproject
COPY . .
RUN apk add --no-cache mariadb-connector-c-dev build-base
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install mysqlclient==2.1.0
ENV DJANGO_SETTINGS_MODULE=myproject.settings
ENV DATABASE_URL=mysql://user:password@/database
ENV TZ=Asia/Taipei
EXPOSE 8080
CMD ["python", "manage.py", "migrate"]
CMD ["gunicorn", "myproject.wsgi", "--bind", "0.0.0.0:8080", "--workers", "3"]