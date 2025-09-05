from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Cho phép truy cập nếu user là admin
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"

class IsCustomer(BasePermission):
    """
    Cho phép truy cập nếu user là customer
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "customer"
