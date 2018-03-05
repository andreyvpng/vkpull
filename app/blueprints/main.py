from random import choice
from string import ascii_letters
from functools import wraps
from flask import Blueprint, redirect, render_template, session, abort, request, url_for, flash
from app.db_helper import get_polls_of_user, get_poll_via_url, get_poll_via_id, get_possible_choice, create_new_poll, \
	create_choice, is_user_take_part, delete_poll, is_url_available

main = Blueprint('main', __name__)


def is_logged(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if not session.get('logged_in'):
			flash('Ты не авторизирован!')
			return redirect(url_for('main.index'))
		return func(*args, **kwargs)
	return wrapper


@main.route('/')
def index():
	polls = None
	if session.get('logged_in'):
		polls = get_polls_of_user(session.get('user_id'))
	return render_template('index.html', polls=polls)


@main.route('/add_poll', methods=['GET', 'POST'])
@is_logged
def add_poll():
	if request.method == "POST":
		while True:
			url_of_poll = ''.join(choice(ascii_letters) for _ in range(30))
			if is_url_available(url_of_poll):
				break
		choices = request.form.getlist('choice')
		create_new_poll(url_of_poll, session['user_id'], request.form['title'], choices)
		return redirect(url_for('main.show_poll', url_of_poll=url_of_poll))
	return render_template('add_poll.html')


@main.route('/del_poll_<poll_id>', methods=['POST'])
@is_logged
def dell_poll(poll_id):
	poll = get_poll_via_id(poll_id)
	if poll.get('user_id') == session.get('user_id'):
		delete_poll(poll_id)
	else:
		flash('У тебя нет прав на удаление этого опроса!')
	return redirect(url_for('main.index'))


@main.route('/poll_<url_of_poll>')
def show_poll(url_of_poll):
	poll = get_poll_via_url(url_of_poll)
	if not poll:
		abort(404)

	options = get_possible_choice(poll['id'])
	user_choice = is_user_take_part(session['user_id'], options)
	return render_template('poll.html', poll=poll, options=options, user_choice=user_choice)


@main.route('/make_choice', methods=['POST'])
@is_logged
def make_choice():
	poll_id = request.form.get('poll_id')
	choice_id = request.form.get('choice_id')

	options = get_possible_choice(poll_id)
	user_choice = is_user_take_part(session['user_id'], options)

	if not user_choice['answered']:
		create_choice(session['user_id'], poll_id, choice_id)
	return redirect(url_for('main.show_poll', url_of_poll=request.form.get('poll_url')))