from rest_framework import serializers
from .models import Order
from books.serializers import BookSerializer
from users.serializers import UserForGetSerializer

#
# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ('id', 'book', 'created_at', 'updated_at', 'quantity')
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['book'] = BookSerializer(instance.book).data
#         return representation


class OrderSerializer(serializers.ModelSerializer):
    # total_price = serializers.SerializerMethodField()
    user = UserForGetSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'book', 'created_at', 'updated_at', 'status', 'quantity')

    # def get_total_price(self, obj):
    #     total = 0
    #     for item in obj.order_items.all():
    #         total += item.quantity * item.book.price
    #     return total

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserForGetSerializer(instance.user).data
        representation['book'] = BookSerializer(instance.book).data
        return representation

    def create(self, validated_data):
        order = Order.objects.create(user=self.context['request'].user, **validated_data)
        return order



