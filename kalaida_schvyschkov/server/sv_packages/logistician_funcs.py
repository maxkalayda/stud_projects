from sv_packages.common_funcs import create_connection

def isEmpty(data):
    i = 0
    for val in data.values():
        if ((val == None) or (val == "")): i += 1
    return False if len(data.values()) != i else True

def postHandlerLogisticianByMaterial(data):
    print(f"data = {data}")
    if isEmpty(data) == True:
        SQLreq = "SELECT * FROM T_supply_directory;"
        print(f"SQLreq = {SQLreq}")
    else:
        SQLreq = "SELECT * FROM T_supply_directory " \
                 "WHERE sup_code IN (SELECT tsu.sup_code FROM T_storage_units AS tsu " \
                 "WHERE tsu.material_code IN (SELECT tmd.material_code FROM T_material_directory AS tmd " \
                 "WHERE"

        for item in data.items():
            key = list(item)[0]
            val = list(item)[1]
            if ((val == None) or (val == "")): continue
            SQLreq += f" tmd.{key} = '{val}' AND"

        SQLreq = SQLreq[: -3] # Удаление последнего AND
        SQLreq += "));"
        print(f"SQLreq = {SQLreq}")

    db_path = "sv_packages/database/sqlite.db"
    connection = create_connection(db_path)
    sups = connection.execute(SQLreq).fetchall()
    connection.close()
    return sups

def postHandlerLogisticianByBank(data):
    print(f"data = {data}")
    if isEmpty(data) == True:
        SQLreq = "SELECT * FROM T_supply_directory;"
        print(f"SQLreq = {SQLreq}")
    else:
        for item in data.items():
            key = list(item)[0]
            val = list(item)[1]
            if ((val == None) or (val == "")): data[key] = "%"
        SQLreq = f"SELECT * FROM T_supply_directory WHERE bank_address LIKE '%{data['index']}, {data['city']}, {data['street']} st., {data['building']}%';";
        print(f"SQLreq = {SQLreq}")

    db_path = "sv_packages/database/sqlite.db"
    connection = create_connection(db_path)
    sups = connection.execute(SQLreq).fetchall()
    connection.close()
    print(len(sups))
    buff = {"sum" : len(sups)}
    return buff

def postHandlerLogisticianAdd(data):
    print(f"data = {data}")

    SQLreq = f"""INSERT INTO T_supply_directory(sup_name, inn_code, org_address, bank_address, bank_acc) VALUES"""
    for item in data.items():
        val = list(item)[1]
        if ((val == None) or (val == "")):
            buff = {"res": " не удалось добавить поставщика. Все поля должны быть заполнены!"}
            return buff

    SQLreq = f"""{SQLreq} ('{data['sup_name']}', '{data['inn_code']}', '{data['org_address']}', '{data['bank_address']}', '{data['bank_acc']}');"""

    print(f"SQLreq = {SQLreq}")

    db_path = "sv_packages/database/sqlite.db"
    connection = create_connection(db_path)
    connection.execute("""BEGIN;""").fetchall()
    connection.execute(SQLreq).fetchall()
    connection.execute("""COMMIT;""").fetchall()
    connection.close()
    buff = {"res": " поставщик успешно добавлен в базу данных!"}
    return buff

def postHandlerLogisticianDelete(data):
    print(f"data = {data}")

    if isEmpty(data) == True:
        buff = {"res": " не удалось удалить поставщика. Должно быть заполнено хотя бы одно поле!"}
        return buff
    else:
        SQLreq = "SELECT * FROM T_supply_directory WHERE";

        for item in data.items():
            key = list(item)[0]
            val = list(item)[1]
            if ((val == None) or (val == "")): continue
            SQLreq += f" {key} = '{val}' AND"

        SQLreq = SQLreq[: -3] # Удаление последнего AND
        SQLreq += ";"
        print(f"SQLreq = {SQLreq}")

    db_path = "sv_packages/database/sqlite.db"
    connection = create_connection(db_path)
    sups = connection.execute(SQLreq).fetchall()
    connection.close()

    if len(sups) == 0:
        buff = {"res": " не удалось удалить поставщика. Поставщик не найден!"}
        return buff

    SQLreq = f"""DELETE FROM T_supply_directory WHERE"""

    for item in data.items():
        key = list(item)[0]
        val = list(item)[1]
        if ((val == None) or (val == "")): continue
        SQLreq += f" {key} = '{val}' AND"

    SQLreq = SQLreq[: -3]  # Удаление последнего AND
    SQLreq += ";"

    print(f"SQLreq = {SQLreq}")

    db_path = "sv_packages/database/sqlite.db"
    connection = create_connection(db_path)
    connection.execute("""BEGIN;""").fetchall()
    connection.execute(SQLreq).fetchall()
    connection.execute("""COMMIT;""").fetchall()
    connection.close()
    buff = {"res": " поставщик успешно удалён из базы данных!"}
    return buff
