# Generated by Django 3.2.5 on 2021-08-01 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0006_ingredient_only_one_article_number"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="ingredient",
            name="only_one_article_number",
        ),
        migrations.AddConstraint(
            model_name="ingredient",
            constraint=models.UniqueConstraint(
                fields=("article_number",), name="only_unique_article_number"
            ),
        ),
        migrations.AddConstraint(
            model_name="ingredient",
            constraint=models.UniqueConstraint(
                fields=("name",), name="only_unique_name"
            ),
        ),
    ]
