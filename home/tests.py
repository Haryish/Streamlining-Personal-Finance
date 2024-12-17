from django.test import TestCase

<<<<<<< HEAD
=======
# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile, AddMoneyInfo

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Snegan', password='12345')
        self.user_profile = UserProfile.objects.create(user=self.user, balance=1000)

    def test_user_profile_creation(self):
        self.assertEqual(self.user_profile.user.username, 'testuser')
        self.assertEqual(self.user_profile.balance, 1000)

class AddMoneyInfoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.add_money_info = AddMoneyInfo.objects.create(user=self.user, amount=500, description='Test deposit')

    def test_add_money_info_creation(self):
        self.assertEqual(self.add_money_info.user.username, 'testuser')
        self.assertEqual(self.add_money_info.amount, 500)
        self.assertEqual(self.add_money_info.description, 'Test deposit')
>>>>>>> b3dca27a3ae88f8a34cbd4564bf5085be083ce3d
