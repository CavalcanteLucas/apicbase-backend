from rest_framework import viewsets, response, generics

from .models import Ingredient, Recipe, RecipeFormula
from .serializers import IngredientSerializer, RecipeSerializer, RecipeFormulaSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeFormulaViewSet(viewsets.ModelViewSet):
    queryset = RecipeFormula.objects.all()
    serializer_class = RecipeFormulaSerializer


class RecipeDetailsListAPIView(generics.ListAPIView):
    serializer_class = RecipeFormulaSerializer

    def get_result(self, data):
        for item in data:
            ingredient = (
                Ingredient.objects.filter(id=item["ingredient"]).values().first()
            )
            item["ingredient"] = ingredient["name"]
            item["unit"] = ingredient["unit"]
            item["cost_per_amount"] = float(ingredient["cost_per_amount"]) / float(
                ingredient["amount"]
            )
            item["cost"] = float(item["cost_per_amount"]) * float(
                item["amount_per_recipe"]
            )
        return data

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(self.get_result(serializer.data))

    def get_queryset(self):
        recipe_id = self.kwargs["recipe_id"]
        return RecipeFormula.objects.filter(recipe=recipe_id)


class RecipeTotalCostEndpoint(generics.ListAPIView):
    serializer_class = RecipeFormulaSerializer

    def get_result(self, data):
        total_cost = 0.00
        for item in data:
            ingredient = (
                Ingredient.objects.filter(id=item["ingredient"]).values().first()
            )
            total_cost += (
                float(item["amount_per_recipe"])
                * float(ingredient["cost_per_amount"])
                / float(ingredient["amount"])
            )
        return "%.2f" % total_cost

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(self.get_result(serializer.data))

    def get_queryset(self):
        recipe_id = self.kwargs["recipe_id"]
        return RecipeFormula.objects.filter(recipe=recipe_id)
