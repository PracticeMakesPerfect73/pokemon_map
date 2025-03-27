from django.db import models  # noqa F401

class Pokemon(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='pokemons/', blank=True)

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, default=1)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True)
    level = models.IntegerField(blank=True)
    health = models.IntegerField(blank=True)
    strength = models.IntegerField(blank=True)
    defence = models.IntegerField(blank=True)
    stamina = models.IntegerField(blank=True)