from django.test import TestCase
from django.urls import reverse
from django.db import transaction
from django.db.backends.sqlite3.base import IntegrityError
# Create your tests here.


class chatAppTests(TestCase):
    #Testing the response code of the Chat Rooms index Page and details that should be contained within the page.
    def test_chatAppIndex(self):
        response = self.client.get('/chat/')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Chat Rooms')
        self.assertContains(response, 'General Discussion')
        self.assertContains(response, 'Support')

    #Testing the response code of the General Discussion's chat room/page and details that should be contained within the page.
    def test_generalDiscussionChatPage(self):
        response = self.client.get('/chat/general/', follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'general')
        self.assertContains(response, 'un-moderated')
        self.assertContains(response, 'Your message here')

    #Testing the response code of the Support chat room/page and details that should be contained within the page.
    def test_supportChatPage(self):
        response = self.client.get('/chat/support/', follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'support')
        self.assertContains(response, 'un-moderated')
        self.assertContains(response, 'Your message here')

    #Testing the response code of a custom chat room/page and details that should be contained within the page.
    def test_ownRoomPage(self):
        response = self.client.get('/chat/1/', follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '1')
        self.assertContains(response, 'un-moderated')
        self.assertContains(response, 'Your message here')