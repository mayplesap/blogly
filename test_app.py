from unittest import TestCase
from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['SQLALCHEMY_ECHO'] = False

app.config["TESTING"] = True

app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]
db.drop_all()
db.create_all()

class BloglyAppTestCase(TestCase):
    """ Test flask app of Blogly. """

    def setUp(self):
        """ Set up client and config each time. """
        self.client = app.test_client()
        app.config["TESTING"] = True

        Post.query.delete()
        User.query.delete()
        user = User(first_name="Oz", 
                    last_name="Kong",
                    image_url='')
        db.session.add(user)
        db.session.commit()
        self.user = user

        posts = Post(title="Joob",
                    content="Wants ham",
                    user_id=self.user.id)
        db.session.add(posts)
        db.session.commit()
        self.post = posts

    def tearDown(self):
        """ Clean up any fouled transaction. """

        db.session.rollback()

    def test_homepage(self):
        """ Make sure information and HTML is displayed. """

        with self.client as client:
            response = client.get('/', follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('User Listing Template', html)

    def test_add_user(self):
        """ Tests add user correctly adds a new user. """

        with self.client as client:
            response = client.post('/users/new',
                                    data={'first-name': 'kitty',
                                          'last-name': 'cat',
                                          'image-url': ''}, 
                                    follow_redirects=True)
            html = response.get_data(as_text=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('kitty cat', html)

    def test_user_detail(self):
        """ Test user detail page properly displayed. """

        with self.client as client:
            response = client.get(f'/users/{self.user.id}')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(f'{self.user.first_name}', html)

    def test_user_not_exist(self):
        """ Test a user id for a user that does not exist. """

        with self.client as client:
            response = client.get('/users/0')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 404)
            self.assertIn('404 Not Found', html)

    def test_edit_user(self):
        """ Test edit user page properly displayed """

        with self.client as client:
            response = client.get(f'/users/{self.user.id}/edit')
            html = response.get_data(as_text=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('Edit User Template', html)

    def test_add_post(self):
        """ Tests add post correctly adds a new post. """

        with self.client as client:
            response = client.post(f'/users/{self.user.id}/posts/new',
                                    data={'title': 'hello',
                                          'post-content': 'world',
                                          'user_id': self.user.id}, 
                                    follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('hello', html)
            
    def test_post_detail(self):
        """ Test post detail page properly displayed. """

        with self.client as client:
            response = client.get(f'/posts/{self.post.id}')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(f'{self.user.first_name}', html)

    def test_post_not_exist(self):
        """ Test a post id for a post that does not exist. """

        with self.client as client:
            response = client.get('/posts/-1')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 404)
            self.assertIn('404 Not Found', html)

    def test_edit_post(self):
        """ Test edit post page displayed. """

        with self.client as client:
            response = client.get(f'/posts/{self.post.id}/edit')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Edit Post Template', html)
    


