from django import forms
# from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class SteganographyForm(forms.Form):
    image = forms.ImageField()
    message = forms.CharField(max_length=255, required=False, widget=forms.Textarea(attrs={'rows': 3}))
    filename = forms.CharField(max_length=50, required=False, help_text="Enter a name for the encoded image (without extension).")

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hash password
        if commit:
            user.save()
        return user
