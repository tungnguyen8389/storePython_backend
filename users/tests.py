from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Tạo user admin và customer
        self.admin_user = User.objects.create_user(
            username="admin",
            password="admin123",
            role="admin"
        )
        self.customer_user = User.objects.create_user(
            username="customer",
            password="cust123",
            role="customer"
        )

    def test_register_user(self):
        data = {
            "username": "newuser",
            "password": "newpass123",
            "email": "newuser@mail.com",
            "role": "customer"
        }
        response = self.client.post(reverse("register"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["username"], "newuser")

    def test_login_user(self):
        data = {
            "username": "customer",
            "password": "cust123"
        }
        response = self.client.post(reverse("login"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_profile_requires_authentication(self):
        # chưa login => 401
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_access(self):
        # login bằng admin
        login = self.client.post(reverse("login"), {"username": "admin", "password": "admin123"}, format="json")
        token = login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

        response = self.client.get(reverse("admin-test"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_cannot_access_admin(self):
        # login bằng customer
        login = self.client.post(reverse("login"), {"username": "customer", "password": "cust123"}, format="json")
        token = login.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

        response = self.client.get(reverse("admin-test"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
