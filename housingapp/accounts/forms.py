from django import forms
from django.contrib.auth import authenticate, get_user_model


class MixedLoginForm(forms.Form):
    username = forms.CharField(label='Username or Email')
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        username = cleaned.get('username')
        password = cleaned.get('password')
        if username and password:
            User = get_user_model()
            user = authenticate(username=username, password=password)
            if user is None:
                # try looking up by email
                try:
                    u = User.objects.get(email__iexact=username)
                    user = authenticate(username=u.get_username(), password=password)
                except User.DoesNotExist:
                    user = None
            if user is None:
                raise forms.ValidationError('Invalid credentials')
            if not user.is_active:
                raise forms.ValidationError('This account is inactive.')
            self.user_cache = user
        return cleaned

    def get_user(self):
        return self.user_cache
