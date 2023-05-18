from django.test import TestCase
from django.urls import reverse
from homeapp.models import User
# Create your tests here.

class chatAppTests(TestCase):

    #Set up for testing pages when users are logged in.
    @classmethod
    def setUpTestData(cls):
        user1 = User(username='user1', email='user1@email.com')
        user1.set_password('MyPassword123')
        user1.save()

    #Testing the response code of the Chat Rooms index Page when the user isn't logged in.
    def test_chatAppIndexNoLogin(self):
        response = self.client.get(reverse('chat_index'))
        self.assertNotEqual(response.status_code, 200)
    
    #Testing the response code of the Chat Rooms index Page and details that should be contained within the page when the user is logged in.
    def test_chatAppIndexLogin(self):
        login = self.client.login(username='user1', password='MyPassword123')
        self.assertTrue(login)
        response = self.client.get(reverse('chat_index'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Chat Rooms')
        self.assertContains(response, 'General Discussion')
        self.assertContains(response, 'Support')

    #Testing the response code of the General Discussion's chat room/page when the user isn't logged in..
    def test_generalDiscussionChatPageNoLogin(self):
        response = self.client.get('/chat/general/', follow=True)
        self.assertNotEqual(response.status_code, 200)
    
    #Testing the response code of the General Discussion's chat room/page and details that should be contained within the page when the user is logged in.
    def test_generalDiscussionChatPageLogin(self):
        login = self.client.login(username='user1', password='MyPassword123')
        self.assertTrue(login)
        response = self.client.get('/chat/general/', follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'general')
        self.assertContains(response, 'un-moderated')
        self.assertContains(response, 'Your message here')

    #Testing the response code of the Support chat room/page when the user isn't logged in..
    def test_supportChatPageNoLogin(self):
        response = self.client.get('/chat/support/', follow=True)
        self.assertNotEqual(response.status_code, 200)
   
    #Testing the response code of the Support chat room/page and details that should be contained within the page when the user is logged in.
    def test_supportChatPageLogin(self):
        login = self.client.login(username='user1', password='MyPassword123')
        self.assertTrue(login)
        response = self.client.get('/chat/support/', follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'support')
        self.assertContains(response, 'un-moderated')
        self.assertContains(response, 'Your message here')

    #Testing the response code of a custom chat room/page when the user isn't logged in.
    def test_ownRoomPageNoLogin(self):
        response = self.client.get('/chat/1/', follow=True)
        self.assertNotEqual(response.status_code, 200)
   
    #Testing the response code of a custom chat room/page and details that should be contained within the page.
    def test_ownRoomPageLogin(self):
        login = self.client.login(username='user1', password='MyPassword123')
        self.assertTrue(login)
        response = self.client.get('/chat/1/', follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '1')
        self.assertContains(response, 'un-moderated')
        self.assertContains(response, 'Your message here')