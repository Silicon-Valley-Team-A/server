# 8de backend server
* Django, MySQL
* MySQL installation required.

## 1. git clone
 ```
 git clone https://github.com/Silicon-Valley-Team-A/server.git
 ```

## 2. Install requirements
 ```
 pip install -r requirements.txt
 ```

## 3. Move to server/settings.py and edit the database section
 * You can reference db.sql from lines 1-8 and 18-19.
 * It creates an example user and you don't need to edit setting.py if you execute them.

## 4. Go to django project and execute these commands in terminal
 ```
 python manage.py makemigrations account
 python manage.py migrate
 ```

## 5. Back to MySQL workbench and create tables
 * Execute db.sql from line 25.

## 6. Back to terminal and run Django Project
 ```
 cd server
 python manage.py runserver
 ```