from django.shortcuts import render
from decimal import Decimal
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase


# class DashboardView(TemplateView):
#     template_name = "dashboard.html"  # Specify the template

#     def get_context_data(self, **kwargs):
#         # Get the default context
#         context = super().get_context_data(**kwargs)

#         # Add custom data
#         context['inventory'] = Ingredient.objects.all()  # All ingredients in inventory
#         context['purchases'] = Purchase.objects.all()  # All purchases
#         context['menu_items'] = MenuItem.objects.all()  # All menu items

#         # Calculate total revenue
#         total_revenue = sum(
#             purchase.menu_item.price * purchase.quantity for purchase in Purchase.objects.all()
#         )
#         context['total_revenue'] = total_revenue

#         # Calculate total cost
#         total_cost = Decimal(0)
#         for purchase in Purchase.objects.all():
#             requirements = RecipeRequirement.objects.filter(menu_item=purchase.menu_item)
#             for req in requirements:
#                 total_cost += Decimal(req.quantity_required) * req.ingredient.unit_price * purchase.quantity
#         context['total_cost'] = total_cost

#         # Calculate profit
#         context['profit'] = total_revenue - total_cost

#         return context

class InventoryListView(ListView):
    model = Ingredient
    template_name = 'inventory/inventory_list.html'
    context_object_name = 'ingredients'

class IngredientDeleteView(DeleteView):
    model = Ingredient
    template_name = 'inventory/ingredient_confirm_delete.html'
    success_url = reverse_lazy('inventory-list')

class MenuListView(ListView):
    model = MenuItem
    template_name = 'inventory/menu_list.html'
    context_object_name = 'menu_items'

class PurchaseListView(ListView):
    model = Purchase
    template_name = 'inventory/purchase_list.html'
    context_object_name = 'purchases'

class FinancialSummaryView(TemplateView):
    template_name = 'inventory/financial_summary.html'  # Points to your template

    def get_context_data(self, **kwargs):
        # Get the default context
        context = super().get_context_data(**kwargs)

        # Calculate total revenue
        total_revenue = sum(
            purchase.menu_item.price * purchase.quantity for purchase in Purchase.objects.all()
        )
        context['total_revenue'] = total_revenue

        # Calculate total cost
        total_cost = Decimal(0)
        for purchase in Purchase.objects.all():
            requirements = RecipeRequirement.objects.filter(menu_item=purchase.menu_item)
            for req in requirements:
                total_cost += Decimal(req.quantity_required) * req.ingredient.unit_price * purchase.quantity
        context['total_cost'] = total_cost

        # Calculate profit
        context['profit'] = total_revenue - total_cost

        return context
