from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="예산 관리 어플리케이션",
        default_version="v1",
        description="원티드 프리온보딩 Mission3. 개인 프로젝트",
        contact=openapi.Contact(email="happysseul627@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # API
    path("api/users/", include("budget_management.users.urls")),
    # Swagger
    path("swagger/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
