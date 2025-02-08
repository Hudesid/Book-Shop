from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import Notification, NotificationSerializer
from .paginations import NotificationLimitOffsetPagination
from books.renderers import XMLRenderer, CustomRenderer


class NotificationModelViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = NotificationLimitOffsetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']
    search_fields = ['created_at', 'updated_at']
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, CustomRenderer, XMLRenderer]
