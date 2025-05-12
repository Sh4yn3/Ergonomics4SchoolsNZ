from app.routes import db


TopicResources = db.Table('TopicResources',
        db.Column('topic_id', db.Integer, db.Foreignkey('Topics')),
        db.Column('resource_id', db.Integer, db.Foreignkey('Resources')))


class Topics(db.Model):
    __tablename__ = "Topics"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.text())
    slug = db.Column(db.text())
    image = db.Column(db.text())
    introduction = db.Column(db.text())
    last_updated_on = db.Column(db.text())
    created_on = db.Column(db.text())


class Articles(db.Model):
    __tablename__ = "Articles"
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.Foreignkey('Topics.id'))
    title = db.Column(db.text())
    content = db.Column(db.text())
    template_type = db.Column(db.Integer())


class Resources(db.Model):
    __tablename__ = "Resources"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.text())
    image = db.Column(db.text())
    type = db.Column(db.text())
    url = db.Column(db.text())
    description = db.Column(db.text())


class Images(db.Model):
    __tablename__ = "Images"
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.Foreignkey('Articles.id'))
    image = db.Column(db.text())
    description = db.Column(db.text())
    source = db.Column(db.text())
