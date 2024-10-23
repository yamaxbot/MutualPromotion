import sqlite3 as sq

async def start_sq():
    global db, cur

    db = sq.connect('data.db')
    cur = sq.Cursor(db)
    
    cur.execute("CREATE TABLE IF NOT EXISTS clients(id TEXT, point TEXT, subscription TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS orders(number TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS chats(chat_id TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS fast_orders(number TEXT, des TEXT, percentage TEXT, users TEXT, customer TEXT, issuance TEXT)")

    cur.execute("INSERT INTO orders VALUES(?)", (0,))
    
    db.commit()

async def add_all_clients_sql(id):
    cur.execute("INSERT INTO clients VALUES(?, ?, ?)", (id, 0, '0'))
    db.commit()

async def get_clients_sql(id):
    return cur.execute("SELECT * FROM clients WHERE id = ?", (id,)).fetchone()


async def add_points_sql(id):
    point = cur.execute("SELECT * FROM clients WHERE id = ?", (id,)).fetchone()
    point = point[1]
    cur.execute("UPDATE clients SET point = ? WHERE id = ?", (int(point)+1, id))
    db.commit()


async def add_two_points_sql(id):
    point = cur.execute("SELECT * FROM clients WHERE id = ?", (id,)).fetchone()
    point = point[1]
    cur.execute("UPDATE clients SET point = ? WHERE id = ?", (int(point)+2, id))
    db.commit()


async def add_number_sql(qul):
    cur.execute("UPDATE orders SET number = ? WHERE number = ?", (qul+1, qul,))
    db.commit()


async def get_number_sql():
    return cur.execute("SELECT * FROM orders").fetchall()


async def add_fast_orders_sql(numbers, des, percentage, id):
    cur.execute("INSERT INTO fast_orders VALUES(?, ?, ?, ?, ?, ?)", (numbers, des, percentage, '.', id, 1,))
    db.commit()


async def get_all_fast_orders_sql():
    return cur.execute("SELECT * FROM fast_orders WHERE percentage <> '0' ").fetchall()


async def update_fast_orders_sql(percentage, number):
    cur.execute("UPDATE fast_orders SET percentage = ? WHERE number = ?", (percentage, number))
    db.commit()


async def get_fast_orders_number_sql(number):
    ord = cur.execute("SELECT * FROM fast_orders WHERE number = ?", (number, )).fetchone()
    ord = ord[2]
    cur.execute("UPDATE fast_orders SET percentage = ? WHERE number = ?", (int(ord)+1, number, ))
    db.commit()


async def minus_balance_sql(id, point_m):
    people = cur.execute("SELECT * FROM clients WHERE id = ?", (id, )).fetchone()
    point = int(people[1])
    cur.execute("UPDATE clients SET point = ? WHERE id = ?", (point-int(point_m), id, ))
    db.commit()


async def return_points_sql(id, point_p):
    point = cur.execute("SELECT * FROM clients WHERE id = ?", (id,)).fetchone()
    point = point[1]
    cur.execute("UPDATE clients SET point = ? WHERE id = ?", (int(point) + int(point_p), id))
    db.commit()


async def add_chats_sql(chat_id):
    cur.execute("INSERT INTO chats VALUES(?)", (chat_id, ))
    db.commit()


async def delete_chats_sql():
    cur.execute("DELETE FROM chats")
    db.commit()


async def get_chats_sql():
    return cur.execute("SELECT chat_id FROM chats").fetchone()


async def update_id_fast_orders_sql(number, id):
    users = cur.execute("SELECT * FROM fast_orders WHERE number = ?", (number, )).fetchone()
    users = users[3] + str(id) + '.'
    cur.execute("UPDATE fast_orders SET users = ? WHERE number = ?", (users, number, ))
    db.commit()


async def issuance_update_sql(number, issuance):
    cur.execute("UPDATE fast_orders SET issuance = ? WHERE number = ?", (issuance, number, ))
    db.commit()


async def get_all_clients_sql():
    return cur.execute("SELECT * FROM clients").fetchall()


async def subscription_update_sql(id):
    cur.execute("UPDATE clients SET subscription = ? WHERE id = ?", ('1', id, ))
    db.commit()


async def new_get_all_fast_orders_sql(id):
    ls = []
    all_order = cur.execute("SELECT * FROM fast_orders").fetchall()
    for order in all_order:
        if str(id) not in order[3] and order[-1] == '1' and order[-2] != str(id) and int(order[2]) > 0:
            ls.append(order)
    return ls


async def active_orders_sql():
    all_order = cur.execute("SELECT * FROM fast_orders").fetchall()
    ls = []
    for order in all_order:
        if int(order[2]) > 0:
            ls.append(order)
    return ls

async def activ_order_or_no_sql(number):
    order = cur.execute("SELECT * FROM fast_orders WHERE number = ?", (number,)).fetchone()
    if order[2] == '0':
        return order
    else:
        return


async def issue_points_sql(id, point):
    client = cur.execute("SELECT * FROM clients WHERE id = ?", (id, )).fetchone()
    points = int(client[1]) + int(point)
    cur.execute("UPDATE clients SET point = ? WHERE id = ?", (points, id))
    db.commit()