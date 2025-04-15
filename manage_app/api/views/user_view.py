from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from manage_app.api.serializers.user_serializer import UserSerializer


class UserApiView(APIView):
    permission_classes = (IsAuthenticated, )

    @extend_schema(
        summary="Получить информацию о пользователе, который делает запрос",
        description="Метод возвращает информацию о пользователе, который делает запрос",
        responses={200: UserSerializer},
        tags=["Users"],
    )
    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)
