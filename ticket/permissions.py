from rest_framework.permissions import BasePermission


class FeedbackPermission (BasePermission) : 

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated : 
            state_1 = obj.user == request.user
            if obj.reply_to and hasattr(obj.reply_to,"user") : 
                state_2 = obj.reply_to.user ==request.user
            else : 
                state_2 = False
            return bool( state_1 or state_2 )
        return super().has_object_permission(request, view, obj)