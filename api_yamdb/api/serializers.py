from rest_framework import serializers
from django.core.exceptions import ValidationError
from reviews.models import Category, Genre, Title, User
from reviews.validator import username_validator


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validator=[username_validator]
    )
    email = serializers.EmailField(
        required=True,
        max_length=254
    )

    def validate(self, data):
        username = data.get("username")
        email = data.get("email")
        if User.objects.filter(username=username, email=email).exists():
            return data
        if User.objects.filter(username=username).exists():
            raise ValidationError("Этот логин уже занят")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Эта почта уже занята")
        return data

    class Meta:
        model = User
        fields = ['username', 'email', 'bio',
                  'first_name', 'last_name', 'role']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
