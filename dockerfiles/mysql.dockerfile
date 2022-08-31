FROM mysql:latest

WORKDIR /var/lib/mysql

COPY ./data_mysql .

