# Generated by Django 5.1.5 on 2025-04-01 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('poke_name', models.CharField(max_length=100)),
                ('image', models.URLField()),
                ('data', models.JSONField()),
            ],
        ),
    ]
