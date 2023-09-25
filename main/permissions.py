from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Проверка является ли аутентифицированный пользователь (request.user)
    пользователем из базы данных (obj)
    """

    def has_object_permission(self, request, view, obj):
        if request.method == "GET" or request.user.is_superuser:
            return True
        else:
            return request.user == obj
