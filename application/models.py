from django.db import models
from django.db.models.deletion import CASCADE


class Unit(models.TextChoices):
    GRAM = "gram", "gram"
    KILOGRAM = "kilogram", "kilogram"
    CENTILITER = "centiliter", "centiliter"
    LITER = "liter", "liter"


class Ingredient(models.Model):
    name = models.CharField(max_length=80)
    article_number = models.IntegerField()
    cost_per_amount = models.DecimalField(max_digits=6, decimal_places=2)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=10, choices=Unit.choices)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        constraints = [
            models.CheckConstraint(
                name="ingredient_cost_per_amount_cannot_be_negative",
                check=(models.Q(cost_per_amount__gt=0)),
            ),
            models.CheckConstraint(
                name="ingredient_amount_cannot_be_negative",
                check=(models.Q(amount__gt=0)),
            ),
            models.UniqueConstraint(
                name="only_unique_ingredient_article_number", fields=["article_number"]
            ),
            models.UniqueConstraint(
                name="only_unique_ingredient_name", fields=["name"]
            ),
            models.CheckConstraint(
                name="only_four_types_of_units",
                check=models.Q(unit__in=Unit.values),
            ),
        ]


class Recipe(models.Model):
    name = models.CharField(max_length=80)
    ingredients = models.ManyToManyField(Ingredient, through="RecipeFormula")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(name="only_unique_recipe_name", fields=["name"])
        ]


class RecipeFormula(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=CASCADE)
    amount_per_recipe = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.recipe} - {self.ingredient}"

    class Meta:
        ordering = ["recipe"]
        constraints = [
            models.CheckConstraint(
                name="recipe_amount_cannot_be_negative",
                check=(models.Q(amount_per_recipe__gt=0)),
            )
        ]
