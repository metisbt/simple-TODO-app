from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from accounts.models import Profile
from django.shortcuts import get_object_or_404
from .serializers import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    ChangePasswordApiSerializer,
    ProfileSerializer,
    TokenObtainPairSerializer,
    ActivationResendSerializer,
)
# for JWT
from rest_framework_simplejwt.views import TokenObtainPairView
# for send simple emails
# from django.core.mail import send_mail
# for send customize emails
from mail_templated import send_mail
# customize email send with treading
from mail_templated import EmailMessage
from ..utils import EmailThread
# for generate token manually
from rest_framework_simplejwt.tokens import RefreshToken
# for decode simplejwt token
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from django.conf import settings

User = get_user_model()

# for register user and send registration email
class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data['email']
            data = {
                'email':email,
            }
            # generate token manually
            user_obj = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user_obj)
            # customize email send with treading
            email_obj = EmailMessage(
                'email/activation_email.tpl',
                {'token':token},
                'admin@admin.com',
                to=[email],
            )
            EmailThread(email_obj).start()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

# for email confirmation
class ActivationApiView(APIView):

    def post(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithm =['HS256'])
            user_id = token.get("user_id")
        # if token expired
        except ExpiredSignatureError:
            return Response(
                {"details": "toke has been expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        # if token not valid
        except InvalidSignatureError:
            return Response(
                {"details": "toke is not valid"}, status=status.HTTP_400_BAD_REQUEST
            )
        # object user
        user_obj = User.objects.get(pk=user_id)
        if user_obj.is_verified:
            return Response(
                {"detail": "your account has already verified"},
                status=status.HTTP_200_OK,
            )
        # is_verified -> True
        user_obj.is_verified = True
        user_obj.save()
        # valid response ok
        return Response(
            {"detail": "your account have been verified and activated successfully"},
            status=status.HTTP_200_OK,
        )
    
# for resend email registration token
class ActivationResendApiView(APIView):
    serializer_class = ActivationResendSerializer

    def post(self, request, *args, **kwargs):
        serializer = ActivationResendSerializer(data=request.date)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user_obj)
        # customize email send with treading
        email_obj = EmailMessage(
            "email/activation_email.tpl",
            {"token": token},
            "admin@admin.com",
            to=[user_obj.email],
        )
        EmailThread(email_obj).start()
        return Response(
            {"detail": "user activation resend successfully"}, status=status.HTTP_200_OK
        )

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
# for change password
class ChangePasswordApiView(generics.GenericAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordApiSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    
    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            return Response(
                {"detail": "Password updated successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# for login with token
class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, 'user_id': user.pk, 'email': user.email})
    
# for token logout
class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# for login with jwt
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

# for profile
class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj