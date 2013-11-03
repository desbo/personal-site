import os.path
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, render_template, url_for, \
    abort, flash, redirect, Markup
from jinja2.exceptions import TemplateNotFound
from datetime import datetime

app = Flask(__name__)
app.config.from_pyfile('config.py')


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def connect_db():
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    return db


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

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


def prompt_for_login():
    return render_template('login.html')


def process_login(username, password):
    if (username == app.config['USERNAME'] and
            password == app.config['PASSWORD']):
        session['logged_in'] = True
        return render_template('post.html')
    else:
        flash('Bad login details!')
        return prompt_for_login()


def save_post(title, text):
    with get_db() as db:
        db.execute(
            'insert into posts (title, text, posted_on) values (?, ?, ?)',
            [title, text, str(datetime.now())])
        db.commit()
        flash('Post %s saved' % title)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/blog')
def show_posts():
    with get_db() as db:
        cur = db.execute('select * from posts order by posted_on desc')
        posts = cur.fetchall()
        return render_template('blog.html', posts=posts)


@app.route('/post', methods=['GET', 'POST'])
def post():
    if session.get('logged_in') == True:
        if request.method == 'POST':
            if (request.form['title'] and request.form['text']):
                save_post(request.form['title'], request.form['text'])
                return redirect(url_for('show_posts'))
            else:
                flash('No content provided')
                return render_template('post.html')
        else:
            return render_template('post.html')
    else:
        return prompt_for_login()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return process_login(request.form['username'],
                             request.form['password'])
    else:
        return prompt_for_login()


@app.route('/logout')
def logout():
    del session['logged_in']
    return redirect(url_for('home'))


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
    init_db()
    set_nav()

    app.debug = app.config['DEBUG']
    app.run()
