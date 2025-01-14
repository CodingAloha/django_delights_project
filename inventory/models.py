from django.db import models

# Ingredients: Representing Inventory items
class Ingredient(models.Model):
    name = models.CharField(max_length=100) # name of ingredient (e.g., flour)
    quantity = models.FloatField(default=0) # quantity available in the inventory (e.g., 4.5)
    unit = models.CharField(max_length=50, default="unitless") # unit of measurement (e.g., "tbsp", "lbs")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2) # price per unit (e.g., 0.05)

    def __str__(self):
        return f"{self.name} - {self.quantity} {self.unit} available @ {self.unit_price}/{self.unit}"
    
# MenuItems: Representing menu entries
class MenuItem(models.Model):
    title = models.CharField(max_length=100) # name of menu item (e.g., "Orange Juice")
    price = models.DecimalField(max_digits=10, decimal_places=2) # price of the menu item (e.g., 3.49)

    def __str__(self):
        return f"{self.title} @ ${self.price}"

# RecipeRequirement: Mapping ingredients to menu items
class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE) # reference to MenuItem table
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE) # reference to Ingredient table
    quantity_required = models.FloatField() # quantity of ingredient needed for menu item (e.g., 1.5 ounces of "sugar" to create "Chocolate Cake")

    def __str__(self):
        return f"{self.quantity_required} {self.ingredient.unit} of {self.ingredient.name} for {self.menu_item.title}"
    
# Purchases: Logging restaurant purchases
class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE) # purchased menu item
    timestamp = models.DateTimeField(auto_now_add=True) # time of purchase
    quantity = models.PositiveIntegerField(default=1) # quantity purchased

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.title} @ {self.timestamp}"