from flask import Blueprint, abort, render_template

from jinja2.exceptions import TemplateNotFound


lisp = Blueprint('lisp', __name__, template_folder='templates')


@lisp.route('/')
@lisp.route('/<int:chapter>')
def lisp_page(chapter: int = 0):
    try:
        return render_template(f'pages/lisp/{chapter}.tmpl.html', active=f'lisp: {chapter}')

    except TemplateNotFound:
        abort(404)
