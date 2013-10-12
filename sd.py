from flask import Flask, render_template, url_for, abort
from jinja2.exceptions import TemplateNotFound

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/test')
def test():
    return 'testing!'


@app.route('/<path:template>')
def show(template):
    if not template.endswith('html'):
        template = "%s.html" % template
    try:
        return render_template(template)
    except TemplateNotFound:
        abort(404)

if __name__ == '__main__':
    app.debug = True
    app.run()
