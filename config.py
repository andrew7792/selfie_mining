from flask import Flask
from flask_sqlalchemy import SQLAlchemy


DB_USERNAME = 'selfiuser'
DB_PASSWORD = 'password'
# DB_HOST = '192.168.2.85'
DB_HOST = 'localhost'
DB_NAME = 'instagram_selfi'


config = {'DB_USERNAME': DB_USERNAME,
          'DB_PASSWORD': DB_PASSWORD,
          'DB_HOST': DB_HOST,
          'DB_NAME': DB_NAME}

app = Flask('selfiapp')
app.url_map.strict_slashes = False
# app.debug = True

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://' + config['DB_USERNAME'] + ':' + \
                                        config['DB_PASSWORD'] + '@' + \
                                        config['DB_HOST'] + '/'+ config['DB_NAME'] + '?charset=utf8mb4&binary_prefix=true'

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SECRET_KEY"] = "appsecretkey_dfgdfgdg345#ddf#ysdfg_selfisecretkey"

app.config['IMAGES_FOLDER'] = "/store/assets"

db = SQLAlchemy(app=app, engine_options={ 'connect_args': { 'connect_timeout': 28800 }})