from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from unittest.mock import patch


class RegisterAPITests(APITestCase):
    def setUp(self):
        self.url = reverse('register-list')

    def test_successful_registration(self):
        data = {
            "username": "user1",
            "first_name": "Ali",
            "last_name": "Ahmadi",
            "national_code": "1234567890",
            "phone": "09123456789",
            "password": "testpass"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)

    def test_invalid_national_code(self):
        data = {
            "username": "user2",
            "first_name": "Ali",
            "last_name": "Ahmadi",
            "national_code": "1234",
            "phone": "09123456789",
            "password": "testpass"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("national_code", str(response.data))

    def test_duplicate_national_code(self):
        User.objects.create_user(
            username="existinguser",
            first_name="Ali",
            last_name="Ahmadi",
            national_code="1234567890",
            phone="09120000000",
            password="testpass"
        )
        data = {
            "username": "user3",
            "first_name": "Ali",
            "last_name": "Ahmadi",
            "national_code": "1234567890",
            "phone": "09121111111",
            "password": "testpass"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("national_code", str(response.data))

    def test_missing_required_fields(self):
        data = {
            "username": "user4",
            "national_code": "1234567890"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("first_name", str(response.data))
        self.assertIn("last_name", str(response.data))
        self.assertIn("phone", str(response.data))
        self.assertIn("password", str(response.data))

    def test_internal_server_error(self):
        data = {
            "username": "user5",
            "first_name": "Ali",
            "last_name": "Ahmadi",
            "national_code": "9876543210",
            "phone": "09120000001",
            "password": "testpass"
        }
        with patch('users.serializers.UserRegisterSerializer.save', side_effect=Exception("DB error")):
            response = self.client.post(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
            self.assertIn("error", response.data)

    def test_duplicate_username(self):
        User.objects.create_user(
            username="userdup",
            first_name="Test",
            last_name="User",
            national_code="1111111111",
            phone="09120000002",
            password="testpass"
        )
        data = {
            "username": "userdup",
            "first_name": "Another",
            "last_name": "Person",
            "national_code": "2222222222",
            "phone": "09120000003",
            "password": "testpass"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", str(response.data))

    def test_phone_too_long(self):
        data = {
            "username": "user6",
            "first_name": "Ali",
            "last_name": "Ahmadi",
            "national_code": "3333333333",
            "phone": "12345678901234567890",
            "password": "testpass"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("phone", str(response.data))

    def test_blank_fields(self):
        data = {
            "username": "",
            "first_name": "",
            "last_name": "",
            "national_code": "",
            "phone": "",
            "password": ""
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("first_name", str(response.data))
        self.assertIn("last_name", str(response.data))
        self.assertIn("national_code", str(response.data))
        self.assertIn("phone", str(response.data))
        self.assertIn("password", str(response.data))

    def test_non_digit_national_code(self):
        data = {
            "username": "user7",
            "first_name": "Ali",
            "last_name": "Ahmadi",
            "national_code": "abc1234567",
            "phone": "09123456780",
            "password": "testpass"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("national_code", str(response.data))
