from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    InventoryListView, 
    IngredientDeleteView, 
    MenuListView, 
    PurchaseListView, 
    FinancialSummaryView, 
    IngredientUpdateView, 
    MenuItemCreateView, 
    IngredientCreateView, 
    RecipeRequirementCreateView, 
    PurchaseCreateView,
    MenuItemUpdateView,
    MenuItemDeleteView
)

urlpatterns = [
    path('', login_required(InventoryListView.as_view()), name='home'),
    path('', InventoryListView.as_view(), name='home'),
    path('inventory/<pk>/delete/', IngredientDeleteView.as_view(), name='ingredient-delete'),
    path('ingredient/<int:pk>/edit/', IngredientUpdateView.as_view(), name='ingredient-edit'),
    path('ingredient/add/', IngredientCreateView.as_view(), name='ingredient-add'),
    path('menu/', MenuListView.as_view(), name='menu-list'),
    path('menu/add/', MenuItemCreateView.as_view(), name='menu-add'),
    path('menu/<int:pk>/edit/', MenuItemUpdateView.as_view(), name='menu-edit'),
    path('menu/<int:pk>/delete/', MenuItemDeleteView.as_view(), name='menu-delete'),
    path('recipe/add/', RecipeRequirementCreateView.as_view(), name='recipe-add'),
    path('purchases/', PurchaseListView.as_view(), name='purchase-list'),
    path('purchase/add/', PurchaseCreateView.as_view(), name='purchase-add'),
    path('financial-summary/', FinancialSummaryView.as_view(), name='financial-summary'),
]