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
    return render_template('contact.html', page_title='CONTACT US')


# topic list route
@app.route('/topics')
def topiclist():
    return render_template('topics_list.html', page_title='LIST OF TOPICS')


@app.route('/topic/<int:topic_id>')
def topic(topic_id):
    topic = models.Topics.query.filter_by(id=topic_id).first_or_404()
    articles = models.Articles.query.filter_by(topic_id=topic_id).all()

    valid_articles = []
    for article in articles:
        template_type = article.template_type
        include_path = f"topic templates/article_{template_type}.html"
        full_path = os.path.join(app.template_folder, include_path)
        if os.path.isfile(full_path):
            valid_articles.append({'article': article, 'include_path': include_path})

    return render_template("topic.html", topic=topic, articles=valid_articles)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=True)
