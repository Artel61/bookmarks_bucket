from drf_yasg import openapi
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .authentication import CsrfExemptSessionAuthentication
from .serializers import CreateUserSerializer, OutputUserSerializer
from .utils import register_user


output = {
    status.HTTP_200_OK: openapi.Response('Результат регистрации', OutputUserSerializer),
}


class RegisterUserView(APIView):
    """Регистрация пользователя"""
    authentication_classes = [CsrfExemptSessionAuthentication]

    # @swagger_auto_schema(method='POST', request_body=CreateUserSerializer, responses=output)
    def post(self, request: Request) -> Response:
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        resp = register_user(serializer)
        return Response(resp.data, status=status.HTTP_201_CREATED)
