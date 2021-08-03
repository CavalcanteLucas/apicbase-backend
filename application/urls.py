from django.db.models import base
from django.urls import path
from rest_framework import routers

from .views import (
    IngredientViewSet,
    RecipeViewSet,
    RecipeFormulaViewSet,
    RecipeDetailsListAPIView,
    RecipeTotalCostEndpoint,
)

router = routers.DefaultRouter()
router.register("ingredients", IngredientViewSet, basename="ingredients")
router.register("recipes", RecipeViewSet, basename="recipes")
router.register("recipes-formulas", RecipeFormulaViewSet, basename="recipes-formulas")

urlpatterns = [
    path(
        "recipes/<int:recipe_id>/details/",
        RecipeDetailsListAPIView.as_view(),
        name="recipe-details",
    ),
    path(
        "recipes/<int:recipe_id>/cost/",
        RecipeTotalCostEndpoint.as_view(),
        name="recipe-details-cost",
    ),
]

urlpatterns += router.urls
