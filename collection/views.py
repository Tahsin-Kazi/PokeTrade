from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import *
from poketrade.settings import GENAI_API_KEY
from random import randint
from google import genai
from PIL import Image
from io import BytesIO

TYPE_COLORS = {
    "Normal": "bg-gray-400",
    "Fire": "bg-red-500",
    "Water": "bg-blue-500",
    "Electric": "bg-yellow-400",
    "Grass": "bg-green-500",
    "Ice": "bg-blue-300",
    "Fighting": "bg-red-700",
    "Poison": "bg-purple-500",
    "Ground": "bg-yellow-600",
    "Flying": "bg-blue-400",
    "Psychic": "bg-pink-500",
    "Bug": "bg-green-600",
    "Rock": "bg-yellow-700",
    "Ghost": "bg-purple-700",
    "Dragon": "bg-indigo-500",
    "Dark": "bg-gray-700",
    "Steel": "bg-gray-500",
    "Fairy": "bg-pink-300",
}

@login_required(login_url='login')
def index(request):
    user = request.user
    collection = user.profile.collection.all()
    
    query = request.GET.get('q', '')
    search_field = request.GET.get('search_field', 'name')
    
    if not user.is_authenticated:
        return redirect('login')

    if query:
        filter_kwargs = {f"{search_field}__icontains": query}
        collection = Pokemon.objects.filter(owner=user.profile, **filter_kwargs)
    else:
        collection = Pokemon.objects.filter(owner=user.profile)

    context = {
        'user': user,
        'collection' : collection,
        'search_query': query,
    }

    return render(request, 'collection/index.html', context)

def detail(request, id):
    
    p = get_object_or_404(Pokemon, id=id)

    if request.method == 'POST':
        new_name = request.POST.get('name', '').strip()
        if new_name:
            p.name = new_name
            p.save()
            messages.success(request, "Nickname updated successfully!")
        else:
            messages.error(request, "Nickname is invalid!")

    data = p.data
    data['image'] = p.image
    data['nickname'] = p.name
    data['total'] = sum(data["stats"].values())
    data['internal_id'] = p.id
    
    data['types_with_colors'] = [
        {"type": t, "color": TYPE_COLORS.get(t, "bg-gray-200")} for t in data.get("types", [])
    ]

    return render(request,'collection/details.html', {'data': data})

def get_custom_image(username, pokemon, prompt):
    client = genai.Client(api_key=GENAI_API_KEY)

    contents = ('Hi, can you generate a 2D, clipart, cartoon, '
                'white background, square image of'
                'a Pokemon like creature that is a') + prompt

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=contents,
        config=genai.types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE']
        )
    )

    part = response.candidates[0].content.parts[0]
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = Image.open(BytesIO(part.inline_data.data))
        path = "static/custom/" + username.strip().lower() + '_' + pokemon.strip().lower() + '.png'
        image.save(path)
        path = "/" + path
        return path
    else:
        return ''


def create_pokemon(request):
    if request.method == 'POST':
        if 'confirm' in request.POST and request.user.profile.currency >= 100:
            user = request.user
            name = request.POST.get("name")
            pokemon = request.POST.get("pokemon")
            prompt = request.POST.get("prompt")
            types = request.POST.getlist("types")

            data = {
                "id": "X",
                "name": pokemon,
                "ability" : "None",
                "height": round(random.uniform(0.5, 3.0)),
                "weight": round(random.uniform(5.0, 150.0)),
                "types": types,
                "stats": {
                    "hp": random.randint(30, 200),
                    "attack": random.randint(30, 200),
                    "defense": random.randint(30, 200),
                    "specialattack": random.randint(30, 200),
                    "specialdefense": random.randint(30, 200),
                    "speed": random.randint(30, 200)
                },
                "image_prompt": prompt,
            }

            pokemon = Pokemon(
                owner=user.profile,
                name=name,
                pokemon=pokemon,
                image=get_custom_image(request.user.username, pokemon, prompt),
                data=data
            )

            pokemon.save()
            user.profile.collection.add(pokemon)
            user.profile.currency -= 100
            user.profile.save()
            return redirect('collection.detail', id=pokemon.id)
        else:
            messages.error(request, "Cannot create a Pokemon, you need to have 1000 PokeDollars and confirm!")
            return redirect('collection.create')

    context = {
        'types' : [(t, TYPE_COLORS[t]) for t in TYPE_COLORS.keys()],
    }

    return render(request, 'collection/create.html', context=context)

def add_pokemon(pokemon, profile):
    name = pokemon.name
    p = Pokemon(
        pokemon = name,
        owner = profile,
    )
    p.save()
    profile.collection.add(p)
    return p

def add_starters(profile):
    x, y, z = randint(1, 1025), randint(1, 1025), randint(1, 1025)
    x, y, z = fetch_pokemon(x), fetch_pokemon(y), fetch_pokemon(z)
    add_pokemon(x, profile)
    add_pokemon(y, profile)
    add_pokemon(z, profile)