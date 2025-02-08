from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from . import views
from rest_framework_simplejwt.views import TokenRefreshView


schema_view = get_schema_view(
   openapi.Info(
      title="Book-shop",
      default_version='v1',
      description="Bookstore website where you can buy books",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@myapi.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('user/register/', views.UserCreateAPIView.as_view(), name='user-register'),
    path('user/login/', views.CustomTokenObtainPairAPIView.as_view(), name='login'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('user/verify-email/<int:pk>/<str:token>/', views.VerifyEmailAPIView.as_view(), name='verify-email'),
    path('user/forgot/password/', views.ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('user/recovery/password/<int:pk>/<str:token>/', views.RecoveryPasswordAPIView.as_view(), name='recovery-password'),
    path('user/profile/<int:pk>/', views.UserRetrieveAPIView.as_view(), name='user-profile'),
    path('my/profile/<int:pk>/', views.MyProfileRetrieveUpdateDestroyAPIView.as_view(), name='my-profile'),
    path('swagger/', schema_view.as_view(), name='swagger-docs'),
]