from flask import Flask, abort, render_template
from jinja2.exceptions import TemplateNotFound

from .lisp import views as lisp_views
from .python import views as python_views

app = Flask(__name__)
app.register_blueprint(python_views.python, url_prefix='/python')
app.register_blueprint(lisp_views.lisp, url_prefix='/lisp')


@app.route('/')
def index():
    try:
        return render_template('pages/index.tmpl.html', active='home')

    except TemplateNotFound:
        abort(404)


@app.errorhandler(404)
def not_found(error):
    return render_template('pages/errors/404.tmpl.html', active='home'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('pages/errors/500.tmpl.html', active='home'), 500


if __name__ == '__main__':
    app.run()
