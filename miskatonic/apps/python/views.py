from flask import Blueprint, abort, redirect, request, render_template, url_for
from flask_login import login_required
from jinja2.exceptions import TemplateNotFound

import markdown

from miskatonic.models import Category, Article
from miskatonic.apps.python.forms import PythonArticleForm


python = Blueprint('python', __name__, template_folder='templates')


@python.route('/')
def index():
    try:
        articles = list(Article.select().where(Article.category_id == Category.get(Category.title == 'python')))

        return render_template(
            f'pages/articles.tmpl.html',
            active='python:',
            title='Python Articles',
            articles=sorted(articles, key=lambda x: x.date, reverse=True),
            category='python',
        )

    except (Category.DoesNotExist, Article.DoesNotExist):
        abort(404)

    except TemplateNotFound:
        abort(500)


@python.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = PythonArticleForm()

    if request.method == 'GET':
        return render_template(
            'pages/post.tmpl.html',
            title='Post',
            form=form,
            active=f'python:',
        )

    if form.validate_on_submit():
        Article.create(
            title=form.title.data,
            category_id=Category.get(Category.title == 'python'),
            content=form.content.data,
        )
        return redirect(url_for('python.index'))

    return redirect(url_for('index'))


@python.route('/<string:slug>')
def article(slug: str):
    try:
        category = Category.get(Category.title == 'python')
        article = Article.select().where(Article.category_id == category, Article.slug == slug).first()

        return render_template(
            f'pages/python/article.tmpl.html',
            active=f'python: {article.title}',
            title=article.title,
            content=markdown.markdown(article.content),
            date=str(article.date).split('.')[0],
        )

    except (Category.DoesNotExist, Article.DoesNotExist):
        abort(404)

    except TemplateNotFound:
        abort(500)


@python.route('/<string:slug>/edit', methods=['GET', 'POST'])
@login_required
def article_edit(slug: str):
    article = Article.get(Article.slug == slug)
    form = PythonArticleForm(title=article.title, content=article.content)

    if request.method == 'GET':
        return render_template(
            'pages/post.tmpl.html',
            title='Post',
            form=form,
            active=f'python:',
        )

    if form.validate_on_submit():
        article.title = form.title.data
        article.content = form.content.data
        article.save()
        return redirect(url_for('python.index'))

    return redirect(url_for('index'))
