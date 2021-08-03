from rest_framework import serializers

from .models import Ingredient, Recipe, RecipeFormula


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name", "article_number", "cost_per_amount", "amount", "unit"]


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ["id", "name"]


class RecipeFormulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeFormula
        fields = ["id", "recipe", "ingredient", "amount_per_recipe"]
