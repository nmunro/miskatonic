from flask import Flask, g, abort, render_template
from jinja2.exceptions import TemplateNotFound

from .db import db, create_tables
from .config import Config
from .modules.lisp.views import lisp
from .modules.python.views import python

app = Flask(__name__)
app.register_blueprint(lisp, url_prefix='/lisp')
app.register_blueprint(python, url_prefix='/python')


@app.before_request
def before_request():
    g.db = Config().db
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.errorhandler(404)
def not_found(error):
    return render_template('pages/errors/404.tmpl.html', active='home'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('pages/errors/500.tmpl.html', active='home'), 500


@app.route('/')
def index():
    try:
        return render_template('pages/index.tmpl.html', active='home')

    except TemplateNotFound:
        abort(500)


if __name__ == '__main__':
    create_tables()
    app.run()
