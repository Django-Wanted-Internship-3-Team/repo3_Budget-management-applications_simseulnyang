from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from budget_management.category.models import Category
from budget_management.category.serializers import (
    CategoryQuerySerializer,
    CategorySerializer,
)


class CategoryListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="사용자 카테고리 목록 조회",
        responses={
            status.HTTP_200_OK: CategorySerializer,
            status.HTTP_404_NOT_FOUND: "카테고리가 없습니다.",
        },
    )
    def get(self, request: Request) -> Response:
        """
        사용자가 사용중인 카테고리 정보를 조회합니다.

        Returns:
            id (int) : 카테고리 id
            category_name (str) : 카테고리명
            is_status (str) : 사용 또는 사용중지 여부
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="카테고리 상세 보기",
        query_serializer=CategoryQuerySerializer,
        responses={
            status.HTTP_200_OK: CategorySerializer,
            status.HTTP_404_NOT_FOUND: "카테고리가 없습니다.",
        },
    )
    def get(self, request: Request, category_id: int) -> Response:
        """
        카테고리의 상세 내용을 확인합니다.

        Args:
            category_id (int, required): 카테고리 ID

        return:
            id (int) : 카테고리 id
            category_name (str) : 카테고리명
            is_status (str) : 사용 또는 사용중지 여부
        """
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response("카테고리가 없습니다.", status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
