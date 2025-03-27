# Generated by Django 3.1.14 on 2025-03-27 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0003_pokemonentity'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemonentity',
            name='pokemon',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pokemon_entities.pokemon'),
        ),
    ]
