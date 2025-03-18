from rest_framework.permissions import DjangoModelPermissions, BasePermission


class AccountPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser or request.user["role"] == "admin":
            return True
        return False
