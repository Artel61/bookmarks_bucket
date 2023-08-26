from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .serializers import CreateUserSerializer, OutputUserSerializer


def register_user(serializer: CreateUserSerializer) -> OutputUserSerializer:
    data = serializer.data
    new_user = User.objects.create(
        username=data['email'],
        email=data['email'],
    )
    new_user.set_password(data['password'])
    new_user.save()

    token = Token.objects.create(user=new_user)

    resp = OutputUserSerializer(
        data={
            "user_id": new_user.pk,
            "user_token": token.key,
        },
    )
    resp.is_valid(raise_exception=False)
    return resp
