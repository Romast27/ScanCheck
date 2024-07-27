from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Photo, Feedback


class PhotoForm(forms.ModelForm):
    image = forms.ImageField(label='Choose photo')
    class Meta:
        model = Photo
        fields = ['image']


class FeedbackForm(forms.ModelForm):

    text = forms.CharField(required=False)
    RATES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    rating = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=RATES,
    )

    class Meta:
        model = Feedback
        fields = ['text', 'rating']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
