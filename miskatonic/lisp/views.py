import sqlite3

from flask import Blueprint, abort, render_template

from jinja2.exceptions import TemplateNotFound

import markdown

from ..db import open_db


lisp = Blueprint('lisp', __name__, template_folder='templates')


@lisp.route('/')
@lisp.route('/<int:chapter>')
def lisp_page(chapter: int = 1):
    try:
        with open_db() as cur:
            record = cur.execute('SELECT * FROM lisp_articles WHERE id=?', (chapter,)).fetchone()

            return render_template(
                f'pages/lisp/article.tmpl.html',
                active=f'lisp: {chapter}',
                title=record[1],
                content=markdown.markdown(record[2]),
                date=record[3],
            )

    except (TemplateNotFound, sqlite3.OperationalError):
        abort(404)
