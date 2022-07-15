FROM ubuntu:22.04
# EC2의 우분투 버전과 통일

RUN apt-get -y update
RUN apt-get install -y python3-pip
# pip 설치

RUN apt-get install libmysqlclient-dev -y
# for MySQLclient (이거 설치 안되면 mysqlclient 설치 시 오류 발생)

RUN apt-get install curl -y
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash
RUN apt-get install -y nodejs
# react 실행을 위한 nodejs, npm 설치

RUN pip3 install --upgrade pip

# 컨테이너 내부에 config(설정파일)가 들어갈 폴더 생성
RUN mkdir /config
ADD /config/requirements.txt /config/
RUN pip3 install --no-cache-dir -r /config/requirements.txt
# requirements.txt 실행

### 작업 디렉토리 ###
# 소스코드가 들어갈 폴더 생성
RUN mkdir /src;
ADD . /src
WORKDIR /src

# react 실행
# WORKDIR /src/client
# RUN npm install --global yarn
# RUN yarn install
# RUN yarn build

EXPOSE 3000