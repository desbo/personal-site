import os.path
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, render_template, url_for, \
    abort, flash, redirect, Markup
from jinja2.exceptions import TemplateNotFound
from datetime import datetime

app = Flask(__name__)
app.config.from_pyfile('config.py')


#this is overkill and should just be done in the template.
@app.context_processor
def set_nav():
    nav = [
    ('work', 'Work'),
    ('contact', 'Contact')
    ]

    if (app.config['BLOG_ENABLED']):
        nav.insert(0, ('blog', 'Blog'))

    return dict(nav=nav)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/<path:template>')
def show(template):
    if not template.endswith('html'):
        template = "%s.html" % template
    try:
        return render_template(template)
    except TemplateNotFound:
        abort(404)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    set_nav()

    app.debug = app.config['DEBUG']
    app.run()
