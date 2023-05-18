from django.test import TestCase
from django.urls import reverse
from homeapp.models import User

class urlsTests(TestCase):

    #Set up for testing pages when users are logged in.
    @classmethod
    def setUpTestData(cls):
        user1 = User(username='user1', email='user1@email.com')
        user1.set_password('MyPassword123')
        user1.save()

    #Testing the response code of the Nutrition Page when the user isn't logged in.
    def test_modulePageNoLogin(self):
        response = self.client.get(reverse('nutrition'))
        self.assertNotEqual(response.status_code, 200)
    
    #Testing the response code of the Nutrition Page and the details that we expect to be there when the user is logged in.
    def test_modulePageLogin(self):
        login = self.client.login(username='user1', password='MyPassword123')
        self.assertTrue(login)
        response = self.client.get(reverse('nutrition'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Nutrition')
        self.assertContains(response, 'Search Nutritional Values')
        self.assertContains(response, 'Log your weekly caloric intake')
    