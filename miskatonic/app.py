from flask import Flask, g, abort, render_template
from flask_login import LoginManager
from jinja2.exceptions import TemplateNotFound

from .config import Config
from .models import Article, Category, Person
from .apps.lisp.views import lisp
from .apps.admin.views import admin
from .apps.python.views import python

app = Flask(__name__)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(lisp, url_prefix='/lisp')
app.register_blueprint(python, url_prefix='/python')

login = LoginManager()
login.init_app(app)

app.config['SECRET_KEY'] = Config.SECRET_KEY


@app.before_request
def before_request():
    g.db = Config.db
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@login.user_loader
def load_user(uid):
    return Person.select().where(Person.id == int(uid)).first()


@app.errorhandler(401)
def not_found(error):
    """
    Generic 401 server error view
    """
    return render_template('pages/errors/401.tmpl.html', active='home'), 401


@app.errorhandler(404)
def not_found(error):
    """
    Generic 404 server error view
    """
    return render_template('pages/errors/404.tmpl.html', active='home'), 404


@app.errorhandler(500)
def internal_server_error(error):
    """
    Generic 500 server error view
    """
    return render_template('pages/errors/500.tmpl.html', active='home'), 500


@app.route('/')
def index():
    try:
        return render_template('pages/index.tmpl.html', active='home')

    except TemplateNotFound:
        abort(500)


if __name__ == '__main__':
    with Config.db:
        Config.db.create_tables([Category, Article, Person])

    app.run()
