import os
from urllib import parse


class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	VK_API_ID = os.environ.get('VK_API_ID')
	VK_API_SECRET = os.environ.get('VK_API_SECRET')
	VK_API_URL = os.environ.get('VK_API_URL')


class DevelopmentConfig(Config):
	DEBUG = True
	DATABASE_NAME = os.environ.get("DATABASE_NAME")
	DATABASE_USER = os.environ.get("DATABASE_USER")
	DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
	DATABASE_HOST = os.environ.get("DATABASE_HOST")
	DATABASE_PORT = os.environ.get("DATABASE_PORT")


class HerokuConfig(Config):
	parse.uses_netloc.append("postgres")
	url = parse.urlparse(os.environ.get("DATABASE_URL"))

	DEBUG = False
	DATABASE_NAME = url.path[1:]
	DATABASE_USER = url.username
	DATABASE_PASSWORD = url.password
	DATABASE_HOST = url.hostname
	DATABASE_PORT = url.port


config = {
	'development': DevelopmentConfig,
	'heroku': HerokuConfig
}
