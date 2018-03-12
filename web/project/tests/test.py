# placeholder for tests
import os
import unittest
import tempfile
import project

class TestLogin(unittest.TestCase):

    def setUp(self):
        self.db_fd, project.app.config['DATABASE'] = tempfile.mkstemp()
        project.app.testing = True
        self.app = project.app.test_client()
        with project.app.app_context():
            project.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(project.app.config['DATABASE'])

    def test_create_user(self):
        pass

    def test_update_so(self):
        pass

    def test_login(self):
        pass


if __name__ == '__main__':
    unittest.main()
