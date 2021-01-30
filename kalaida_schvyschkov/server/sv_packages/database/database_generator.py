import sqlite3 as db
from sqlite3 import Error
from random import choice, randint

def create_connection(path):
    connection = None
    try:
        connection = db.connect(path)
        print(db.version)
    except Error as e:
        print(e)
    return (connection)

def sql_execute(sql, conn):
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def generate_db():

    size_of_T_supply_directory = 200
    size_of_T_storage_units = round(size_of_T_supply_directory*1.3)

    db_path = "sqlite.db"
    connection = create_connection(db_path)

    sql_execute("""BEGIN;""", connection)
    sql_command = """DROP TABLE IF EXISTS T_material_directory;"""
    sql_execute(sql_command, connection)
    sql_command = """DROP TABLE IF EXISTS T_supply_directory;"""
    sql_execute(sql_command, connection)
    sql_command = """DROP TABLE IF EXISTS T_storage_units;"""
    sql_execute(sql_command, connection)
    sql_execute("""COMMIT;""", connection)

# Таблица "Справочник материалов"

    sql_execute("""BEGIN;""", connection)
    sql_command = """CREATE TABLE T_material_directory (
                        material_code integer PRIMARY KEY AUTOINCREMENT,
                        class_code integer NOT NULL,
                        group_code integer NOT NULL,
                        material_name text NOT NULL,
                        measure_unit_name text NOT NULL,
                        measure_unit_code integer NOT NULL
                    );"""
    sql_execute(sql_command, connection)

    units_list = ["kg", "m", "l", "kg, m", "kg, l", "m, l", "kg, m, l"]

    material_dict = {"metal": units_list[0], "plastic": units_list[6], "wood": units_list[3], "glass": units_list[6],
                     "ceramics": units_list[6], "synthetic fibres": units_list[4], "composites": units_list[6],
                     "paper": units_list[3], "stone": units_list[3], "leather": units_list[3], "minerals": units_list[3],
                     "rubber": units_list[3], "thread": units_list[1], "plaster": units_list[4],
                     "chemicals": units_list[4], "water": units_list[0]}

    sql_command = f"""INSERT INTO T_material_directory(class_code, group_code, material_name,
                                                        measure_unit_name, measure_unit_code) VALUES"""
    i = 0
    for mat in material_dict:
        i = i+1
        sql_command = f"""{sql_command} ({randint(100,999)}, {randint(1000,9999)}, '{mat}', '{material_dict[mat]}', {[j for j,n in enumerate(units_list) if n == material_dict[mat]][0]+11}),"""
    sql_command = sql_command[:-1]
    sql_execute(sql_command, connection)
    sql_execute("""COMMIT;""", connection)

# ____________________________________________
# Таблица "Поставщики"

    sql_execute("""BEGIN;""", connection)
    sql_command = """CREATE TABLE T_supply_directory (
                        sup_code integer PRIMARY KEY AUTOINCREMENT,
                        sup_name text NOT NULL,
                        inn_code integer NOT NULL,
                        org_address text NOT NULL,
                        bank_address text NOT NULL,
                        bank_acc big integer NOT NULL
                    );"""
    sql_execute(sql_command, connection)

    sup_name_parts_list = ["Soap", "Car", "Home", "Sweet", "Tea", "Lovely", "Work", "Repairing", "Computer", "Logic",
                           "Help", "Wrong", "Milk", "Trash", "War", "University", "Life", "Nice", "Stream", "Mommy",
                           "Stupid", "Big", "Small", "Daddy"]

    address_city_list = ["Moscow", "New-York", "Paris", "London", "Ugugu", "Stavropol", "Detroit", "Alexandria", "Luada", "Aljir", "Tirana", "Manama", "Brussel", "Sofia"]
    address_street_list = ["Main", "Green", "Yellow", "Red", "Dragon", "Sheep", "Creepy", "Lost", "Second", "Third", "First", "Trapiado"]

    sql_command = f"""INSERT INTO T_supply_directory(sup_name, inn_code, org_address, bank_address, bank_acc) VALUES"""
    for i in range(size_of_T_supply_directory):
        sql_command = f"""{sql_command} ('{choice(sup_name_parts_list) + ' ' + choice(sup_name_parts_list)}', {i+randint(1000000000, 9999900000)},
                    '{str(randint(100000,999999)) + ', ' + choice(address_city_list) + ', ' + choice(address_street_list) + ' st., ' + str(randint(1,120))}',
                    '{str(randint(100000,999999)) + ', ' + choice(address_city_list) + ', ' + choice(address_street_list) + ' st., ' + str(randint(1,120))}',
                    '{i+randint(10000000001000000000, 99999000009999900000)}'),"""
    sql_command = sql_command[:-1]
    sql_execute(sql_command, connection)
    sql_execute("""COMMIT;""", connection)

# ____________________________________________
# Таблица "Единицы хранения"

    product_list = ["Door", "Toy", "Juice", "Food", "TV", "Computer", "Cake", "Phone", "Carpet"]

    sql_execute("""BEGIN;""", connection)
    sql_command = """CREATE TABLE T_storage_units (
                        order_num integer PRIMARY KEY AUTOINCREMENT,
                        time_date date NOT NULL DEFAULT(date(CURRENT_TIMESTAMP)),
                        sup_code integer NOT NULL REFERENCES T_supply_directory(sup_code),
                        balance_acc integer NOT NULL,
                        code_of_dir_of_documents integer NOT NULL,
                        product_name text NOT NULL,
                        num_of_document integer NOT NULL,
                        material_code integer NOT NULL REFERENCES T_material_directory(material_code),
                        material_acc integer NOT NULL,
                        measure_unit_code integer NOT NULL REFERENCES T_material_directory(measure_unit_code),
                        amount_of_material integer NOT NULL,
                        unit_price integer NOT NULL
                    );"""
    sql_execute(sql_command, connection)

    sql_command = f"""INSERT INTO T_storage_units(sup_code, balance_acc, code_of_dir_of_documents, product_name, 
                                                    num_of_document, material_code, material_acc, measure_unit_code, 
                                                    amount_of_material, unit_price) VALUES"""
    for i in range(size_of_T_storage_units):
        rmaterial = choice(list(material_dict.keys()))
        sql_command = f"""{sql_command} ({randint(1, 50)}, {randint(100000, 999999)}, {randint(100000, 999999)}, '{choice(product_list)}', {randint(100000, 999999)}, 
                        (SELECT material_code FROM T_material_directory WHERE material_name = '{rmaterial}'), {randint(1000, 9999)},
                        (SELECT measure_unit_code FROM T_material_directory WHERE material_name = '{rmaterial}'), {randint(1, 999)}, {randint(1000, 9999)}),"""
    sql_command = sql_command[:-1]
    sql_execute(sql_command, connection)
    sql_execute("""COMMIT;""", connection)
    connection.close()

    print("\n Done!\n")

def view_db():
    db_path = "sqlite.db"
    connection = create_connection(db_path)
    sql_command = """SELECT * FROM T_storage_units;"""
    sql_execute(sql_command, connection)
    sql_command = """SELECT * FROM T_supply_directory;"""
    sql_execute(sql_command, connection)
    sql_command = """SELECT * FROM T_material_directory;"""
    sql_execute(sql_command, connection)
    connection.close()
    print("\n Done!\n")

if __name__ == '__main__':
    a = 0
    while True:
        try:
            a = int(input(" 1) Generate new db;\n 2) View db;\n 3) Exit.\n Type in: "))
        except ValueError:
            print(" Wrong input!")
            continue
        if (a == 1):
            generate_db()
        elif (a == 2):
            view_db()
        elif (a == 3):
            exit()
        else:
            print(" Wrong number!")
            continue