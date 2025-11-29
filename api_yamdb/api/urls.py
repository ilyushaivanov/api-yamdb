from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..reviews import views

router = DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
