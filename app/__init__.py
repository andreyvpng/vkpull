import os
from flask import Flask, g
from app.db_helper import init_db
from config import config

app = Flask(__name__)
app.config.from_object(config[os.environ.get('FLASK_CONFIG') or 'development'])


@app.cli.command('init_db')
def init_db_command():
	init_db(app)
	print('Initialized the database.')


@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'db'):
		g.db.close()


from app.blueprints.main import main as main_blueprint
app.register_blueprint(main_blueprint)
from app.blueprints.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')
