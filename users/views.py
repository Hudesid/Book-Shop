from django.db import transaction
from django.utils import timezone
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from .serializers import UserSerializer, User, CustomTokenObtainPairSerializer, UserForGetSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import UserToken
from books.renderers import CustomRenderer, XMLRenderer


class PropertyBasePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = UserToken.objects.create(user=user)
            verification_link = reverse('verify-email', kwargs={'pk': user.id, 'token': token.token})
            current_site = get_current_site(request).domain
            full_link = f"http://{current_site}{verification_link}"
            message = f"Sizning emailgizdan Book shop dan ro'yxatdan o'tildi. Ushbu link orqali saytga o'tsangiz bo'ladi: {full_link}"
            try:
                send_mail(
                    'Book shop dan habar',
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False
                )
            except Exception as e:
                return Response({"message": f"Error sending email: {str(e)}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "fist_name": user.first_name,
                    "last_name": user.last_name,
                    "message": "User created and verification email sent."},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserForGetSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, CustomRenderer, XMLRenderer]


class MyProfileRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [PropertyBasePermission, IsAuthenticated]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, CustomRenderer, XMLRenderer]

    def update(self, request, *args, **kwargs):
        old_user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if old_user.email != user.email:
                token = UserToken.objects.create(user=user)
                verification_link = reverse('verify-email', kwargs={'pk': user.id, 'token': token.token})
                current_site = get_current_site(request).domain
                full_link = f"http://{current_site}{verification_link}"
                message = f"Email ni tasdiqlash uchun shu link bo'yicha saytga o'tsangiz bo'ladi: {full_link}"
                send_mail(
                    'Book shop dan habar',
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False
                )
                return Response(
                    {"message": "User created and verification email sent."},
                    status=status.HTTP_200_OK
            )
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        if not email:
            raise ValidationError("Email is required.")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("No user found with this email address.")

        token = UserToken.objects.create(user=user)
        verification_link = reverse('recovery-password', kwargs={'pk': user.id, 'token': token.token})
        current_site = get_current_site(request).domain
        full_link = f"http://{current_site}{verification_link}"
        message = f"Yangi password kiritish uchun shu link ni bo'yicha o'ting: {full_link}"

        try:
            send_mail(
                'Book shop dan habar',
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )
        except Exception as e:
            raise ValidationError(f"An error occurred while sending the email: {str(e)}")

        return Response(
            {"message": "Password recovery email sent."},
            status=status.HTTP_200_OK
        )


class RecoveryPasswordAPIView(APIView):
    def post(self, request, pk=None, token=None, *args, **kwargs):
        new_password = request.data.get('new_password')
        token_data = UserToken.objects.get(token=token)
        if token is None:
            return Response({'message': 'Token must be.'}, status=status.HTTP_400_BAD_REQUEST)
        if not token_data:
            return Response({'message': 'The token is wrong'}, status=status.HTTP_400_BAD_REQUEST)
        elif token_data.expires_at < timezone.now():
            token_data.delete()
            return Response({'message': 'Token has expired and token deleted.'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=pk)
        if user is None:
            return Response({'message': "User with this ID not found"}, status=status.HTTP_404_NOT_FOUND)
        user.set_password(new_password)
        user.save()
        return Response({'message': "Password successfully updated"})


class VerifyEmailAPIView(APIView):
    def get(self, request, pk, token, *args, **kwargs):
        try:
            user = User.objects.get(id=pk)
            token = UserToken.objects.get(token=token, user=user)
        except User.DoesNotExist:
            return Response({'message': 'The user ID is wrong'}, status=status.HTTP_400_BAD_REQUEST)
        except UserToken.DoesNotExist:
            return Response({'message': 'The token is wrong'}, status=status.HTTP_400_BAD_REQUEST)

        if token.expires_at <= timezone.now() and not user.is_verify_email:
            with transaction.atomic():
                token.delete()
                user.delete()
            return Response({'message': 'Token has expired and user is deleted'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.is_verify_email = True
        user.save()

        return Response({'message': 'Token verified successfully'}, status=status.HTTP_200_OK)


class CustomTokenObtainPairAPIView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


