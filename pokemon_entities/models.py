from django.db import models  # noqa F401
from django.utils.timezone import datetime

class Pokemon(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='pokemons_images/', blank=True)

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='entities', verbose_name='Покемон')
    latitude = models.FloatField(blank=True, null=True, verbose_name='широта')
    longitude = models.FloatField(blank=True, null=True, verbose_name='долгота')
    appeared_at = models.DateTimeField( blank=True, null=True, verbose_name='Когда появится')
    disappeared_at = models.DateTimeField( blank=True, null=True, verbose_name='Когда исчезнет')

    level = models.IntegerField(default=1, verbose_name='Уровень')
    health = models.IntegerField(blank=True, null=True, verbose_name='Количество жизни')
    strength = models.IntegerField(blank=True, null=True, verbose_name='Сила')
    defence = models.IntegerField(blank=True, null=True, verbose_name='Защита')
    stamina = models.IntegerField(blank=True, null=True, verbose_name='Выносливость')


    def __str__(self):
        return f'{self.pokemon.title} at {self.latitude}, {self.longitude}'