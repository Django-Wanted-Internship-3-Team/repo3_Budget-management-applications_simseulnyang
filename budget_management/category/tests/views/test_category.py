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
            "category_name": "Food",
            "category_info": "Expenses on food",
            "is_status": "in_use",
        }

    def test_category_list_success(self):
        response = self.client.get(
            path=reverse("category_list"),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_delete_category_success(self):
    #     valid_category_data = self.category_data.copy()
    #     valid_category_data["is_status"] = "deleted"

    #     response = self.client.patch(
    #         path=reverse("category_deleted"),
    #         data=json.dumps(valid_category_data),
    #         content_type="application/json",
    #         HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_delete_category_fail_invalid_status(self):
    #     invalid_category_data = self.category_data.copy()
    #     invalid_category_data["is_status"] = "invalid_status"

    #     response = self.client.patch(
    #         path=reverse("category_deleted"),
    #         data=json.dumps(invalid_category_data),
    #         content_type="application/json",
    #         HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
