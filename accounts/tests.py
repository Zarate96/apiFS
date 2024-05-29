from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from accounts.models import MyUser
from shared.constants import constants

class UserRegistrationAPIViewTest(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.valid_user_data = {
            "username": "testuser",
            "password": "password123",
            "password2": "password123",
            "email": "testuser@example.com",
            "es_cliente": True
        }
        self.invalid_user_data = {
            "username": "",
            "password": "password123",
            "password2": "password123",
            "email": "not-an-email",
            "es_cliente": True
        }

    @patch('accounts.utils.EmailHandler.send_email')
    def test_register_user_success(self, mock_send_activation_email):
        response = self.client.post(self.register_url, self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], constants.MESSAGE_CREATED)
        self.assertTrue(MyUser.objects.filter(username='testuser').exists())
        mock_send_activation_email.assert_called_once()

    def test_register_user_invalid_data(self):
        response = self.client.post(self.register_url, self.invalid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], constants.MESSAGE_BAD_REQUEST)
        self.assertFalse(MyUser.objects.filter(email='not-an-email').exists())

    @patch('accounts.utils.EmailHandler.send_email', side_effect=Exception("Email error"))
    def test_register_user_email_error(self, mock_send_email):
        response = self.client.post(self.register_url, self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['message'], constants.MESSAGE_ERROR)
        self.assertTrue(MyUser.objects.filter(username='testuser').exists())
        mock_send_email.assert_called_once()
    