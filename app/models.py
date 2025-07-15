from app.routes import db


TopicResources = db.Table("TopicResources",
                          db.Column("topic_id", db.Integer,
                                    db.ForeignKey("Topics")),
                          db.Column("resource_id", db.Integer,
                                    db.ForeignKey("Resources"))
                          )


class Topics(db.Model):
    __tablename__ = "Topics"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    slug = db.Column(db.Text())
    image = db.Column(db.Text())
    introduction = db.Column(db.Text())
    last_updated_on = db.Column(db.Text())


class Articles(db.Model):
    __tablename__ = "Articles"
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey("Topics.id"))
    title = db.Column(db.Text())
    subheading = db.Column(db.Text())
    content = db.Column(db.Text())
    template_type = db.Column(db.Integer())
    belongs_to = db.Column(db.Text())


class Resources(db.Model):
    __tablename__ = "Resources"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    image = db.Column(db.Text())
    type = db.Column(db.Text())
    url = db.Column(db.Text())
    description = db.Column(db.Text())


class Photos(db.Model):
    __tablename__ = "Photos"
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey("Articles.id"))
    image = db.Column(db.Text())
    description = db.Column(db.Text())
    source = db.Column(db.Text())
