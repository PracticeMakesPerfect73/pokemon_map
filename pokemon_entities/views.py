import folium

from django.utils import timezone
from django.shortcuts import render, get_object_or_404

from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    current_time = timezone.localtime()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    active_pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=current_time,
        disappeared_at__gt=current_time
    ).select_related('pokemon')

    pokemons_on_page = []
    for pokemon_entity in active_pokemon_entities:
        pokemon = pokemon_entity.pokemon
        add_pokemon(
            folium_map,
            pokemon_entity.latitude,
            pokemon_entity.longitude,
            request.build_absolute_uri(pokemon.image.url)
            if pokemon.image else DEFAULT_IMAGE_URL
        )

        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url)
            if pokemon.image else DEFAULT_IMAGE_URL,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    current_time = timezone.localtime()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    active_pokemon_entities = PokemonEntity.objects.filter(
        pokemon=requested_pokemon,
        appeared_at__lte=current_time,
        disappeared_at__gt=current_time
    )

    for pokemon_entity in active_pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.latitude,
            pokemon_entity.longitude,
            request.build_absolute_uri(requested_pokemon.image.url)
            if requested_pokemon.image else DEFAULT_IMAGE_URL
        )

    prev_evolution_chars = None
    if requested_pokemon.previous_evolution:
        previous_evolution = requested_pokemon.previous_evolution
        prev_evolution_chars = {
            'pokemon_id': previous_evolution.id,
            'title_ru': previous_evolution.title,
            'img_url': request.build_absolute_uri(previous_evolution.image.url)
            if previous_evolution.image else DEFAULT_IMAGE_URL,
        }

    next_evolution_chars = None
    if requested_pokemon.next_evolution.first():
        next_evolution = requested_pokemon.next_evolution.first()
        next_evolution_chars = {
            'pokemon_id': next_evolution.id,
            'title_ru': next_evolution.title,
            'img_url': request.build_absolute_uri(next_evolution.image.url)
            if next_evolution.image else DEFAULT_IMAGE_URL,
        }

    pokemon_chars = {
        'pokemon_id': requested_pokemon.id,
        'title_ru': requested_pokemon.title,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'description': requested_pokemon.description,
        'img_url': request.build_absolute_uri(requested_pokemon.image.url)
        if requested_pokemon.image else DEFAULT_IMAGE_URL,
        'entities': active_pokemon_entities,
        'previous_evolution': prev_evolution_chars,
        'next_evolution': next_evolution_chars,
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_chars
    })
