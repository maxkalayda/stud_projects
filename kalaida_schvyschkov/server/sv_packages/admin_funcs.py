from sv_packages.common_funcs import create_connection
db_path = "sv_packages/database/login_params.db"

def adminDeleteFunc(inputs):

    SQL = "DELETE FROM user"
    i = 1
    for item in inputs.items():
        key = list(item)[0]
        print(key)
        value = list(item)[1]
        print(value)

        if (value != ""):
            if (i == 1):
                SQL = SQL + " WHERE"
                SQL = SQL + " " + key + " = '" + value + "'"
            else:
                if (i != 3):
                    SQL = SQL + " AND " + key + " = '" + value + "'"
                else:
                    SQL = SQL + ";"
        i = i + 1

    print(SQL)
    db = create_connection(db_path)
    db.execute("BEGIN;").fetchall()
    db.execute(SQL).fetchall()
    db.execute("COMMIT;").fetchall()
    db.close()

    return [(inputs['id'], inputs['login'], inputs['passwd'])]

def adminEditFunc(inputs):

    SQL = "UPDATE user SET login = '" + inputs['login'] + "', passwd = '" + inputs['passwd']  + "' WHERE id = " + inputs['id'] + ";"

    print(SQL)
    db = create_connection(db_path)
    db.execute("BEGIN;").fetchall()
    db.execute(SQL).fetchall()
    db.execute("COMMIT;").fetchall()
    db.close()

    return [(inputs['id'], inputs['login'], inputs['passwd'])]

def adminViewFunc(inputs):

    SQL = "SELECT * FROM user";
    i = 1
    for item in inputs.items():
        key = list(item)[0]
        print(key)
        value = list(item)[1]
        print(value)

        if (value != ""):
            if (i == 1):
                SQL = SQL + " WHERE"
                SQL = SQL + " " + key + " = '" + value + "'"
            else:
                if (i != 3):
                    SQL = SQL + " AND " + key + " = '" + value + "'"
                else:
                    SQL = SQL + ";"
        i = i + 1

    print(SQL)

    db = create_connection(db_path)
    result = db.execute(SQL).fetchall()
    db.close()
    return result