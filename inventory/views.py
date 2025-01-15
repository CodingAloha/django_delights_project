from django.shortcuts import render
from decimal import Decimal
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from .forms import MenuItemForm, IngredientForm, RecipeRequirementForm, PurchaseForm
from datetime import datetime


class InventoryListView(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = 'inventory/inventory_list.html'
    context_object_name = 'ingredients'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_year'] = datetime.now().year
        return context

class IngredientCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'inventory/ingredient_form.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Ingredient'
        context['button_text'] = 'Add Ingredient'
        return context

class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingredient
    template_name = 'inventory/ingredient_confirm_delete.html'
    success_url = reverse_lazy('home')

class IngredientUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Ingredient
    fields = ['name', 'quantity', 'unit', 'unit_price']
    template_name = 'inventory/ingredient_form.html'
    success_url = reverse_lazy('home')
    success_message = "Ingredient updated successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Ingredient'
        context['button_text'] = 'Save Changes'
        return context
    
class MenuListView(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = 'inventory/menu_list.html'
    context_object_name = 'menu_items'

class MenuItemUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = MenuItem
    fields = ['title', 'price']
    template_name = 'inventory/menuitem_form.html'
    success_url = reverse_lazy('menu-list')
    success_message = "Menu updated successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Menu'
        context['button_text'] = 'Save Changes'
        return context

class MenuItemCreateView(LoginRequiredMixin, CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'inventory/menuitem_form.html'
    success_url = reverse_lazy('menu-list')

class MenuItemDeleteView(LoginRequiredMixin, DeleteView):
    model = MenuItem
    template_name = 'inventory/menuitem_confirm_delete.html'
    success_url = reverse_lazy('menu-list')

class PurchaseListView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = 'inventory/purchase_list.html'
    context_object_name = 'purchases'

class FinancialSummaryView(LoginRequiredMixin, TemplateView):
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

class RecipeRequirementCreateView(LoginRequiredMixin, CreateView):
    model = RecipeRequirement
    form_class = RecipeRequirementForm
    template_name = 'inventory/reciperequirement_form.html'
    success_url = reverse_lazy('home')

class PurchaseCreateView(LoginRequiredMixin, CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'inventory/purchase_form.html'
    success_url = reverse_lazy('purchase-list')

    def form_valid(self, form):
        # Debug: Check if the form is valid
        if not form.is_valid():
            print("Form errors:", form.errors)  # Log form errors
            return self.form_invalid(form)

        # Save the purchase instance
        purchase = form.save(commit=False)
        print("Form data:", form.cleaned_data)  # Debug: Check form data

        # Check inventory availability
        for requirement in RecipeRequirement.objects.filter(menu_item=purchase.menu_item):
            ingredient = requirement.ingredient
            required_quantity = requirement.quantity_required * purchase.quantity

            if ingredient.quantity < required_quantity:
                form.add_error(
                    None,
                    f"Not enough {ingredient.name} in inventory to make {purchase.menu_item.title}."
                )
                return self.form_invalid(form)

        # Deduct inventory
        for requirement in RecipeRequirement.objects.filter(menu_item=purchase.menu_item):
            ingredient = requirement.ingredient
            required_quantity = requirement.quantity_required * purchase.quantity
            ingredient.quantity -= required_quantity
            ingredient.save()

        purchase.save()
        return super().form_valid(form)