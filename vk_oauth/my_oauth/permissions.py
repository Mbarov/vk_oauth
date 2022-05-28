from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    '''Проверка, является ли пользователь владельцем записи/объекта'''
    def has_object_permission(self, request, view, obj):
        if request.user:
            if obj == request.user: 
                return True
            else:
                return False
        if obj.user == request.user:
            return True
        else:
            return False

