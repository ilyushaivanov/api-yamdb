from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer
from .permissions import IsAuthorOrModeratorOrAdmin


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrModeratorOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title__id']

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title_id=title_id)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        serializer.save(author=self.request.user, title_id=title_id)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев."""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrModeratorOrAdmin]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return Comment.objects.filter(review_id=review_id)

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        serializer.save(author=self.request.user, review_id=review_id)
