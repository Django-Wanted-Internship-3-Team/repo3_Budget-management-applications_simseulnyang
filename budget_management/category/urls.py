from typing import List

from django.urls import URLPattern, path

from budget_management.category.views import CategoryListView

urlpatterns: List[URLPattern] = [
    path("", CategoryListView.as_view(), name="category_list"),
]
