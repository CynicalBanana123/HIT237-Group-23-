from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description"]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Short summary'}),
            'description': forms.Textarea(attrs={'rows': 6}),
        }
