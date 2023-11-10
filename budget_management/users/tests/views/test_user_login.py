import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class LoginViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser1")
        self.user.set_password("testpassword")
        self.user.save()

    def test_validate_with_valid_credentials(self):
        response = self.client.post(
            path=reverse("login"), data=json.dumps({"username": "testuser1", "password": "testpassword"}), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_validate_with_invalid_credentials(self):
        response = self.client.post(
            path=reverse("login"),
            data=json.dumps({"username": "nonexistentuser", "password": "invalidpassword"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_validate_failure_invalid_username(self):
        response = self.client.post(
            path=reverse("login"),
            data=json.dumps({"username": "invalid_username", "password": "testpassword"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_failure_invalid_password(self):
        response = self.client.post(
            path=reverse("login"),
            data=json.dumps({"username": "testuser1", "password": "invalid_password"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_failure_missing_username(self):
        response = self.client.post(path=reverse("login"), data=json.dumps({"password": "testpassword"}), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_validate_failure_missing_password(self):
        response = self.client.post(path=reverse("login"), data=json.dumps({"username": "testuser1"}), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
