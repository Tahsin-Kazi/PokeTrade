# Generated by Django 5.2 on 2025-04-06 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0007_alter_pokemon_options_alter_pokemon_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
