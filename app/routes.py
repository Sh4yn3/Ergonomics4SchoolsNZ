from app import app
from flask import request
from flask import render_template, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import os


basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir,"ergonomics.db")
db.init_app(app)


import app.models as models


@app.route("/")
def root():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/career-advice")
def careers():
    return render_template("careers.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


# working form for the contact page
@app.route("/add")
def add():
    name = request.args.get("name")
    return render_template("contact.html", name=name)


# list of options that leads to a (research) topic
@app.route("/learning-zone")
def learningzone():
    topic = models.Topics.query.all()
    research = models.Research.query.all()

    return render_template("learningzone.html", topic=topic,
                           research=research)


@app.route("/learning-zone/topic/ergonomics")
def ergonomics():
    return render_template("ergonomics.html")


# DELETE LATER
@app.route("/test")
def test():
    return render_template("test.html")


# loads in information of the user's chosen topic
@app.route("/learning-zone/topic/<int:id>")
def topic(id):
    topic = models.Topics.query.filter_by(id=id).first_or_404()
    articles = models.Articles.query.filter_by(topic_id=id).all()
    photo = models.Photos.query.get_or_404(id)
    resource = models.Resources.query.filter_by(id=id).all()

    return render_template("topic.html", topic=topic, articles=articles,
                           photo=photo, resource=resource)


# loads in information about the user's chosen research letter
@app.route("/learning-zone/research/<int:id>")
def research(id):
    research = models.Research.query.filter_by(id=id).first_or_404()
    resource = models.Resources.query.filter_by(id=id).all()

    return render_template("research.html", research=research,
                           resource=resource)


# search route and function
@app.route("/search")
def search():
    # Get the "q" parameter from the URL (e.g. /search?q=chair)
    # If q is missing, use an empty string instead
    # .strip() removes extra spaces at start or end
    query = request.args.get("q", "").strip()

    # If the query is empty (user searched nothing),
    # just show the search page with no results
    if not query:
        return render_template("search.html", query=query, topics=[])

    # otherwise, searched the database with the specified text
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
