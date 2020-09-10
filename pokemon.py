import pymysql
import json

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="poke",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

if connection.open:
    print("the connection is opened")


# def insert_to_table(data: dict):
#     try:
#         with connection.cursor() as cursor:
#             query = 'INSERT into Pokemon values ()'
#             cursor.execute(query)
#     except:
#         print("Error")


def load_data():
    data = json.load(open("poke_data.json"))
    return data


def not_in_owners(owner):
    try:
        with connection.cursor() as cursor:
            query = f'SELECT * FROM Owners WHERE name = "{owner["name"]}"'
            cursor.execute(query)
            result = cursor.fetchall()
            connection.commit()
            return len(result) == 0
    except:
        print("Error")


def insert_owners(owners, pokemon_id):
    for owner in owners:
        if not_in_owners(owner):
            try:
                with connection.cursor() as cursor:
                    query = f'INSERT INTO Owners (name, town) VALUES ("{owner["name"]}", "{owner["town"]}")'
                    cursor.execute(query)
                    connection.commit()
            except:
                print("Error in Owners insert")

        try:
            with connection.cursor() as cursor:
                query = f'INSERT INTO OwnedBy (pokemon_id, owner_name) VALUES ({pokemon_id}, "{owner["name"]}")'
                cursor.execute(query)
                connection.commit()
        except:
            print("Error in OwnedBy insert")


def not_in_types(type):
    try:
        with connection.cursor() as cursor:
            query = f'SELECT * FROM types WHERE name = "{type}"'
            cursor.execute(query)
            result = cursor.fetchall()
            connection.commit()
            return len(result) == 0
    except:
        print("Error")


def insert_type(name,type):
    # if not_in_types(type):
        try:
            with connection.cursor() as cursor:
                query = f'INSERT INTO PokemonsTypes (pokemon_name,pokemon_type) VALUES ("{name}","{type}")'
                cursor.execute(query)
                connection.commit()
        except:
            print("Error in types insert")


def insert_pokemon(pokemon):
    insert_type(pokemon["name"],pokemon["type"])
    try:
        with connection.cursor() as cursor:
            query = f'INSERT INTO Pokemons (id, name, height, weight) VALUES ({pokemon["id"]}, ' \
                    f'"{pokemon["name"]}", {pokemon["height"]}, {pokemon["weight"]})'
            cursor.execute(query)
            connection.commit()
    except:
        print("Error in pokemon insert")
    insert_owners(pokemon["ownedBy"], pokemon["id"])


def insert_to_database(pokemon_data):
    for pokemon in pokemon_data:
        insert_pokemon(pokemon)


if __name__ == '__main__':
    pokemon_data = load_data()
    insert_to_database(pokemon_data)
