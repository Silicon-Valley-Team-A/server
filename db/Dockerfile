FROM mysql:8.0.22

ENV MYSQL_DATABASE=8dedb \
    MYSQL_ROOT_PASSWORD=8de

# 스키마 설정
ADD ./db/init.sql /docker-entrypoint-initdb.d

EXPOSE 3306
