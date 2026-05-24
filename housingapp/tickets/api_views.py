from rest_framework import generics, permissions

from .models import Ticket
from .serializers import TicketSerializer


class IsOwnerOrTenant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class TicketListAPIView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsOwnerOrTenant]

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, 'profile', None) and user.profile.role
        if role == 'owner':
            return Ticket.objects.with_creator().newest_first()
        return Ticket.objects.for_user(user).newest_first()
