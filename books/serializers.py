from rest_framework import serializers
from .models import Book
from users.serializers import UserForGetSerializer


class BookSerializer(serializers.ModelSerializer):
    seller = UserForGetSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'seller', 'genre', 'published_at', 'price', 'description', 'created_at', 'updated_at')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['seller'] = UserForGetSerializer(instance.seller, read_only=True).data
        return representation

    def create(self, validated_data):
        book = Book.objects.create(seller=self.context['request'].user, **validated_data)
        return book

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            instance.seller = self.context['request'].user
        instance.save()
        return instance