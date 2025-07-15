from app import app
from flask import request
from flask import render_template, abort
from flask_sqlalchemy import SQLAlchemy
import os


basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "ergonomics.db")
db.init_app(app)


import app.models as models


# landing page route
@app.route("/")
def root():
    return render_template("home.html", page_title="HOME")


# about route
@app.route("/about")
def about():
    return render_template("about.html", page_title="ABOUT US")


# contact route
@app.route("/contact")
def contact():
    return render_template("contact.html", page_title="CONTACT US")


# for contact
@app.route("/add")
def add():
    name = request.args.get("name")
    return render_template("contact.html", title=name)


# careers advice
@app.route("/career-advice")
def careers():
    return render_template("careers.html", page_title="CAREER ADVICE")


# topic list route
@app.route("/topics")
def topiclist():
    topics = models.Topics.query.all()
    return render_template("topics_list.html", page_title="LIST OF TOPICS",
                           topics=topics)


# topics route
@app.route("/topic/<int:id>")
def topic(id):
    topic = models.Topics.query.filter_by(id=id).first_or_404()
    articles = models.Articles.query.filter_by(topic_id=id).all()
    photo = models.Photos.query.get_or_404(id)
    resource = models.Resources.query.filter_by(id=id).all()

    # Convert template_type to int if it"s a string
    for article in articles:
        if article.template_type and isinstance(article.template_type, str):
            try:
                article.template_type = int(article.template_type)
            except ValueError:
                article.template_type = 0  # or skip, or set to a default value

    return render_template("topic.html", topic=topic, articles=articles,
                           photo=photo, resource=resource)


@app.route("/search")
def search():
    query = request.args.get("q", "").strip()

    if not query:
        return render_template("search.html", query=query, topics=[])

    # Search topics by name (case-insensitive, partial match)
    results = models.Topics.query.filter(models.Topics.name.ilike(f"%{query}%")).all()

    return render_template("search.html", query=query, topics=results)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=True)
