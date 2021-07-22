"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

NO_IMAGE_IMAGE = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'

def connect_db(app):
    """ Connect to database. """

    db.app = app
    db.init_app(app)

class User(db.Model):
    """ User. """

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                          nullable=False)
    image_url = db.Column(db.Text, default=NO_IMAGE_IMAGE)

    def __repr__(self):
        return f"<User {self.id}: {self.first_name} {self.last_name}>"

    def get_full_name(self):
        """ Concatenate first and last name. """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name

    posts = db.relationship('Post', 
                            backref='user')

class Post(db.Model):
    """ Post. """

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text,
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime,
                           default=datetime.datetime.now)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"),
                        nullable=False)
    
    def __repr__(self):
        return f"<Post {self.id}: {self.title} by user id {self.user_id} created at {self.created_at}>"

    # posts_tags = db.relationship('PostTag',
    #                              backref='post')

    tags = db.relationship('Tag', 
                           secondary='posts_tags',
                           backref='posts')

class Tag(db.Model):
    """ Tag. """

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text,
                     nullable=False,
                     unique=True)

    def __repr__(self):
        return f"<Tag {self.id}: {self.name}>"

    # posts_tags = db.relationship('PostTag',
    #                              backref='tag')


class PostTag(db.Model):
    """ PostTag."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey("posts.id"),
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey("tags.id"),
                       primary_key=True)
