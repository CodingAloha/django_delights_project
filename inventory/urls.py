from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import (
    FinancialSummaryView,
    IngredientCreateView,
    IngredientDeleteView,
    IngredientUpdateView,
    InventoryListView,
    MenuItemCreateView,
    MenuItemDeleteView,
    MenuItemUpdateView,
    MenuListView,
    PurchaseCreateView,
    PurchaseDeleteView,
    PurchaseListView,
    PurchaseUpdateView,
    RecipeRequirementCreateView,
    RecipeRequirementDeleteView,
    RecipeRequirementListView,
    RecipeRequirementUpdateView,
)

urlpatterns = [
    path("", InventoryListView.as_view(), name="home"),
    path("ingredient/add/", IngredientCreateView.as_view(), name="ingredient-add"),
    path(
        "ingredient/<int:pk>/edit/",
        IngredientUpdateView.as_view(),
        name="ingredient-edit",
    ),
    path(
        "inventory/<int:pk>/delete/",
        IngredientDeleteView.as_view(),
        name="ingredient-delete",
    ),
    path("menu/", MenuListView.as_view(), name="menu-list"),
    path("menu/add/", MenuItemCreateView.as_view(), name="menu-add"),
    path("menu/<int:pk>/edit/", MenuItemUpdateView.as_view(), name="menu-edit"),
    path("menu/<int:pk>/delete/", MenuItemDeleteView.as_view(), name="menu-delete"),
    path("purchases/", PurchaseListView.as_view(), name="purchase-list"),
    path("purchase/add/", PurchaseCreateView.as_view(), name="purchase-add"),
    path("purchase/<int:pk>/edit/", PurchaseUpdateView.as_view(), name="purchase-edit"),
    path(
        "purchase/<int:pk>/delete/",
        PurchaseDeleteView.as_view(),
        name="purchase-delete",
    ),
    path(
        "menu/<int:pk>/recipe/",
        RecipeRequirementListView.as_view(),
        name="recipe-requirements",
    ),
    path("recipe/add/", RecipeRequirementCreateView.as_view(), name="recipe-add"),
    path(
        "recipe/<int:pk>/edit/",
        RecipeRequirementUpdateView.as_view(),
        name="recipe-edit",
    ),
    path(
        "recipe/<int:pk>/delete/",
        RecipeRequirementDeleteView.as_view(),
        name="recipe-delete",
    ),
    path(
        "financial-summary/", FinancialSummaryView.as_view(), name="financial-summary"
    ),
]
