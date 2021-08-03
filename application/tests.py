from django.test import TestCase
from django.urls import reverse
from django.forms import model_to_dict
from django.db.utils import IntegrityError

from rest_framework import status
from model_bakery import baker

from .models import Ingredient, Recipe, RecipeFormula


class IngredientTest(TestCase):
    def setUp(self):
        self.ingredients_set = baker.prepare("Ingredient", _quantity=2)

    def test_list_ingredients_successfully(self):
        self.assertEqual(0, Ingredient.objects.count())
        [ingredient.save() for ingredient in self.ingredients_set]
        self.assertEqual(len(self.ingredients_set), Ingredient.objects.count())
        url = reverse("ingredients-list")
        response = self.client.get(path=url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(self.ingredients_set), len(response.data))

    def test_create_ingredient_successfully(self):
        self.assertEqual(0, Ingredient.objects.count())
        url = reverse("ingredients-list")
        response = self.client.post(
            path=url,
            content_type="application/json",
            data=model_to_dict(self.ingredients_set[0]),
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Ingredient.objects.count())
        expected_data = {
            "name": self.ingredients_set[0].name,
            "article_number": self.ingredients_set[0].article_number,
            "cost_per_amount": str(self.ingredients_set[0].cost_per_amount),
            "amount": str(self.ingredients_set[0].amount),
            "unit": self.ingredients_set[0].unit,
        }
        self.assertTrue(
            all(item in response.data.items() for item in expected_data.items())
        )

    def test_delete_ingredient_successfully(self):
        self.ingredients_set[0].save()
        self.assertEqual(1, Ingredient.objects.count())
        ingredient_sample = Ingredient.objects.first()
        url = reverse("ingredients-detail", kwargs={"pk": ingredient_sample.id})
        response = self.client.delete(path=url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(0, Ingredient.objects.count())

    def test_edit_ingredient_successfully(self):
        self.ingredients_set[0].save()
        self.assertEqual(1, Ingredient.objects.count())
        ingredient_sample = Ingredient.objects.first()
        ingredient_sample_variant = {
            "name": "a name",
            "article_number": 42,
            "cost_per_amount": "1.99",
            "amount": "10.00",
            "unit": "centiliter",
        }
        url = reverse("ingredients-detail", kwargs={"pk": ingredient_sample.id})
        response = self.client.put(
            path=url,
            content_type="application/json",
            data=ingredient_sample_variant,
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, Ingredient.objects.count())
        expected_data = {
            "name": ingredient_sample_variant["name"],
            "article_number": ingredient_sample_variant["article_number"],
            "cost_per_amount": ingredient_sample_variant["cost_per_amount"],
            "amount": ingredient_sample_variant["amount"],
            "unit": ingredient_sample_variant["unit"],
        }
        self.assertTrue(
            all(item in response.data.items() for item in expected_data.items())
        )

    def test_ingredient_cannot_have_negative_cost_per_amount(self):
        self.assertEqual(0, Ingredient.objects.count())
        with self.assertRaises(IntegrityError):
            baker.make("Ingredient", cost_per_amount=-1)
            self.assertEqual(0, Ingredient.objects.count())

    def test_ingredient_cannot_have_negative_amount(self):
        self.assertEqual(0, Ingredient.objects.count())
        with self.assertRaises(IntegrityError):
            baker.make("Ingredient", amount=-1)
            self.assertEqual(0, Ingredient.objects.count())

    def test_ingredient_cannot_have_repetitive_article_number(self):
        self.assertEqual(0, Ingredient.objects.count())
        baker.make("Ingredient", article_number=10)
        self.assertEqual(1, Ingredient.objects.count())
        with self.assertRaises(IntegrityError):
            baker.make("Ingredient", article_number=10)
            self.assertEqual(1, Ingredient.objects.count())

    def test_ingredient_cannot_have_repetitive_name(self):
        self.assertEqual(0, Ingredient.objects.count())
        baker.make("Ingredient", name="some ingredient")
        self.assertEqual(1, Ingredient.objects.count())
        with self.assertRaises(IntegrityError):
            baker.make("Ingredient", name="some ingredient")
            self.assertEqual(1, Ingredient.objects.count())


class RecipeTest(TestCase):
    def setUp(self):
        self.ingredients_set_1 = baker.make("Ingredient", _quantity=2)
        self.ingredients_set_2 = baker.make("Ingredient", _quantity=3)
        self.recipe_sample_1 = baker.prepare(
            "Recipe",
            ingredients=self.ingredients_set_1,
        )
        self.recipe_sample_2 = baker.prepare(
            "Recipe",
            ingredients=self.ingredients_set_2,
        )
        self.recipes_set = [self.recipe_sample_1, self.recipe_sample_2]

    def test_recipe_cannot_have_repetitive_name(self):
        self.assertEqual(0, Recipe.objects.count())
        baker.make("Recipe", name="some recipe")
        self.assertEqual(1, Recipe.objects.count())
        with self.assertRaises(IntegrityError):
            baker.make("Recipe", name="some recipe")
            self.assertEqual(1, Recipe.objects.count())

    def test_list_recipes_successfully(self):
        self.assertEqual(0, Recipe.objects.count())
        [recipe.save() for recipe in self.recipes_set]

        self.assertEqual(len(self.recipes_set), Recipe.objects.count())
        url = reverse("recipes-list")
        response = self.client.get(path=url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(self.recipes_set), len(response.data))

    def test_create_recipe_successfully(self):
        self.assertEqual(0, Recipe.objects.count())

        url = reverse("recipes-list")
        response = self.client.post(
            path=url,
            content_type="application/json",
            data=model_to_dict(self.recipes_set[0]),
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Recipe.objects.count())
        expected_data = {
            "name": self.recipes_set[0].name,
        }
        self.assertTrue(
            all(item in response.data.items() for item in expected_data.items())
        )

    def test_delete_recipe_successfully(self):
        self.recipes_set[0].save()
        self.assertEqual(1, Recipe.objects.count())
        recipe_sample = Recipe.objects.first()
        url = reverse("recipes-detail", kwargs={"pk": recipe_sample.id})
        response = self.client.delete(path=url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(0, Recipe.objects.count())

    def test_edit_recipe_name_successfully(self):
        self.recipes_set[0].save()
        self.assertEqual(1, Recipe.objects.count())
        recipe_sample = Recipe.objects.first()
        recipe_sample_variant = {
            "name": "a name",
        }
        url = reverse("recipes-detail", kwargs={"pk": recipe_sample.id})
        response = self.client.put(
            path=url,
            content_type="application/json",
            data=recipe_sample_variant,
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, Recipe.objects.count())
        expected_data = {
            "name": recipe_sample_variant["name"],
        }
        self.assertTrue(
            all(item in response.data.items() for item in expected_data.items())
        )


class RecipeFormulaTest(TestCase):
    def setUp(self):
        self.ingredients_set_1 = baker.make("Ingredient", _quantity=2)
        self.ingredients_set_2 = baker.make("Ingredient", _quantity=3)
        self.recipe_sample_1 = baker.make(
            "Recipe",
        )

        self.recipe_sample_2 = baker.make(
            "Recipe",
        )

        self.recipe_formula_sample = baker.prepare(
            "RecipeFormula",
            recipe=self.recipe_sample_1,
            ingredient=self.ingredients_set_1[0],
            amount_per_recipe="2.00",
        )

    def test_recipe_formula_cannot_have_negative_amount_per_price(self):
        self.assertEqual(0, RecipeFormula.objects.count())
        with self.assertRaises(IntegrityError):
            baker.make("RecipeFormula", amount_per_recipe=-1)
            self.assertEqual(0, RecipeFormula.objects.count())

    def test_recipe_formula_calculates_correct_price(self):
        self.assertEqual(0, RecipeFormula.objects.count())
        ingredient_sample_1 = baker.make("Ingredient", cost_per_amount=2, amount=1)
        ingredient_sample_2 = baker.make("Ingredient", cost_per_amount=3, amount=1)
        recipe_sample = baker.make("Recipe")
        baker.make(
            "RecipeFormula",
            ingredient=ingredient_sample_1,
            recipe=recipe_sample,
            amount_per_recipe=10,
        )
        baker.make(
            "RecipeFormula",
            ingredient=ingredient_sample_2,
            recipe=recipe_sample,
            amount_per_recipe=100,
        )
        self.assertEqual(2, RecipeFormula.objects.count())
        url = reverse("recipe-details-cost", kwargs={"recipe_id": recipe_sample.id})
        response = self.client.get(path=url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected_data = "320.00"  # 2/1 * 10 + 3/1 * 100
        self.assertEqual(expected_data, response.data)

    def test_create_recipe_formula_successfully(self):
        self.assertEqual(0, RecipeFormula.objects.count())
        url = reverse("recipes-formulas-list")
        response = self.client.post(
            path=url,
            content_type="application/json",
            data=model_to_dict(self.recipe_formula_sample),
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, RecipeFormula.objects.count())

        expected_data = {
            "recipe": self.recipe_formula_sample.recipe.id,
            "ingredient": self.recipe_formula_sample.ingredient.id,
            "amount_per_recipe": self.recipe_formula_sample.amount_per_recipe,
        }
        self.assertTrue(
            all(item in response.data.items() for item in expected_data.items())
        )

    def test_delete_recipe_formula_successfully(self):
        self.recipe_formula_sample.save()
        self.assertEqual(1, RecipeFormula.objects.count())
        recipe_formula_sample_alternative = RecipeFormula.objects.first()
        url = reverse(
            "recipes-formulas-detail",
            kwargs={"pk": recipe_formula_sample_alternative.id},
        )
        response = self.client.delete(path=url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(0, RecipeFormula.objects.count())
