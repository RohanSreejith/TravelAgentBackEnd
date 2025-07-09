from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Website, TravelPackage

User = get_user_model()

class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testagent',
            email='test@example.com',
            password='testpass123',
            phone_number='1234567890',
            agency_name='Test Agency'
        )

    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/signup.html')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')

    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'testagent',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

class DashboardTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testagent',
            password='testpass123'
        )
        self.client.login(username='testagent', password='testpass123')

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')

    def test_packages_view(self):
        response = self.client.get(reverse('packages'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/packages.html')

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='modeltest',
            password='testpass123'
        )

    def test_website_creation(self):
        website = Website.objects.create(
            agent=self.user,
            name='Test Website',
            url='https://test.com'
        )
        self.assertEqual(str(website), 'Test Website')

    def test_travel_package_creation(self):
        package = TravelPackage.objects.create(
            agent=self.user,
            title='Test Package',
            destination='Test Destination',
            duration_days=5,
            price=10000.00,
            description='Test description'
        )
        self.assertEqual(str(package), 'Test Package - Test Destination')