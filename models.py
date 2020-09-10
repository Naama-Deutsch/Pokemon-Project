import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="poke",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)


def run_query(query):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    except:
        print("Error in query")


# Exercise 1
def get_heaviest_pokemon():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Pokemons WHERE weight IN (SELECT MAX(weight) from Pokemons)")
            result = cursor.fetchone()
            return result
    except:
        print("Error in query")

def get_location(poke_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM PokemonsLocation WHERE Pokemon_id = "{poke_id}"')
            result = cursor.fetchone()
            return result
    except:
        print("Error in query")

def get_pokemon_by_type(type_name):
    with connection.cursor() as cursor:
        query = f'select * from Pokemons\
             where name in\
             (select pokemon_name from PokemonsTypes\
              where pokemon_type="{type_name}")'
        cursor.execute(query)
        res=cursor.fetchall()
        return res

def update_pokemon_types(pokemone_name,type):
    with connection.cursor() as cursor:
        cursor.execute(
            f'INSERT INTO PokemonsTypes (pokemon_name,pokemon_type) VALUES ("{pokemone_name}","{type["type"]["name"]}")')
        connection.commit()

def add_types(name, types):
    with connection.cursor() as cursor:
        for type in types:
            query = f'INSERT INTO PokemonsTypes (pokemon_name,pokemon_type) VALUES ("{name}","{type}")'
            cursor.execute(query)
            connection.commit()

def insert_pokemon(pokemon):
    with connection.cursor() as cursor:
           query = f'INSERT INTO Pokemons (id, name, height, weight) VALUES ({pokemon["id"]}, ' \
           f'"{pokemon["name"]}", {pokemon["height"]}, {pokemon["weight"]})'
           cursor.execute(query)
           connection.commit()

# Exercise 3
def find_owners(pokemon_name):
    result = run_query(f'SELECT OwnedBy.name \
                    FROM Pokemons JOIN  OwnedBy \
                    WHERE Pokemons.id = OwnedBy.id AND Pokemons.name = "{pokemon_name}" ')
    return list(map(lambda x: x["name"], result))


# Exercise 4
def find_roster(trainer_name):
    result = run_query(f'SELECT Pokemons.name \
                        FROM Pokemons JOIN  OwnedBy \
                        WHERE Pokemons.id = OwnedBy.id AND OwnedBy.name = "{trainer_name}" ')
    return list(map(lambda x: x["name"], result))


# Extension
def find_most_owned():
    return run_query("SELECT * \
                    from Pokemons \
                    WHERE id in \
                    (SELECT id from OwnedBy \
                    group by id having count(*) >= ALL(select count(*) from OwnedBy group by id))")

def delete_pokemon_trainer(poke_name,trainer_name):
    with connection.cursor() as cursor:
        query = f'delete from OwnedBy \
                where owner_name="{trainer_name}" and pokemon_id in\
                                            (select id from Pokemons \
                                            where name="{poke_name}" )'
        cursor.execute(query)
        connection.commit()

if __name__ == '__main__':
    print(get_heaviest_pokemon())
    print(find_by_type("grass"))
    print(find_owners("gengar"))
    print(find_roster("Loga"))
    print(find_most_owned())
