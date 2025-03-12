import os
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()

class Config():
     SECRET_KEY = 'mysecretkey'



class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST =  os.getenv('DATABASE_HOST2')
    MYSQL_USER = os.getenv('USER_DATABASE2')
    MYSQL_PASSWORD = os.getenv('PASSWORD_DATABASE2')
    MYSQL_DB = os.getenv('DATABASE_NAME2')
    MYSQL_DB1 = os.getenv('DATABASE_NAME12')
    MYSQL_PORT = 3306
    print(MYSQL_DB1)
    # SQLALCHEMY_DATABASE_URI = f'mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
    SQLALCHEMY_DATABASE_URI1 = f'mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB1}'
    
    
   


config = {
    'development': DevelopmentConfig
}