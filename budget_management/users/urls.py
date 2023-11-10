from typing import List

from django.urls import URLPattern, path

from budget_management.users.views import SignupView

urlpatterns: List[URLPattern] = [
    path("signup/", SignupView.as_view(), name="signup"),
]
