FROM ubuntu:22.04
# EC2의 우분투 버전과 통일

RUN apt-get -y update
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip
# pip 설치


### 데이터베이스 연결 부분 ###
RUN apt-get install libmysqlclient-dev -y
# for MySQLclient (이거 설치 안되면 mysqlclient 설치 시 오류 발생)


### 모델 연결 부분 ###
RUN apt-get update && apt-get install -y git
RUN pip install git+https://github.com/openai/CLIP.git
RUN pip install ftfy regex tqdm spotipy


### 장고 모듈 설치 부분 ###
RUN mkdir /config
ADD /config/requirements.txt /config/
RUN pip3 install --no-cache-dir -r /config/requirements.txt
# requirements.txt 실행

EXPOSE 8000