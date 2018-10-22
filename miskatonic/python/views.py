from flask import Blueprint, abort, render_template

from jinja2.exceptions import TemplateNotFound


python = Blueprint('python', __name__, template_folder='templates')


@python.route('/')
@python.route('/<int:chapter>')
def python_page(chapter: int = 0):
    try:
        return render_template(f'pages/python/{chapter}.tmpl.html', active=f'python: {chapter}')

    except TemplateNotFound:
        abort(404)
