import os.path
import sys
import json
from flask import Flask, request, session, g, render_template, url_for, \
    abort, flash, redirect, Markup
from jinja2.exceptions import TemplateNotFound
from datetime import datetime
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/work')
def work():
    projects = json.load(open('data/projects.json'))['projects']
    return render_template('work.html', projects=projects)


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
    try:
        app.debug = sys.argv[1] == "debug"
    except IndexError:
        pass
    app.run()