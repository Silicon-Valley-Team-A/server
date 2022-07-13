FROM mysql:8.0.22

# 작업 디렉토리 내에 db 생성
RUN mkdir /db
ADD /db/init.sql /db/

# 스키마 설정
ADD ./db/init.sql /docker-entrypoint-initdb.d/