import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from budget_management.users.models import User


class CategoryViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="testusername1")
        cls.user.set_password("testpassword")
        cls.user.save()
        cls.user_data = {
            "username": "testusername1",
            "password": "testpassword",
        }

    def setUp(self):
        response = self.client.post(
            path=reverse("login"),
            data=json.dumps(self.user_data),
            content_type="application/json",
        )
        self.access_token = response.data["token"]["access"]
        self.category_data = {
            "id": 1,
            "category_name": "Food",
            "is_status": "in_use",
        }

    def test_category_list_success(self):
        response = self.client.get(
            path=reverse("category_list"),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_user_fail_to_list_category(self):
        response = self.client.get(
            path=reverse("category_list"),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {"detail": "자격 인증데이터(authentication credentials)가 제공되지 않았습니다."})

    def test_fail_not_existed_category(self):
        self.invalid_category_data = {
            "id": 100,
            "category_name": "invalid_name",
            "is_status": "invalid_status",
        }

        response = self.client.get(
            path=reverse("category_detail", kwargs={"category_id": self.invalid_category_data["id"]}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
