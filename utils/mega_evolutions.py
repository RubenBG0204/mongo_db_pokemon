# Megapiedras conocidas por nombre de Pokemon.
MEGA_EVOLUTIONS = {
    "venusaur": ["venusaurite"],
    "charizard": ["charizardite-x", "charizardite-y"],
    "blastoise": ["blastoisinite"],
    "beedrill": ["beedrillite"],
    "pidgeot": ["pidgeotite"],
    "alakazam": ["alakazite"],
    "slowbro": ["slowbronite"],
    "gengar": ["gengarite"],
    "kangaskhan": ["kangaskhanite"],
    "pinsir": ["pinsirite"],
    "gyarados": ["gyaradosite"],
    "aerodactyl": ["aerodactylite"],
    "mewtwo": ["mewtwonite-x", "mewtwonite-y"],
    "ampharos": ["ampharosite"],
    "steelix": ["steelixite"],
    "scizor": ["scizorite"],
    "heracross": ["heracronite"],
    "houndoom": ["houndoominite"],
    "tyranitar": ["tyranitarite"],
    "sceptile": ["sceptilite"],
    "blaziken": ["blazikenite"],
    "swampert": ["swampertite"],
    "gardevoir": ["gardevoirite"],
    "sableye": ["sablenite"],
    "mawile": ["mawilite"],
    "aggron": ["aggronite"],
    "medicham": ["medichamite"],
    "manectric": ["manectite"],
    "sharpedo": ["sharpedonite"],
    "camerupt": ["cameruptite"],
    "altaria": ["altarianite"],
    "banette": ["banettite"],
    "absol": ["absolite"],
    "glalie": ["glalitite"],
    "salamence": ["salamencite"],
    "metagross": ["metagrossite"],
    "latias": ["latiasite"],
    "latios": ["latiosite"],
    "lopunny": ["lopunnite"],
    "garchomp": ["garchompite"],
    "lucario": ["lucarionite"],
    "abomasnow": ["abomasite"],
    "gallade": ["galladite"],
    "audino": ["audinite"],
    "diancie": ["diancite"],
    "meganium": ["meganiumite"],
    "emboar": ["emboarite"],
    "feraligatr": ["feraligite"],
    "barbaracle": ["barbaracite"],
    "starmie": ["staminite"],
    "floette": ["floetite"],
    "floette-eternal": ["floetite"],
    "pyroar": ["pyroarite"],
    "clefable": ["clefablite"],
    "scolipede": ["scolipedite"],
    "victreebel": ["victreebelite"],
    "excadrill": ["excadrite"],
    "eelektross": ["eelektrossite"],
    "dragonite": ["dragoninite"],
    "malamar": ["malamarite"],
    "dragalge": ["dragalgite"],
    "froslass": ["froslassite"],
    "hawlucha": ["hawluchanite"],
    "scrafty": ["scraftinite"],
    "chandelure": ["chandelurite"],
    "falinks": ["falinksite"],
    "skarmory": ["skarmorite"],
    "drampa": ["drampanite"],
    "zygarde": ["zygardite"],
    "chesnaught": ["chesnaughtite"],
    "delphox": ["delphoxite"],
    "greninja": ["greninjite"],
    "baxcalibur": ["baxcalibrite"],
    "raichu": ["raichunite-x", "raichunite-y"],
    "chimecho": ["chimechite"],
    "zeraora": ["zeraorite"],
    "crabominable": ["crabominite"],
    "scovillain": ["scovillainite"],
    "staraptor": ["staraptite"],
    "tatsugiri": ["tatsugirinite"],
    "golisopod": ["golisopite"],
    "golurk": ["golurkite"],
    "meowstic": ["meowsticite"],
    "heatran": ["heatranite"],
    "glimmora": ["glimmoranite"],
    "darkrai": ["darkrainite"],
    "magearna": ["magearnite"],
}

EXTRA_MEGA_STONES = {
    "absol": ["absolite-z"],
    "lucario": ["lucarionite-z"],
}

# Mega Rayquaza no usa megapiedra.
SPECIAL_MEGA_EVOLUTIONS = {"rayquaza"}

# PokeAPI aun no tiene sprites de varias piedras nuevas.
IMAGELESS_STONES = {
    "absolite-z",
    "barbaracite",
    "baxcalibrite",
    "chandelurite",
    "chesnaughtite",
    "chimechite",
    "clefablite",
    "crabominite",
    "darkrainite",
    "delphoxite",
    "dragalgite",
    "dragoninite",
    "drampanite",
    "eelektrossite",
    "emboarite",
    "excadrite",
    "falinksite",
    "feraligite",
    "floetite",
    "froslassite",
    "glimmoranite",
    "golisopite",
    "golurkite",
    "greninjite",
    "hawluchanite",
    "heatranite",
    "lucarionite-z",
    "magearnite",
    "malamarite",
    "meganiumite",
    "meowsticite",
    "pyroarite",
    "raichunite-x",
    "raichunite-y",
    "scraftinite",
    "scolipedite",
    "scovillainite",
    "skarmorite",
    "staraptite",
    "staminite",
    "tatsugirinite",
    "victreebelite",
    "zeraorite",
    "zygardite",
}


def add_mega_evolution_info(pokemon):
    # Anade datos de megaevolucion antes de pintar detalle o editar.
    if not pokemon:
        return pokemon

    fields = get_mega_evolution_fields(
        pokemon.get("name", ""),
        force=pokemon.get("can_mega_evolve", False),
        detect_known=True,
    )
    pokemon["can_mega_evolve"] = fields["can_mega_evolve"]
    pokemon["mega_stones"] = fields["mega_stones"]
    return pokemon


def get_mega_evolution_fields(name, force=False, detect_known=True):
    # Devuelve si puede megaevolucionar y que piedras debe mostrar.
    clean_name = name.strip().lower()
    stones = MEGA_EVOLUTIONS.get(clean_name, []) + EXTRA_MEGA_STONES.get(clean_name, [])

    if clean_name in SPECIAL_MEGA_EVOLUTIONS and (force or detect_known):
        return {"can_mega_evolve": True, "mega_stones": []}

    if stones and (force or detect_known):
        return {
            "can_mega_evolve": True,
            "mega_stones": [build_stone(stone) for stone in stones],
        }

    if force:
        return {
            "can_mega_evolve": True,
            "mega_stones": [
                {
                    "name": f"Piedra de {clean_name.capitalize()}",
                    "image": "",
                }
            ],
        }

    return {"can_mega_evolve": False, "mega_stones": []}


def build_stone(stone):
    # Monta el nombre visible y la imagen si existe en PokeAPI.
    return {
        "name": format_stone_name(stone),
        "image": "" if stone in IMAGELESS_STONES else f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/{stone}.png",
    }


def format_stone_name(stone):
    # Convierte charizardite-x en Charizardite X.
    return stone.replace("-", " ").title()
