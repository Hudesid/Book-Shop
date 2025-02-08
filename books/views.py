from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from .serializers import Book, BookSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import BookLimitOffsetPagination
from .renderers import CustomRenderer, XMLRenderer


class PropertyBasePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.seller


class BookCreateAPIView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookListAPIView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ['title', 'genre', 'author', 'published_at', 'price']
    ordering = ['title']
    search_fields = ['title', 'genre', 'author']
    pagination_class = BookLimitOffsetPagination
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, CustomRenderer, XMLRenderer]


class BookRetrieveAPIView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, CustomRenderer, XMLRenderer]


class BookRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, PropertyBasePermission]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, CustomRenderer, XMLRenderer]




