from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_recipes, name="list_recipes"),
    path("recipes/alphabetical/", views.list_recipes_alphabetical, name="list_recipes_alphabetical"),
    path("recipes/by_date/", views.list_recipes_by_date, name="list_recipes_by_date"),
    path("recipe/add/", views.create_recipe, name="recipe_add"),
    path("recipe/<int:id>/edit/", views.update_recipe, name="recipe_edit"),
    path("recipe/<int:id>/delete/", views.delete_recipe, name="recipe_delete"),
    path("recipe/<int:id>/", views.recipe_detail, name="recipe_detail"),
    path("register/", views.register_user, name="register_user"),

]

