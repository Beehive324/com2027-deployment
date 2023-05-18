from django.test import TestCase
from django.urls import reverse


class urlsTests(TestCase):
    
    #Testing the response code of our Module Page and the details within which we expect to be there.
    def test_modulePage(self):
        response = self.client.get(reverse('nutrition'), follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Nutrition')
        self.assertContains(response, 'Search Nutritional Values')
        self.assertContains(response, 'Log your weekly caloric intake')
    