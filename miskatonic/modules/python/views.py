from flask import Blueprint, abort, render_template
from jinja2.exceptions import TemplateNotFound

import markdown

from miskatonic.db import Category, Article


python = Blueprint('python', __name__, template_folder='templates')


@python.route('/')
def python_index():
    try:
        articles = list(Article.select().where(Article.category == Category.get(Category.title == 'python')))

        return render_template(
            f'pages/articles.tmpl.html',
            active='python:',
            title='Python Articles',
            articles=reversed(articles),
            category='python',
        )

    except (Category.DoesNotExist, Article.DoesNotExist):
        abort(404)

    except TemplateNotFound:
        abort(500)


@python.route('/<string:slug>')
def python_page(slug: str):
    try:
        category = Category.get(Category.title == 'python')
        article = Article.select().where(Article.category == category, Article.slug == slug).first()

        return render_template(
            f'pages/python/article.tmpl.html',
            active=f'python: {article.title}',
            title=article.title,
            content=markdown.markdown(article.content),
            date=article.date,
        )

    except (Category.DoesNotExist, Article.DoesNotExist):
        abort(404)

    except TemplateNotFound:
        abort(500)
