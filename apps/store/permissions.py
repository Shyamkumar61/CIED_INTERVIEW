from rest_framework.permissions import BasePermission, DjangoModelPermissions


class MangerPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == "inventory_manager"
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user.role == "inventory_manager"
        return False


class StaffPermission(BasePermission):

    def has_permission(self, request, view):
        print(request.user)
        if request.user.is_authenticated:
            return request.user.role == "med_staff"
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user.role == "med_staff"
        return False
