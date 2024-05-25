from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it and view it.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user

class IsTransportista(BasePermission):
    """
    Custom permission to only allow transportistas to view and edit their own objects.
    """
    def has_object_permission(self, request, view, obj):
        return obj.es_transportista

class IsCliente(BasePermission):
    """
    Custom permission to only allow clients to view and edit their own objects.
    """
    def has_object_permission(self, request, view, obj):
        return obj.es_cliente