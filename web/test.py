# placeholder for tests
import os
import unittest
import tempfile
from project import app, db, models

import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
basedir = os.path.abspath(os.path.dirname(__file__))
from flask.ext.sqlalchemy import SQLAlchemy


class TestLogin(unittest.TestCase):

    def setUp(self):
        self.db_uri = 'sqlite:///' + os.path.join(basedir, 'test.db')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
        self.app = app.test_client()
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
        response = self.app.post(
            '/register/',
            data={
                'username': 'something',
                'email': 'jackson.kontny@gmail.com',
                'password': 'password',
            })
        self.assertEqual(response.status_code, 201)
        assert models.User.query.filter_by(username='something').first()

    def test_incomplete_data(self):
        response = self.app.post(
            '/register/',
            data={
                'username': 'something',
                'password': 'password',
            })
        self.assertEquals(response.status_code, 400)
        response = self.app.post(
            '/register/',
            data={
                'username': 'something',
                'email': 'jackson.kontny@gmail.com',
            })
        self.assertEquals(response.status_code, 400)
        response = self.app.post(
            '/register/',
            data={
                'password': 'password',
                'email': 'jackson.kontny@gmail.com',
            })
        self.assertEquals(response.status_code, 400)

    def test_duplicate_info(self):
        new_user = models.User(
            username='something', email='something@something.com', password_hash='hash')
        db.session.add(new_user)
        db.session.commit()

        response = self.app.post(
            '/register/',
            data={
                'username': new_user.username,
                'email': 'new@email.com',
                'password': 'password',
            })
        self.assertEquals(response.status_code, 400)
        response = self.app.post(
            '/register/',
            data={
                'username': 'newusername',
                'email': new_user.email,
                'password': 'password',
            })
        self.assertEquals(response.status_code, 400)

    def test_update_so(self):
        new_user = models.User(
            username='something', email='something@something.com', password_hash='hash')
        db.session.add(new_user)
        db.session.commit()



    def test_login(self):
        pass


if __name__ == '__main__':
    unittest.main()
