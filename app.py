"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

#################### USER ####################

@app.route("/")
def home():
    """ Redirect to list of users. """

    return redirect("/users")

@app.route("/users")
def user_listings():
    """ Shows User listings and add new user button. """

    users = User.query.all()
    return render_template("user_listing.html", users=users)

@app.route("/users/new")
def new_user_form():
    """ Add new user form. """

    return render_template("new_user_form.html")

@app.route("/users/new", methods=["POST"])
def add_user():
    """ Takes input from form and adds new user to database """

    data = request.form
    first_name = data['first-name']
    last_name = data['last-name']
    img = data['image-url'] or None
    # img = img if img else None

    user = User(first_name=first_name,
                    last_name=last_name, 
                    image_url=img)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """ Takes user id and shows user's page details. """

    user = User.query.get_or_404(user_id)
    posts = user.posts
    return render_template("user_detail.html", user=user, posts=posts)

@app.route("/users/<int:user_id>/edit")
def edit_user_form(user_id):
    """ Shows the edit_user_form. """

    user = User.query.get_or_404(user_id)
    return render_template("edit_user_form.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """ Submit new changes to database and redirects to /users """
    
    data = request.form
    user = User.query.get_or_404(user_id)
    user.first_name = data['first-name']
    user.last_name = data['last-name']
    user.image_url = data['image-url'] or None
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """ Deletes a user. """

    user = User.query.get_or_404(user_id)
    Post.query.filter(Post.user_id == user.id).delete()
    db.session.commit()
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/posts/new")
def new_post_form(user_id):    
    """ Shows new_post_form. """

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template("new_post_form.html", user=user, tags=tags)

#################### POST ####################

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def new_post(user_id):
    """ Takes input from form and adds a new post. """

    data = request.form
    title = data['title']
    post_content = data['post-content']
    
    post = Post(title=title,
                content=post_content,
                created_at=None,
                user_id=user_id)
    db.session.add(post)
    db.session.commit()

    tag_ids = data.getlist('tag-name')

    for tag_id in tag_ids:
        post_tag = PostTag(post_id=post.id,
                        tag_id=tag_id)
        db.session.add(post_tag)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """ Displays a post. """

    post = Post.query.get_or_404(post_id)
    # user = User.query.get(post.user_id)
    tags = post.tags
    return render_template("post_detail.html", 
                           post=post, 
                           user=post.user, 
                           tags=tags)

@app.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    """ Shows the edit_post_form. """

    post = Post.query.get_or_404(post_id)
    return render_template("edit_post_form.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """ Submit new changes to database and redirects back to post detail. """

    post = Post.query.get_or_404(post_id)

    data = request.form
    post.title = data['title']
    post.content = data['post-content']
    db.session.commit()

    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """ Deletes a post. """

    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

#################### TAG ####################

@app.route("/tags")
def list_tags():
    """ Shows a list of tags. """

    tags = Tag.query.all()
    return render_template("tag_listing.html", tags=tags)

@app.route("/tags/<int:tag_id>")
def show_tag(tag_id):
    """ Takes tag id and shows tag details. """

    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template("tag_detail.html", tag=tag, posts=posts)

@app.route("/tags/new")
def new_tag_form():
    """ Add new tag form. """

    return render_template("new_tag_form.html")

@app.route("/tags/new", methods=["POST"])
def add_tag():
    """ Takes input from form and adds new tag to database. """

    name = request.form['tag-name']

    tag = Tag(name=name)
    """ TODO check for dupe names """
    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route("/tags/<int:tag_id>/edit")
def edit_tag_form(tag_id):
    """ Shows edit_tag_form. """

    tag = Tag.query.get_or_404(tag_id)
    return render_template("edit_tag_form.html", tag=tag)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """ Submit new changes to database and redirects to /tags. """

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['tag-name']
    db.session.commit()

    return redirect(f"/tags/{tag_id}")

@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """ Deletes a tag. """

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")