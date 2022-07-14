# How to getting start the 8de backend server
* Docker installation required.

## 1. git clone
 ```
 git clone https://github.com/Silicon-Valley-Team-A/server.git
 ```

## 2. Insert key.json in the directory 'server', which contains manage.py
 * example of key.json.
 ```
{
    "SECRET_KEY":"secret_key",
    "CLIENT_ID":"client_id",
    "CLIENT_SECRET":"client_secret"
}
 ```

## 3. Docker image build
 * Make sure that your Docker is running.
 * Check your ports: 80, 3306, and 8000 must be unused before build.
 ```
 docker-compose up --build
 ```

## 4. When the build is finished, go to https://127.0.0.1
[https://127.0.0.1](https://127.0.0.1)

## Error Handling
 * 최초 빌드 시 dg01 컨테이너를 실행하면서 장고-mysql 연결하는 동안 2003에러가 발생합니다.
 * dg01 컨테이너를 재시작하면 사라지는 오류이며. 원인 파악 중입니다.