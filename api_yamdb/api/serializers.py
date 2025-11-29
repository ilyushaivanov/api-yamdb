from rest_framework import serializers
from .models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id')
            user = self.context['request'].user
            if Review.objects.filter(title_id=title_id, author=user).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили отзыв на это произведение.'
                )
        return data

    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'score', 'pub_date']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'pub_date']
