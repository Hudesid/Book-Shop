from django.urls import path
from . import views


urlpatterns = [
    path('orders/create/', views.OrderCreateAPIView.as_view(), name='order-create'),
    path('orders/', views.OrderListAPIView.as_view(), name='order-list'),
    path('order/detail/<int:pk>/', views.OrderRetrieveAPIView.as_view(), name='order-detail'),
    path('my/order/detail/<int:pk>/', views.OrderRetrieveUpdateDestroyAPIView.as_view(), name='my-order')
]