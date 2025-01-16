from datetime import datetime
from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import IngredientForm, MenuItemForm, PurchaseForm, RecipeRequirementForm
from .models import Ingredient, MenuItem, Purchase, RecipeRequirement


class InventoryListView(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = "inventory/inventory_list.html"
    context_object_name = "ingredients"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_year"] = datetime.now().year
        return context


class IngredientCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = "inventory/ingredient_form.html"
    success_url = reverse_lazy("home")
    success_message = "Ingredient added successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Ingredient"
        context["button_text"] = "Add Ingredient"
        return context


class IngredientUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Ingredient
    fields = ["name", "quantity", "unit", "unit_price"]
    template_name = "inventory/ingredient_form.html"
    success_url = reverse_lazy("home")
    success_message = "Ingredient updated successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Ingredient"
        context["button_text"] = "Save Changes"
        return context


class IngredientDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Ingredient
    template_name = "inventory/ingredient_confirm_delete.html"
    success_url = reverse_lazy("home")
    success_message = "Ingredient deleted successfully!"


class MenuListView(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = "inventory/menu_list.html"
    context_object_name = "menu_items"


class MenuItemCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = "inventory/menuitem_form.html"
    success_url = reverse_lazy("menu-list")
    success_message = "Menu Item successfully added!"


class MenuItemUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = MenuItem
    fields = ["title", "price"]
    template_name = "inventory/menuitem_form.html"
    success_url = reverse_lazy("menu-list")
    success_message = "Menu updated successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Menu"
        context["button_text"] = "Save Changes"
        return context


class MenuItemDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = MenuItem
    template_name = "inventory/menuitem_confirm_delete.html"
    success_url = reverse_lazy("menu-list")
    success_message = "Menu Item successfully deleted!"


class PurchaseListView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = "inventory/purchase_list.html"
    context_object_name = "purchases"


class PurchaseCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = "inventory/purchase_form.html"
    success_url = reverse_lazy("purchase-list")
    success_message = "Purchase successfully added!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Purchase'
        context['button_text'] = 'Submit'
        return context

class PurchaseUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Purchase
    fields = ["menu_item", "quantity"]
    template_name = "inventory/purchase_form.html"
    success_url = reverse_lazy("purchase-list")
    success_message = "Purchase updated successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Purchase"
        context["button_text"] = "Save Changes"
        return context


class PurchaseDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Purchase
    template_name = "inventory/purchase_confirm_delete.html"
    success_url = reverse_lazy("purchase-list")
    success_message = "Purchase deleted successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Purchase"
        return context


class RecipeRequirementListView(LoginRequiredMixin, ListView):
    model = RecipeRequirement
    template_name = "inventory/recipe_requirement_list.html"
    context_object_name = "recipe_requirements"

    def get_queryset(self):
        return RecipeRequirement.objects.filter(menu_item_id=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_item = get_object_or_404(MenuItem, pk=self.kwargs["pk"])
        context["menu_item"] = menu_item
        return context


class RecipeRequirementCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = RecipeRequirement
    form_class = RecipeRequirementForm
    template_name = "inventory/reciperequirement_form.html"
    success_message = "Recipe requirement successfully added!"

    def get_success_url(self):
        return reverse_lazy(
            "recipe-requirements", kwargs={"pk": self.request.GET.get("menu_item")}
        )

    def get_initial(self):
        initial = super().get_initial()
        menu_item_id = self.request.GET.get("menu_item")
        if menu_item_id:
            initial["menu_item"] = menu_item_id
        return initial


class RecipeRequirementUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = RecipeRequirement
    form_class = RecipeRequirementForm
    template_name = "inventory/reciperequirement_form.html"
    success_message = "Recipe requirement successfully updated!"

    def get_success_url(self):
        return reverse_lazy(
            "recipe-requirements", kwargs={"pk": self.object.menu_item.pk}
        )


class RecipeRequirementDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = RecipeRequirement
    template_name = "inventory/reciperequirement_confirm_delete.html"
    success_url = reverse_lazy("purchase-list")
    success_message = "Recipe requirement successfully deleted!"

    def get_success_url(self):
        return reverse_lazy(
            "recipe-requirements", kwargs={"pk": self.object.menu_item.pk}
        )


class FinancialSummaryView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/financial_summary.html"  # Points to your template

    def get_context_data(self, **kwargs):
        # Get the default context
        context = super().get_context_data(**kwargs)

        # Calculate total revenue
        total_revenue = sum(
            purchase.menu_item.price * purchase.quantity
            for purchase in Purchase.objects.all()
        )
        context["total_revenue"] = total_revenue

        # Calculate total cost
        total_cost = Decimal(0)
        for purchase in Purchase.objects.all():
            requirements = RecipeRequirement.objects.filter(
                menu_item=purchase.menu_item
            )
            for req in requirements:
                total_cost += (
                    Decimal(req.quantity_required)
                    * req.ingredient.unit_price
                    * purchase.quantity
                )
        context["total_cost"] = total_cost

        # Calculate profit
        context["profit"] = total_revenue - total_cost

        return context
