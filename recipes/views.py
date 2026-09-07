from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower

from .forms import RecipeForm, RegisterForm
from .models import Recipe


# Create your views here.

# Functions that manage our web pages.

def register_user(request: HttpRequest):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            # aici se creaza user-ul in baza de date, folosind metoda .save()
            user = form.save()
            # user-ul este autentificat automat
            login(request, user)

            return redirect("list_recipes")
    else:
        form = RegisterForm()

    return render(request, 'recipes/register.html', {"form": form})

def logout_user(request: HttpRequest):
    logout(request)
    return redirect('list_recipes')

# function-based view:
# CRUD: Create, Read, Update, Delete.

# Afisam toate retetele din baza de date in ordinea adaugarii lor.
def list_recipes(request: HttpRequest):
    recipes = Recipe.objects.all().order_by("pk")

    return render(request, "recipes/home.html", context={"recipes": recipes})

@login_required
def create_recipe(request: HttpRequest):
    # Verificam daca reteta a fost trimisa.
    if request.method == "POST":
        form = RecipeForm(request.POST)

        if form.is_valid():
            # Cream o reteta in baza de date.
            recipe = form.save(commit=False)
            # Asociem reteta cu utilizatorul autentificat.
            recipe.user = request.user
            # Salvam reteta in baza de date.
            recipe.save()

            return redirect("list_recipes")
    else:
        form = RecipeForm()

    return render(request, "recipes/create_recipe.html", context={"form": form})

@login_required
def update_recipe(request: HttpRequest, id: int):
    # Cautam reteta dupa ID sau afisam eroare 404 daca nu exista.
    recipe = get_object_or_404(Recipe, pk=id)

    # Verificam daca utilizatorul autentificat este proprietarul retetei.
    if request.user.pk == recipe.user.pk:

        if request.method == "POST":
            form = RecipeForm(request.POST, instance=recipe)

            if form.is_valid():
                form.save()
                return redirect("list_recipes")

        else:
            form = RecipeForm(instance=recipe)

        return render(request, "recipes/recipe_form.html", context={"form": form})

    else:
        return HttpResponse("You are not allowed to edit another user's recipe.")


@login_required
def delete_recipe(request: HttpRequest, id: int):
    recipe = get_object_or_404(Recipe, pk=id)

    # Doar utilizatorul care a creat reteta o poate sterge.
    if request.user.pk == recipe.user.pk:
        if request.method == "POST":
            recipe.delete()
            return redirect("list_recipes")

        else:
            return render(request, "recipes/recipe_confirm_delete.html", context={"recipe": recipe})
    else:
        return HttpResponse("You are not allowed to delete another user's recipe.")

def recipe_detail(request: HttpRequest, id: int):
    # Afisam detaliile unei singure retete.
    recipe = get_object_or_404(Recipe, pk=id)

    return render(request, "recipes/recipe_detail.html", context={"recipe": recipe})

def list_recipes_alphabetical(request: HttpRequest):
    # Afisam retetele in ordine alfabetica.
    recipes = Recipe.objects.all().order_by(Lower("title"))
    return render(request, "recipes/home.html", context={"recipes": recipes})


def list_recipes_by_date(request: HttpRequest):
    # Afisam retetele dupa data crearii de la cea mai veche la cea mai noua.
    recipes = Recipe.objects.all().order_by("created_at")

    return render(request, "recipes/home.html", context={"recipes": recipes})

