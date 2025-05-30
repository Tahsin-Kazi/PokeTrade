# Generated by Django 5.0 on 2025-04-24 20:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_profile_currency_friendrequest_delete_message'),
        ('collection', '0010_remove_pokemon_types'),
        ('marketplace', '0003_alter_listing_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyer_listing', to='accounts.profile'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='date_posted',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='pokemon',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='collection.pokemon'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller_listing', to='accounts.profile'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='status',
            field=models.CharField(choices=[('not_sold', 'Not Sold'), ('sold', 'Sold')], default='not_sold', max_length=10),
        ),
    ]
