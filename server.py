import logging
import webbrowser

from flask import Flask, Response, request
import json
import pymysql
import requests
import urllib.request
from urllib.request import urlopen
from requests.packages.urllib3.exceptions import InsecureRequestWarning
logging.captureWarnings(True)
import models

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="poke",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)
app = Flask(__name__)


@app.route('/sanity')
def sanity():
    return "Server is up and running smoothly"

@app.route('/location/<poke_id>')
def location(poke_id):
    res=models.get_location(poke_id)
    url=f'https://www.google.com/maps/place/"{res["town"]}","{res["street"]}"'
    webbrowser.open_new(url)
    return "Server is up and running smoothly"

@app.route('/update/<poke_name>',methods = ["PUT"])
def update_types(poke_name):
    res=""
    url = f'https://pokeapi.co/api/v2/pokemon/{poke_name}'
    poke_data = requests.get(url,verify=False).json()
    for type in poke_data["types"]:
        try:
            models.update_pokemon_types(poke_name,type)
        except pymysql.err.IntegrityError:
            res=("key is already exist")
        except:
            res="failed to update types"
    if res != "":
        return json.dumps(res)
    return json.dumps(f'update type'), 201


@app.route('/add_pokemon', methods=["POST"])
def add_pokemon():
    pokemon = request.get_json()
    try:
        models.insert_pokemon(pokemon)
    except:
        return json.dumps('didnt create pokemon'), 409
    try:
        models.add_types(pokemon["name"], pokemon["types"])
    except:
        return json.dumps('didnt create conection'), 409

    return json.dumps('create'), 201


@app.route('/pocemon_by_type/<type_name>')
def get_pocemon_by_type(type_name):
    try:
        result = models.get_pokemon_by_type(type_name)
    except:
        return json.dumps("failed to get pokemons by type"), 409
    return json.dumps(result), 200


@app.route('/delete/<pokemone_name>/<trainer_name>', methods=["DELETE"])
def delete_ownedby(pokemone_name,trainer_name):
    try:
        models.delete_pokemon_trainer(pokemone_name,trainer_name)
    except:
        return json.dumps("failed to delete connection"), 409
    return json.dumps("deleted connection"), 201

@app.route('/show/<pokemon_name>')
def show_image(pokemon_name):
    try:
        pokemon_url = 'https://pokeapi.co/api/v2/pokemon/{}'.format(pokemon_name)
        pokemon = requests.get(url=pokemon_url, verify=False).json()
        # image_url = pokemon["sprites"]["other"]["official-artwork"]["front_default"]
        image_url = pokemon["sprites"]["front_default"]
        # webbrowser.open_new(image_url)
        urllib.request.urlretrieve(image_url, f"{pokemon_name}.png")
        return "success"
    except Exception as e:
        return json.dumps(e), 500

if __name__ == '__main__':
    app.run(port=3010)
    # poke_name="butterfree"
    # url = f'https://pokeapi.co/api/v2/pokemon/{poke_name}'
    # poke_data = requests.get(url, verify=False).json()
    # type=poke_data["types"][1]
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         f'INSERT INTO PokemonsTypes (pokemon_name,pokemon_type) VALUES ("{poke_name}","{type["type"]["name"]}")')
    #     connection.commit()
