from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from . import serializers
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import BasePermission, IsAuthenticated
from .paginations import OrderLimitOffsetPagination
from books.renderers import CustomRenderer, XMLRenderer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView


class PropertyBasePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class OrderCreateAPIView(CreateAPIView):
    queryset = serializers.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [IsAuthenticated]


class OrderListAPIView(ListAPIView):
    queryset = serializers.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = OrderLimitOffsetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ['created_at', 'updated_at', 'status']
    ordering = ['created_at']
    search_fields = ['books']
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, CustomRenderer, XMLRenderer]


class OrderRetrieveAPIView(RetrieveAPIView):
    queryset = serializers.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, CustomRenderer, XMLRenderer]


class OrderRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = serializers.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [IsAuthenticated, PropertyBasePermission]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, CustomRenderer, XMLRenderer]