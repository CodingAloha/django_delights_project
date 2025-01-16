from django import forms

from .models import Ingredient, MenuItem, Purchase, RecipeRequirement


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ["title", "price"]


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name", "quantity", "unit", "unit_price"]


class RecipeRequirementForm(forms.ModelForm):
    class Meta:
        model = RecipeRequirement
        fields = ["menu_item", "ingredient", "quantity_required"]


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ["menu_item", "quantity"]
