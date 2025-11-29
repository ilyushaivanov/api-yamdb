from rest_framework import permissions
from reviews.models import User


class IsAdminOnly(permissions.BasePermission):
    """
    Доступа для аутентифицированного пользователя
    с ролью администратора
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.is_admin
        )
            

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Любой пользователь может выполнять безопасные методы
    Изменяющие методы доступые только админу
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    """
    Права доступа:
    Любой пользователь может выполнять безопасные методы.
    На уровне объекта:
        Автор объекта может изменять его.
        Модераторы и администраторы могут изменять любой объект.
        Все остальные пользователи имеют только права на безопасные методы.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )