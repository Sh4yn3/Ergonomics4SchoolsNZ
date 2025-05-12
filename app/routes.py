from app import app
from flask import render_template, abort
from flask_sqlalchemy import SQLAlchemy
import os


basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "ergonomics.db")
db.init_app(app)


import app.models as models


# landing page route
@app.route('/')
def root():
    return render_template('home.html', page_title='HOME')


# about route
@app.route('/about')
def about():
    return render_template('about.html', page_title='ABOUT US')


# contact route
@app.route('/contact')
def contact():
    return render_template('about.html', page_title='CONTACT US')


# topic list route
@app.route('/topics')
def topiclist():
    return render_template('topics_list.html', page_title='LIST OF TOPICS')


# displays a topic of the user's choice
@app.route('/topic/<int:id>')
def topic():
    # get the topic, but put 404 instead if id doesn't exist
    topic = models.ergonomics.query.filter_by(id=id).first_or_404()
    print(topic, topic.name)
    return render_template('topictype1.html', topic=topic)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=True)
