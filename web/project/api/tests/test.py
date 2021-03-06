# placeholder for tests
import json
import os
import sys
import unittest
import tempfile
import datetime
from project import app, db, models

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
basedir = os.path.abspath(os.path.dirname(__file__))

from flask_sqlalchemy import SQLAlchemy


class TestLogin(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
        response = self.app.post(
            '/register/',
            data={
                'email': 'user@gmail.com',
                'password': 'password',
            })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertTrue(data['created'])
        self.assertEqual(data['so_pending_id'], '')
        assert models.User.query.filter_by(email='user@gmail.com').first()

    def test_incomplete_data(self):
        response = self.app.post(
            '/register/',
            data={
                'password': 'password',
            })
        self.assertEqual(response.status_code, 400)
        response = self.app.post(
            '/register/',
            data={
                'email': 'jackson.kontny@gmail.com',
            })
        self.assertEqual(response.status_code, 400)

    def test_duplicate_info(self):
        new_user = models.User(
            email='something@something.com', password_hash='hash')
        new_user.save()

        response = self.app.post(
            '/register/',
            data={
                'email': new_user.email,
                'password': 'password',
            })
        self.assertEqual(response.status_code, 400)

    def test_register_temp_user(self):
        new_user = models.User(
            email='something@something.com', password_hash='hash', is_temp=True)
        new_user.save()
        so_pending_user = models.User(
            email='waiting@something.com',
            password_hash='hash', is_temp=False, so_id=new_user.id)
        so_pending_user.save()
        response = self.app.post(
            '/register/',
            data={
                'email': new_user.email,
                'password': 'password',
            })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertFalse(data['created'])
        self.assertEqual(data['email'], 'something@something.com')
        self.assertEqual(data['so_pending_id'], so_pending_user.id)

    def test_update_new_so(self):
        user = models.User(
            email='something@something.com')
        user.save(password='password')
        response = self.app.post(
            '/login_standard/',
            data={
                'email': user.email,
                'password': 'password',
            })
        self.assertEqual(response.status_code, 200)
        response = self.app.post(
            '/update_so/',
            data={
                'email': 'new_email@email.com'
            }
        )
        self.assertEqual(response.status_code, 200)
        so_user = models.User.query.filter_by(email='new_email@email.com').first()
        user = models.User.query.get(user.id)
        self.assertEqual(user.so_id, so_user.id)
        data = json.loads(response.data)
        self.assertEqual(data['id'], user.id)
        self.assertEqual(data['so_id'], user.so_id)
        self.assertTrue(data['is_so_temp'])

    def test_update_existing_so(self):
        user = models.User(
            email='something@something.com')
        user.save(password='password')
        existing_so = models.User(
            email='existing@something.com')
        existing_so.save(password='password')
        existing_so = models.User.query.filter_by(email='existing@something.com').first()
        response = self.app.post(
            '/login_standard/',
            data={
                'email': user.email,
                'password': 'password',
            })
        self.assertEqual(response.status_code, 200)
        response = self.app.post(
            '/update_so/',
            data={
                'email': existing_so.email
            }
        )
        self.assertEqual(response.status_code, 200)
        user = models.User.query.get(user.id)
        self.assertEqual(user.so_id, existing_so.id)
        data = json.loads(response.data)
        self.assertEqual(data['id'], user.id)
        self.assertEqual(data['so_id'], user.so_id)
        self.assertFalse(data['is_so_temp'])

    def test_login(self):
        new_user = models.User(
            email='something@something.com')
        new_user.save(password='password')
        response = self.app.post(
            '/login_standard/',
            data={
                'email': new_user.email,
                'password': 'password',
            })
        self.assertEqual(response.status_code, 200)

    def test_incorrect_password(self):
        new_user = models.User(
            email='something@something.com')
        new_user.save(password='password')
        response = self.app.post(
            '/login_standard/',
            data={
                'email': new_user.email,
                'password': 'password_wrong',
            })
        self.assertEqual(response.status_code, 400)

    def test_ping(self):
        user = models.User(
            email='something@something.com')
        so = models.User(
            email='someones_gf@something.com')
        user.save(password='password')
        so.save(password='password')
        user.so_id = so.id
        so.so_id = user.id
        user.save()
        so.save()
        self.assertEqual(user.sent_messages().count(), 0)
        response = self.app.post(
            '/login_standard/',
            data={
                'email': user.email,
                'password': 'password',
            })
        response = self.app.post('/ping/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.sent_messages().count(), 1)
        data = json.loads(response.data)
        response_sent_at = data['message_sent_at']
        self.assertIsNotNone(response_sent_at)

    def test_ping_without_so(self):
        user = models.User(
            email='something@something.com')
        so = models.User(
            email='someones_gf@something.com')
        user.save(password='password')
        so.save(password='password')
        user.so_id = so.id
        so.so_id = user.id
        user.save()
        so.save()
        self.assertEqual(user.sent_messages().count(), 0)
        response = self.app.post(
            '/login_standard/',
            data={
                'email': user.email,
                'password': 'password',
            })
        response = self.app.post('/ping/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.sent_messages().count(), 1)

    def test_get_messages(self):
        user = models.User(
            email='something@something.com')
        so = models.User(
            email='someones_gf@something.com')
        user.save(password='password')
        so.save(password='password')
        user.so_id = so.id
        so.so_id = user.id
        user.save()
        so.save()
        for idx in range(5):
            ping = models.Ping(from_id=user.id, to_id=so.id)
            ping.save()
        self.assertEqual(user.sent_messages().count(), 5)
        response = self.app.post(
            '/login_standard/',
            data={
                'email': so.email,
                'password': 'password',
            })
        response = self.app.get('/get_messages/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 5)

        response = self.app.post(
            '/login_standard/',
            data={
                'email': user.email,
                'password': 'password',
            })
        response = self.app.get('/get_messages/')
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)


if __name__ == '__main__':
    unittest.main()
