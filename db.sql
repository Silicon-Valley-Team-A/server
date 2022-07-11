# 스키마 생성
CREATE SCHEMA `8dedb`;

# 사용자 생성
use mysql; create user 'user'@'%' identified by '1234';

# 권한 부여
grant all privileges on 8dedb.* to 'user'@'%'; # django migration 진행할 때 무조건 설정해주어야 함

# django migration 진행: 
# 터미널에서
# python manage.py makemigrations account
# python manage.py migrate

# 보안을 위한 권한 수정
# grant select, insert, update, delete on 8dedb.* to 'user'@'%';

# 8dedb 돌아오기
use 8dedb;

# 여기까지 장고에서 mysql을 돌리기 위해 필요한 환경설정.



# 테이블 생성
CREATE table song(
id varchar(50), # spotify에서 제공하는 노래 id
title varchar(200), # 노래 제목
artist varchar(50), # 가수
duration int, # 재생 시간 프론트분들이 요청하신 요소는 아니라서 빠질 가능성이 있습니다.
file varchar(500), # 미리듣기 파일 경로
title_album varchar(200), # 앨범 제목
image_album varchar(500), # 앨범 이미지 경로
PRIMARY KEY(id)	
);

CREATE table playlist(
id int auto_increment,
user_id bigint, # int형으로 수정, 플레이리스트 생성한 사용자
name varchar(50), # 플레이리스트 이름
tag varchar(50), # 모델이 인식한 키워드 혹은 장르로 채울 예정
PRIMARY KEY(id),
FOREIGN KEY(user_id) references user(id) # email 참조하면 오류나서 id로 수정
);

CREATE table songlist(
id int auto_increment,
playlist_id int, # 어떤 플레이리스트의
song_id varchar(50), # 어떤 노래가
PRIMARY KEY(id),
FOREIGN KEY(playlist_id) references playlist(id),
FOREIGN KEY(song_id) references song(id)
);

CREATE TABLE category (
id int auto_increment,
keyword VARCHAR(50), # 모델에서 받은 키워드
genre VARCHAR(50), # 프론트에서 받은 장르
danceability FLOAT, # 춤 추기에 적합한가? 0.0 - 1.0 범위이며 값이 클 수록 춤추기 좋음
energy FLOAT, # 에너지의 정도. 0.0 - 1.0 범위, 빠르고 화려하고 노이즈가 많은 음악일수록 값이 큼
valence FLOAT, # 음원의 밝음 정도. 0.0 - 1.0 범위, 밝고 행복하고 기쁘면 값이 높고 반대로 슬프고 화나고 우울하면 값이 낮음.
tempo FLOAT, # 템포, beats per minute(BPM)
PRIMARY KEY (id)
);