# Generated by Django 3.2.5 on 2021-07-31 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Formula",
            new_name="RecipeFormula",
        ),
        migrations.AlterModelOptions(
            name="recipeformula",
            options={"ordering": ["recipe"]},
        ),
    ]
