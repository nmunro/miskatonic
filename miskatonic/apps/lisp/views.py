from flask import Blueprint, abort, render_template
from jinja2.exceptions import TemplateNotFound

import markdown

from miskatonic.models import Category, Article


lisp = Blueprint('lisp', __name__, template_folder='templates')


@lisp.route('/')
def lisp_index():
    try:
        acticles = list(Article.select().where(Article.category == Category.get(Category.title == 'lisp')))

        return render_template(
            f'pages/articles.tmpl.html',
            active='lisp:',
            title='Lisp Articles',
            articles=reversed(acticles),
            category='lisp',
        )

    except (Category.DoesNotExist, Article.DoesNotExist):
        abort(404)

    except TemplateNotFound:
        abort(500)


@lisp.route('/<string:slug>')
def lisp_page(slug: str):
    try:
        category = Category.get(Category.title == 'lisp')
        article = Article.select().where(Article.category == category.id, Article.slug == slug).first()

        return render_template(
            f'pages/lisp/article.tmpl.html',
            active=f'lisp: {article.title}',
            title=article.title,
            content=markdown.markdown(article.content),
            date=article.date,
        )

    except (Category.DoesNotExist, Article.DoesNotExist):
        abort(404)

    except TemplateNotFound:
        abort(500)
