import sqlite3

from flask import Blueprint, abort, render_template

from jinja2.exceptions import TemplateNotFound

import markdown

from ..db import open_db


python = Blueprint('python', __name__, template_folder='templates')


@python.route('/')
@python.route('/<int:chapter>')
def python_page(chapter: int = 1):
    try:
        with open_db() as cur:
            record = cur.execute('SELECT * FROM python_articles WHERE id=?', (chapter,)).fetchone()

            return render_template(
                f'pages/python/article.tmpl.html',
                active=f'python: {chapter}',
                title=record[1],
                content=markdown.markdown(record[2]),
                date=record[3],
            )

    except (TypeError, TemplateNotFound, sqlite3.OperationalError):
        abort(404)
