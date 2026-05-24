from rest_framework import serializers
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'status', 'created_by', 'created_at']
