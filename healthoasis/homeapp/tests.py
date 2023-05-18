from django.test import TestCase
from django.urls import reverse
from .models import User

# Create your tests here.

class homeAppTests(TestCase):
    
    #Set up for testing pages when users are logged in.
    @classmethod
    def setUpTestData(cls):
        user1 = User(username='user1', email='user1@email.com')
        user1.set_password('MyPassword123')
        user1.save()

    #Testing the response code of the homepage and details that should and shouldn't be on
    # the homepage when the user isn't logged in.
    def test_homePageNoLogin(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Homepage')
        self.assertContains(response, 'Login')
        self.assertContains(response, 'Sign up')

        self.assertNotContains(response, 'Weather')
        self.assertNotContains(response, 'Nutrition')
        self.assertNotContains(response, 'Exercise')
        self.assertNotContains(response, 'Chat')
        self.assertNotContains(response, 'Workouts')
        self.assertNotContains(response, 'Progress')
        self.assertNotContains(response, 'Workouts')
        self.assertNotContains(response, 'Logout')

    #Testing the response code of the homepage and details that should and shouldn't be on
    # the homepage when the user is logged in.
    def test_homePageLogin(self):
        login = self.client.login(username='user1', password='MyPassword123')
        self.assertTrue(login)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Homepage')
        self.assertContains(response, 'Weather')
        self.assertContains(response, 'Nutrition')
        self.assertContains(response, 'Exercise')
        self.assertContains(response, 'Chat')
        self.assertContains(response, 'Workouts')
        self.assertContains(response, 'Progress')
        self.assertContains(response, 'Workouts')
        self.assertContains(response, 'Logout')

        
        self.assertNotContains(response, 'Login')
        self.assertNotContains(response, 'Sign up')

