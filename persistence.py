import database_common


@database_common.connection_handler
def collect_all_board(cursor):
    cursor.execute("""
        SELECT id, title, user_id
        FROM board
        ORDER BY id;
    """)
    return cursor.fetchall()


@database_common.connection_handler
def get_users_data(cursor):
    cursor.execute("""SELECT *
    FROM users
    ORDER BY  name""")
    datadict = cursor.fetchall()
    return datadict


@database_common.connection_handler
def save_registration_data(cursor, hashed_password, user_name, date):
    cursor.execute("""
    INSERT INTO users(name, password, registration_date)
    VALUES (%s, %s, date_trunc('second', %s));
    """, (user_name, hashed_password, date))


@database_common.connection_handler
def get_login_data(cursor, username):
    cursor.execute("""SELECT *
    FROM users
    WHERE  name = %(username)s""",
                   {'username': username})
    datadict = cursor.fetchone()
    if not datadict:
        data = {}
        return data
    else:
        data = datadict
        return data


@database_common.connection_handler
def get_statuses(cursor):
    cursor.execute("""
    SELECT title status
    FROM statuses;
    """)
    return cursor.fetchall()


@database_common.connection_handler
def get_all_cards_status_id_for_a_board(cursor, board_id):
    cursor.execute("""
    SELECT DISTINCT status_id, status_order FROM cards
    WHERE board_id = %(board_id)s
    ORDER BY status_order
    """, {'board_id': board_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_card_status_board(cursor, board_id):
    cursor.execute("""
    SELECT cards.id as card_id, cards.title as card, s.title as status, b.title as board
    FROM cards
    JOIN statuses s on cards.status_id = s.id
    JOIN board b on cards.board_id = b.id
    WHERE board_id = %(board_id)s
    ORDER BY "order"
    """, {'board_id': board_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_status_title_by_id(cursor, card_id):
    cursor.execute("""
    SELECT title FROM statuses
    WHERE id = %(card_id)s
    """, {'card_id': card_id})
    return cursor.fetchone()


@database_common.connection_handler
def update_boardname(cursor, oldnameid, newname):
    cursor.execute("""UPDATE board
    SET title = %(newname)s
    WHERE id = %(oldnameid)s""",
                   {'oldnameid': oldnameid, 'newname': newname})


@database_common.connection_handler
def get_board_id_by_name(cursor, oldname):
    cursor.execute("""SELECT  id
    FROM board
    WHERE title = %(oldname)s""",
                   {'oldname': oldname})
    return cursor.fetchone()


@database_common.connection_handler
def save_new_board(cursor):
    cursor.execute("""
    INSERT INTO board (title)
    VALUES ('New Board');
    """)
    return None


@database_common.connection_handler
def add_new_status(cursor, status_name):
    cursor.execute("""INSERT INTO statuses(title)
    VALUES (%(status_name)s)
    """, {'status_name': status_name})


@database_common.connection_handler
def add_card_by_board_and_status(cursor, board_id, status_id, status_order):
    cursor.execute("""INSERT INTO cards(board_id, title, status_id, "order", status_order)
    VALUES (%(board_id)s, 'New card', %(status_id)s, 0, %(status_order)s)""", {'board_id': board_id,
                                                                            'status_id': status_id,
                                                                            'status_order': status_order})


@database_common.connection_handler
def get_status_by_name(cursor, name):
    cursor.execute('''SELECT id FROM statuses
    WHERE title = %(name)s''', {'name': name})
    return cursor.fetchone()


@database_common.connection_handler
def delete_board(cursor, board_id):
    cursor.execute("""
    DELETE
    FROM board
    WHERE id = %(board_id)s
    """, {'board_id': board_id})


@database_common.connection_handler
def save_new_card(cursor, board_id, order_number):
    cursor.execute("""
        INSERT INTO cards (board_id, title, status_id, "order")
        VALUES (%(board_id)s, 'New Card', 1, %(order_number)s);
        """, {'board_id': board_id, 'order_number': order_number})


@database_common.connection_handler
def add_new_board(cursor, board_name, user_id):
    cursor.execute("""
    INSERT INTO board (title, user_id)
    VALUES (%(board_name)s, %(user_id)s)
    """, {'board_name': board_name, 'user_id': user_id})


@database_common.connection_handler
def get_board_id_by_title(cursor, board_name):
    cursor.execute("""
    SELECT id
    FROM board
    WHERE title = %(board_name)s
    """, {'board_name': board_name})
    return cursor.fetchone()


@database_common.connection_handler
def add_default_status_to_new_board(cursor, board_id):
    cursor.execute("""INSERT INTO cards (board_id, title, status_id, "order")
    VALUES (%(board_id)s, 'New card', 1, 0);

    INSERT INTO cards(board_id, title, status_id, "order")
    VALUES( %(board_id)s, 'New card', 2, 0);
    
    INSERT INTO cards(board_id, title, status_id, "order")
    VALUES( %(board_id)s, 'New card', 3, 0);
    
    INSERT INTO cards(board_id, title, status_id, "order")
    VALUES( %(board_id)s, 'New card', 4, 0);
    
    """, {'board_id': board_id})


@database_common.connection_handler
def rename_board_sql(cursor, board_id, board_name):
    cursor.execute("""
    UPDATE board
    SET title = %(board_name)s
    WHERE id = %(board_id)s
    """, {'board_name': board_name, 'board_id': board_id})


@database_common.connection_handler
def rename_column(cursor, board_id, status_id, old_status_id):
    cursor.execute("""
    UPDATE cards
    SET status_id = %(status_id)s
    WHERE board_id = %(board_id)s AND status_id = %(old_status_id)s
    """, {"board_id": board_id, "status_id": status_id, "old_status_id": old_status_id})


@database_common.connection_handler
def get_last_card(cursor):
    cursor.execute("""
    SELECT id
    FROM cards
    ORDER BY id DESC
    LIMIT 1;
    """)
    return cursor.fetchone()


@database_common.connection_handler
def change_card_name(cursor, card_id, new_name):
    cursor.execute("""
    UPDATE cards
    SET title = %(new_name)s
    WHERE id = %(card_id)s
    """, {'card_id': card_id, 'new_name': new_name})


@database_common.connection_handler
def get_last_card_by_board_id(cursor, board_id):
    cursor.execute("""
    SELECT id, board_id
    FROM cards
    WHERE board_id = %(board_id)s
    ORDER BY id
    LIMIT 1  
    """, {'board_id': board_id})
    return cursor.fetchone()


@database_common.connection_handler
def delete_card_sql(cursor, card_id):
    cursor.execute("""
    DELETE FROM cards
    WHERE id = %(card_id)s
    """, {'card_id': card_id})


@database_common.connection_handler
def change_card_status(cursor, card_id, board_id, status_id):
    cursor.execute("""
    UPDATE cards
    SET status_id = %(status_id)s, board_id = %(board_id)s
    WHERE id = %(card_id)s
    """, {'card_id': card_id, 'board_id': board_id, 'status_id': status_id})


@database_common.connection_handler
def get_highest_order(cursor, board_id):
    cursor.execute("""
    SELECT "order" as order_number
    FROM cards
    WHERE board_id = %(board_id)s AND status_id = 1
    ORDER BY "order" DESC
    LIMIT 1;
    """, {'board_id': board_id})
    return cursor.fetchone()


@database_common.connection_handler
def get_highest_status_order(cursor, board_id):
    cursor.execute("""
    SELECT status_order
    FROM cards
    WHERE board_id = %(board_id)s
    ORDER BY status_order DESC
    LIMIT 1;
    """, {'board_id': board_id})
    return cursor.fetchone()


@database_common.connection_handler
def get_user_id_by_user_name(cursor, user_name):
    cursor.execute("""
    SELECT id
    FROM users
    WHERE name = %(user_name)s
    """, {'user_name': user_name})
    return cursor.fetchone()


@database_common.connection_handler
def add_new_board_without_id(cursor, board_name):
    cursor.execute("""
    INSERT INTO board (title)
    VALUES (%(board_name)s)
    """, {'board_name': board_name})
