from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
# Modelul Recipe defineste structura unei retete culinare.
# Fiecare reteta apartine unui utilizator si contine informatii despre titlu, descriere, data de adaugare si timp de gatire.


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    created_at = models.DateTimeField(auto_now_add=True)
    cooking_time = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='recipes/', blank=True, null=True)

    def __str__(self):
        return f"Recipe {self.title}"

