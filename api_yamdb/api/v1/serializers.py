import datetime as dt
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MaxValueValidator
from rest_framework import serializers

from reviews.models import Comment, Review
from titles.models import Category, Genre, Title
from users.models import User


class TokenSerializer(serializers.Serializer):
    """ Token serializer."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=256)

    class Meta:
        fields = ('username', 'confirmation_code')


class AdminSerializer(serializers.ModelSerializer):
    """User model serializer for admin user."""

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User
        unique = ('username', 'email')


class UserSerializer(serializers.ModelSerializer):
    """User model serializer for user."""

    email = serializers.EmailField(
        required=True,
        max_length=254,
    )
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[UnicodeUsernameValidator(), ]
    )

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError('username не может быть "me"')
        return value

    def validate_email(self, email):
        email = email.lower()
        if (
            not User.objects.filter(
                username=self.initial_data.get('username')
            ).exists()
            and User.objects.filter(email=email).exists()
        ):
            raise serializers.ValidationError('email занят.')
        return email

    def validate(self, data):
        """
        Username and email validate.
        """

        username = data.get('username')
        email = data.get('email')

        if User.objects.filter(username=username, email=email).exists():
            return data
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Пользователь c таким username уже существует.'
            )
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь c таким email уже существует.'
            )
        return data

    class Meta(AdminSerializer.Meta):
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):
    """Category model serializer."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Genre model serializer."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleWriteSerializer(serializers.ModelSerializer):
    """Title model serializer."""

    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    year = serializers.IntegerField(
        validators=[MaxValueValidator(dt.date.today().year)]
    )
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre',
            'category', 'rating',
        )


class TitleReadSerializer(serializers.ModelSerializer):
    """Read only title model serializer."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre',
            'category', 'rating',
        )
        read_only_fields = (
            'id', 'name', 'year', 'description', 'genre',
            'category', 'rating',
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Review model serializer."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('title', 'id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('title', 'author')

    def validate(self, attrs):
        request = self.context['request']
        if (request.method == 'POST'
                and request.user.reviews.filter(
                title__id=request.parser_context['kwargs']['title_id']
                ).exists()):
            raise serializers.ValidationError(
                'Можно оставить только один отзыв')

        return attrs


class CommentSerializer(serializers.ModelSerializer):
    """Comment model serializer."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('review', 'id', 'author', 'text', 'pub_date')
        read_only_fields = ('review',)
