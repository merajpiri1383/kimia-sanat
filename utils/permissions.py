from rest_framework.permissions import BasePermission


class IsOwnOrNot (BasePermission) :

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated : 
            if request.user == obj.user : 
                return  True
            else : 
                return request.user.is_staff
        else :
            return False
        

class IsActiveOrNot (BasePermission) : 

    def has_permission(self, request, view):
        if request.user.is_authenticated : 
            return request.user.is_real or request.user.is_legal or request.user.is_staff
        else : 
            return False