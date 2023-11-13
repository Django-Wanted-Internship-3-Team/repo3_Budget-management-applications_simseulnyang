from typing import List

from django.urls import URLPattern, path

from budget_management.category.views import CategoryDetailView, CategoryListView

urlpatterns: List[URLPattern] = [
    path("", CategoryListView.as_view(), name="category_list"),
    path("<int:category_id>/", CategoryDetailView.as_view(), name="category_detail"),
]
