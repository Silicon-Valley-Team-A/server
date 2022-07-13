FROM ubuntu:22.04
# EC2의 우분투 버전과 통일

RUN apt-get -y update
RUN apt-get install -y python3-pip
# pip 설치

RUN apt-get install libmysqlclient-dev -y
# for MySQLclient (이거 설치 안되면 mysqlclient 설치 시 오류 발생)

RUN pip3 install --upgrade pip
RUN pip3 install Django gunicorn
# gunicorn 설치(requirement.txt에 끼워넣어도 괜찮음)

# 컨테이너 내부에 config(설정파일)가 들어갈 폴더 생성
RUN mkdir /config
ADD /config/requirements.txt /config/
RUN pip3 install --no-cache-dir -r /config/requirements.txt
# requirements.txt 실행

### 작업 디렉토리 ###
# Django 소스코드가 들어갈 폴더 생성
RUN mkdir /src;

# 작업 디렉토리 src/server/server(manage.py 있는 곳)로 변경
WORKDIR /src/server/server