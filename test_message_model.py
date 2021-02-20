import os
from unittest import TestCase

from models import db, User, Message, Follows,Likes

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



class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        user = User.signup("test", "test@test.com", "testpass", None)
        self.uid = 123
        user.id = self.uid

        db.session.commit()

        self.user = User.query.get(self.uid)        
        
        self.client = app.test_client()
    
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback
        return res

    def test_messages(self):
        """Does it allow to create messages?"""

        msg = Message(text="welcome back", user_id = self.uid)
        db.session.add(msg)
        db.session.commit()

        self.assertEqual(len(self.user.messages[0].text),'welcome back')
        self.assertEqual(len(self.user.messages),1)
    
    def test_likes(self):
        '''does it allow us to like messages'''
        user2 = User.signup('test2','test2@test.com', 'testpass2',None)
        self.uid = 124
        user.id = self.uid

        msg = Message( text='like this', user_id=self.uid)
        db.session.add_all([user2,msg])
        db.session.commit()

        user2.likes.append(msg)
        db.session.commit()

        likes = Likes.query.filer(Likes.user_id == uid).all()

        self.assertEqual(len(likes),1)
        
