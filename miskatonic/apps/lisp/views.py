from flask import Blueprint, abort, redirect, request, render_template, url_for
from flask_login import login_required
from jinja2.exceptions import TemplateNotFound

import markdown

from miskatonic.models import Category, Article
from miskatonic.apps.lisp.forms import LispArticleForm


lisp = Blueprint('lisp', __name__, template_folder='templates')


@lisp.route('/')
def index():
    try:
        articles = list(Article.select().where(Article.category_id == Category.get(Category.title == 'lisp')))

        return render_template(
            f'pages/articles.tmpl.html',
            active='lisp:',
            title='Lisp Articles',
            articles=sorted(articles, key=lambda x: x.date, reverse=True),
            category='lisp',
        )

    except (Category.DoesNotExist, Article.DoesNotExist):
        abort(404)

    except TemplateNotFound:
        abort(500)


@lisp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = LispArticleForm()

    if request.method == 'GET':
        return render_template(
            'pages/post.tmpl.html',
            title='Post',
            form=form,
            active=f'lisp:',
        )

    if form.validate_on_submit():
        Article.create(
            title=form.title.data,
            category_id=Category.get(Category.title == 'lisp'),
            content=form.content.data,
        )
        return redirect(url_for('lisp.index'))

    return redirect(url_for('index'))


@lisp.route('/<string:slug>')
def article(slug: str):
    try:
        category = Category.get(Category.title == 'lisp')
        article = Article.select().where(Article.category_id == category.id, Article.slug == slug).first()

        return render_template(
            f'pages/lisp/article.tmpl.html',
            active=f'lisp: {article.title}',
            title=article.title,
            content=markdown.markdown(article.content),
            date=str(article.date).split('.')[0],
        )

    except (Category.DoesNotExist, Article.DoesNotExist):
        abort(404)

    except TemplateNotFound:
        abort(500)


@lisp.route('/<string:slug>/edit', methods=['GET', 'POST'])
@login_required
def article_edit(slug: str):
    article = Article.get(Article.slug == slug)
    form = LispArticleForm(title=article.title, content=article.content)

    if request.method == 'GET':
        return render_template(
            'pages/post.tmpl.html',
            title='Post',
            form=form,
            active=f'lisp:',
        )

    if form.validate_on_submit():
        article.title = form.title.data
        article.content = form.content.data
        article.save()
        return redirect(url_for('lisp.index'))

    return redirect(url_for('index'))
