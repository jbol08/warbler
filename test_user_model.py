"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        user1 = User.signup("test", "test@test.com", "testpass", None)
        self.uid1 = 123
        user1.id = self.uid

        user2 = User.signup("test2", "test2@test.com", "testpass2", None)
        self.uid2 = 124
        user2.id = self.uid

        db.session.commit()

        user1 = User.query.get(uid1)
        user2 = User.query.get(uid2)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback
        return res

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_following(self):
        '''test that can follow'''
        self.user1.following.append(self.user2)
        db.session.commit()

        self.assertEqual(self.user2.followers[0].id, self.user1.id)

    def test_is_following(self):
        '''test if user 1 is following user2'''
        self.user1.following.append(self.user2)
        db.session.commit()

        self.assertTrue(self.user1.is_following(self.user2))
        

    def test_is_followed_by(self):
        '''test is user 2 is followed by user 1'''
        self.user1.following.append(self.user2)
        db.session.commit()

        self.assertTrue(self.user2.is_followed_by(self.user1))

    def test_signup():
        '''testing that can do a valid signup'''
        user_test = User.signup("test3", "test3@test.com", "testpass2", None)
        uid = 125
        user_test.id = uid
        db.session.commit()

        user_test = User.query.get(uid)
        self.assertIsNotNone(user_test)
        self.assertEqual(user_test.username, "test3")
        self.assertEqual(u_test.email, "test3@test.com")
        self.assertTrue(u_test.password.startswith("$2b$"))

    def test_invalid_username_signup(self):
        '''test that it fails if we do not pass a username which is a required field'''
        no_user = User.signup(None, "test@test.com", "password", None)
        uid = 126
        no_user.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_valid_authentication(self):
        '''check to make sure a user can be authenticated'''
        user = User.authenticate(self.user1.username, "testpass")
        self.assertIsNotNone(user)
        self.assertEqual(user.id, self.uid1)

