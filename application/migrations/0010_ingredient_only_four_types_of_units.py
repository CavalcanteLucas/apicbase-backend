# Generated by Django 3.2.5 on 2021-08-03 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0009_auto_20210801_1648"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="ingredient",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("unit__in", ["gram", "kilogram", "centiliter", "liter"])
                ),
                name="only_four_types_of_units",
            ),
        ),
    ]
