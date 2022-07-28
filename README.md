# 8de backend server
* The backend repository of Recommade.
* You can check our backend API.


## 1. Prerequisites
* Docker installation required.


## 2. Getting started
### 1) git clone
```sh
$ git clone https://github.com/Silicon-Valley-Team-A/server.git
$ docker-compose up
```

### 2) Modify server/key.json
 * We use Spotify API so you should get a Spotify API key and change key.json into your key.
 * key.json locates in the directory 'server/', which contains manage.py

### 3) Modify internal host in settings.py
 * If you don't run our project in local environment, you should change the last line of server/server/settings.py
```python
INTERNAL_HOST_IP = 'http://your_ip_address'
```

### 4) Add moodmodel
 * To run a model, you should add **moodmodel_keras_2.h5** file in server/model/
 * You can download it at [AI repository](https://github.com/Silicon-Valley-Team-A/AI)

### 5) Modify docker-compose.yml(Optional)
 * If you **only want to check backend API** and **didn't clone client repository**, you should make client container(from line 33 to 46) comment in docker-compose.yml
```yml
# Comment these lines
      - client
      
  client:
    image: node:18
    container_name: re01
    working_dir: /client
    command: bash -c "
        yarn install &&
        yarn build"
    # command: sh entrypoint.sh
    volumes:
      - ./client/:/client
    depends_on:
      - db
```

### 6) Docker image build
 * Make sure that your Docker is running.
 * Check your ports: 80, 3306, and 8000 must be unused before build.
```sh
$ docker-compose up
```

### 7) When the build is finished, you can check our API at http://localhost
 * No views provided.
 * You can check our API with [Postman](https://web.postman.co/)
 
 
## 3. API Specification
 * Get playlist from image - POST /api/music
 * Save playlist - POST /api/save
 * Get all playlists the user created(login required) - POST /api/playlist
 * Get one playlist GET /api/playlist/<int:playlist_id>
 * Get CSRFToken - GET /api/csrf_cookie
 * Sign up - POST /api/register
 * Sign in - POST /api/login
 * Sign out - POST /api/logout
 * Check if the user is authenticated - GET /api/authenticated
 * [API Specification document(written in Korean)](https://guiltless-canary-64b.notion.site/API-117910e92050409e907e4dd768a1a072)


## 4. Teck stack
* Backend
  * Django
  * MySQL
  * Django Rest Framework
  * CORSHeader

* DevOps
  * Nginx
  * Gunicorn
  * Docker, docker-compose
  * AWS EC2
  
* OpenAPI
  * Spotify API - To search music and get music information.


## 5. Copyrights / End User Licesnse
This project is not intended for commercial use, please do not use it for commercial purposes.
