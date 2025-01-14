from django.urls import path
from .views import InventoryListView, IngredientDeleteView, MenuListView, PurchaseListView, FinancialSummaryView # DashboardView


urlpatterns = [
    path('', InventoryListView.as_view(), name='home'),
    # path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('inventory/<pk>/delete/', IngredientDeleteView.as_view(), name='ingredient-delete'),
    path('menu/', MenuListView.as_view(), name='menu-list'),
    path('purchases/', PurchaseListView.as_view(), name='purchase-list'),
    path('financial-summary/', FinancialSummaryView.as_view(), name='financial-summary'),
]