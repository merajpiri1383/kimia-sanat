from rest_framework.permissions import BasePermission

class IsOwnDriverOrNot (BasePermission) : 

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated : 
            return obj in request.user.drivers.all()