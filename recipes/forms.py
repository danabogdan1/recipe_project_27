from django import forms
from .models import Recipe
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# Formularul folosit pentru crearea si editarea retetelor.
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "description", "cooking_time", "cover_image"]


User = get_user_model()

# Formularul folosit pentru inregistrarea unui utilizator nou.
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")