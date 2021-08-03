from django.contrib import admin

from .models import Ingredient, Recipe, RecipeFormula


class RecipeFormulaAdmin(admin.ModelAdmin):
    list_display = ["id", "recipe", "ingredient", "amount_per_recipe"]


admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeFormula, RecipeFormulaAdmin)
