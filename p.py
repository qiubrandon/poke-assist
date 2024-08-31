import requests 
from operator import mul

# def typeCleaner(typings):
#     for damage_rel in typings:
#         result = 1
#         for num in typings.get(damage_rel):
#             result *= num
#         typings[damage_rel] = result
#     return typings
        
def calc(team, enemy):

    url = "https://pokeapi.co/api/v2/pokemon/"
    teamInput = team
    teamInput = teamInput.split(",")
    opponent = enemy
    typings = {}
    for mon in teamInput:
        response = requests.get(url + mon)
        if (response.status_code == 200):
            data = response.json()
            typings[mon] = data["types"]
    enemy = requests.get(url + opponent)
    if (enemy.status_code == 200):
        eData = enemy.json()

    # identify typing of enemy and weaknesses, compile them into list

    typeProps = []

    for type in eData["types"]:
        response = requests.get(type["type"]["url"])
        # print(type["type"]["url"])
        damage_relations = response.json()["damage_relations"]
        typeProps.append(damage_relations)

    enemyProps = {}

    # print(typeProps)

    for typing in typeProps:
        for prop in typing:
            modifier = float("inf")
            match prop:
                case "double_damage_from":
                    modifier = 2
                case "double_damage_to":
                    modifier = -2
                case "half_damage_from":
                    modifier = -2
                case "half_damage_to":
                    modifier = 2
                case "no_damage_from":
                    modifier = -4
                case "no_damage_to":
                    modifier = 4
            for type in typing.get(prop):
                name = type["name"]
                if enemyProps.get(name) == None:
                    enemyProps[name] = modifier
                else:
                    enemyProps[name] = enemyProps.get(name) + modifier
                # print(name,"is",enemyProps.get(name))

    etm = enemyProps # enemy type multipliers

    pokeScores = {}


    for pokemon in typings:
        for type in typings[pokemon]:
            t = type["type"]["name"]
            if etm.get(t) == None:
                etm[t] = 1
            if pokeScores.get(pokemon) == None:
                # print("{} is {}".format(t, etm[t]))
                pokeScores[pokemon] = etm[t]
            else:
                pokeScores[pokemon] = pokeScores.get(pokemon) + etm[t]

    optimal = max(pokeScores, key=lambda x: pokeScores[x])
    return optimal

team = input("Enter your team: ")
enemy = input("Enter opponent: ")
optimal = calc(team, enemy)

print(optimal, "is most optimal.")