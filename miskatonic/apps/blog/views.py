from flask import Blueprint, abort, redirect, request, render_template, url_for
from flask_login import login_required
from jinja2.exceptions import TemplateNotFound

import markdown

from .forms import ArticleForm
from .models import Article


blog = Blueprint('blog', __name__, template_folder='templates')


@blog.route('/')
def index():
    try:
        return render_template(
            f'pages/blog/articles.tmpl.html',
            active='blog:',
            title='Articles',
            articles=sorted(list(Article.select()), key=lambda x: x.date, reverse=True),
        )

    except Article.DoesNotExist:
        abort(404)

    except TemplateNotFound:
        abort(500)


@blog.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    try:
        form = ArticleForm()

        if request.method == 'GET':
            return render_template(
                'pages/blog/article.tmpl.html',
                title='Post Article',
                form=form,
                active=f'blog:',
            )

        if form.validate_on_submit():
            Article.create(title=form.title.data, content=form.content.data)
            return redirect(url_for('blog.index'))

        return redirect(url_for('index'))

    except TemplateNotFound:
        abort(500)


@blog.route('/<string:slug>')
def article(slug: str):
    try:
        article = Article.get(Article.slug == slug)

        return render_template(
            f'pages/blog/article.tmpl.html',
            active=f'blog:',
            title=article.title,
            content=markdown.markdown(article.content),
            date=str(article.date).split('.')[0],
        )

    except Article.DoesNotExist:
        abort(404)

    except TemplateNotFound:
        abort(500)


@blog.route('/<string:slug>/edit', methods=['GET', 'POST'])
@login_required
def article_edit(slug: str):
    try:
        article = Article.get(Article.slug == slug)

        form = ArticleForm(title=article.title, content=article.content)

        if request.method == 'GET':
            return render_template(
                'pages/blog/article.tmpl.html',
                title=f'Edit: {article.title}',
                form=form,
                active=f'blog:',
            )

        if form.validate_on_submit():
            if form.submit.data:
                article.title = form.title.data
                article.content = form.content.data
                article.save()
                return redirect(url_for('blog.article', slug=article.slug))

            if form.delete.data:
                try:
                    article.delete_instance()

                except Exception:
                    pass

                return redirect(url_for('blog.index'))

        return redirect(url_for('blog.article', slug=article.slug))

    except Article.DoesNotExist:
        abort(404)

    except TemplateNotFound:
        abort(500)
