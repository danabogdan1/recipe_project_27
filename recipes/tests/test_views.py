import pytest
from django.contrib.auth import get_user_model
from django.test.client import Client

from recipes.models import Recipe

User = get_user_model()

@pytest.fixture
def user(db) -> User:
    u = User.objects.create_user(
        username="test123",
        password="password123"
    )
    return u

@pytest.fixture
def logged_in_client(user, client: Client) -> Client:
    # cream un browser simulat, logat, care poate face requesturi HTTP:
    client.login(
        username="test123",
        password="password123"
    )

    return client

@pytest.fixture
def recipe(user):
    r = Recipe.objects.create(title="Test Recipe", description="Test Recipe Description", cooking_time="20 min", user=user)

    return r

# Testul verifica daca un utilizator autentificat poate sa acceseze pagina principala si daca aceasta se incarca fara erori.
def test_list_all_recipes(logged_in_client):
    response = logged_in_client.get("/")

    assert response.status_code == 200

# Testul verifica daca reteta creata apare pe pagina principala.
def test_recipe_exists(logged_in_client: Client, recipe):
    response = logged_in_client.get("/")

    assert response.status_code == 200
    assert "Test Recipe" in str(response.content)

# Testul verifica daca dupa crearea unei retete se face redirect catre url-ul list_recipes si daca reteta a fost salvata si apartine user-ului corect.
def test_create_recipe(user, logged_in_client: Client):
    response = logged_in_client.post("/recipe/add/", data={"title": "New Test Recipe", "description": "Test Recipe Description", "cooking_time": "20 min"})

    assert response.status_code == 302
    assert Recipe.objects.filter(title="New Test Recipe", user=user).exists()

# Testul verifică dacă un utilizator autentificat poate edita o rețetă existentă și dacă modificările sunt salvate în baza de date.
def test_edit_recipe(recipe, logged_in_client: Client):
    response = logged_in_client.post(f"/recipe/{recipe.pk}/edit/", data={"title": "Updated Recipe", "description": "Updated Description", "cooking_time": "30 min"})

    assert response.status_code == 302
    recipe.refresh_from_db()
    assert recipe.title == "Updated Recipe"

# Testul verifica daca reteta a fost stearsa din baza de date dupa un request HTTP POST.
def test_delete_recipe(user, recipe, logged_in_client: Client):
    response = logged_in_client.post(f"/recipe/{recipe.pk}/delete/")
    assert response.status_code == 302

    response = logged_in_client.post(f"/recipe/{recipe.pk}/delete/")
    assert response.status_code == 404

# Testul verifica daca proprietarul unei retete vede butoanele de Edit si Delete pe pagina retetei.
def test_recipe_owner_sees_edit_delete_buttons(recipe, logged_in_client: Client):
    response = logged_in_client.get(f"/recipe/{recipe.pk}/")

    assert response.status_code == 200
    assert "Edit" in str(response.content)
    assert "Delete" in str(response.content)

# Testul verifica daca retetele sunt afisate in ordine alfabetica.
def test_recipes_alphabetical(user, logged_in_client: Client):
    Recipe.objects.create(title="Waffe Cinnamon Roll", description="Test Recipe Description", cooking_time="20 min", user=user)
    Recipe.objects.create(title="Clafoutis cu afine si banane", description="Test Recipe Description", cooking_time="40 min", user=user)
    response = logged_in_client.get(f"/recipes/alphabetical/")

    assert response.status_code == 200
    content = str(response.content)
    assert content.index("Clafoutis cu afine si banane") < content.index("Waffe Cinnamon Roll")