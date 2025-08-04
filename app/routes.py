from app import app
from flask import request
from flask import render_template, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
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


@app.route("/about")
def about():
    return render_template("about.html", page_title="ABOUT US")


@app.route("/contact")
def contact():
    return render_template("contact.html", page_title="CONTACT US")


# for contact's form to work
@app.route("/add")
def add():
    name = request.args.get("name")
    return render_template("contact.html", title=name)


@app.route("/career-advice")
def careers():
    return render_template("careers.html", page_title="CAREER ADVICE")


# showcases a list of options that leads to a topic/research letter
@app.route("/learning-zone")
def topiclist():
    topics = models.Topics.query.all()
    research = models.Research.query.all()

    return render_template("learningzone.html", page_title="LIST OF TOPICS",
                           topics=topics, research=research)


@app.route("/learning-zone/topic/ergonomics")
def ergonomics():
    return render_template("ergonomics.html")


# loads in information about the user's chosen topic
@app.route("/learning-zone/topic/<int:id>")
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


# loads in information about a research letter
@app.route("/learning-zone/research/<int:id>")
def research(id):
    research = models.Research.query.filter_by(id=id).first_or_404()
    resource = models.Resources.query.filter_by(id=id).all()

    return render_template("research.html", research=research,
                           resource=resource)


# search route and function
@app.route("/search")
def search():
    query = request.args.get("q", "").strip()

    if not query:
        return render_template("search.html", query=query, topics=[])

    results = models.Topics.query.filter(or_(
        models.Topics.name.ilike(f"%{query}%"),
        models.Topics.keywords.like(f"%{query}%"),
        models.Topics.summary.like(f"%{query}%"),
        models.Research.title.ilike(f"%{query}%"),
        models.Research.authors.like(f"%{query}%"),
        models.Research.publishers.like(f"%{query}%"),
        models.Research.introduction.like(f"%{query}%")
    )).all()
    
    return render_template("search.html", query=query, topics=results)


# error route
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=True)
