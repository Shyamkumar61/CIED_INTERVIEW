from typing import Any
from rest_framework import generics
from apps.account.apis.serializers import (
    LoginSerializer,
    CreateMedBillAccountSerializer,
    AccountSerializer,
)
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.account.models import Account
from apps.account.permissions import AccountPermissions
from rest_framework import status
from rest_framework.response import Response


class ResponseInfo:

    def __init__(self, **args) -> None:
        self.response = {
            "status": args.get("status", True),
            "status_code": args.get("status_code", ""),
            "data": args.get("data", {}),
            "message": args.get("message", ""),
        }


class RegisterUserView(generics.CreateAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = [
        IsAuthenticated,
        AccountPermissions,
    ]
    serializer_class = CreateMedBillAccountSerializer


class LogoutView(generics.GenericAPIView):
    authentication_classes = (JWTAuthentication,)

    def __init__(self, *args, **kwargs):
        self.response_format = ResponseInfo().response
        super().__init__(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            if request.user.is_authenticated:
                token.blacklist()
                self.response_format["status"] = True
                self.response_format["status_code"] = status.HTTP_200_OK
                self.response_format["message"] = "User Logout Successfull"
                return Response(self.response_format, status=status.HTTP_200_OK)
        except Exception as e:
            self.response_format["status"] = False
            self.response_format["status_code"] = status.HTTP_400_BAD_REQUEST
            self.response_format["message"] = str(e)
            return Response(self.response_format, status=status.HTTP_404_NOT_FOUND)


class UserListView(generics.ListAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, AccountPermissions)
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, AccountPermissions)
    serializer_class = AccountSerializer

    def get_object(self):
        queryset = get_object_or_404(Account, pk=self.kwargs.get("pk"))
        return queryset
