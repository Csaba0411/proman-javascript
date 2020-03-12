import database_common


@database_common.connection_handler
def collect_all_board(cursor):
    cursor.execute("""
        SELECT id, title
        FROM board;
    """)
    return cursor.fetchall()


# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
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


# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# @database_common.connection_handler
# def get_cards_by_board_id(cursor, board_id):
#     cursor.execute("""
#     SELECT title
#     FROM cards
#     WHERE board_id = %(board_id)s
#     """, {'board_id': board_id})
#     return cursor.fetchall()


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
    SELECT DISTINCT status_id FROM cards
    WHERE board_id = %(board_id)s
    ORDER BY status_id
    """, {'board_id': board_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_card_status_board(cursor, board_id):
    cursor.execute("""
    SELECT cards.title as card, s.title as status, b.title as board
    FROM cards
    JOIN statuses s on cards.status_id = s.id
    JOIN board b on cards.board_id = b.id
    WHERE board_id = %(board_id)s
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


# _cache = {}  # We store cached data in this dict to avoid multiple file readings
#
#
# def _get_data(data_type, file, force):
#     """
#     Reads defined type of data from file or cache
#     :param data_type: key where the data is stored in cache
#     :param file: relative path to data file
#     :param force: if set to True, cache will be ignored
#     :return: OrderedDict
#     """
#     if force or data_type not in _cache:
#         _cache[data_type] = _read_csv(file)
#     return _cache[data_type]
#
#
# def clear_cache():
#     for k in list(_cache.keys()):
#         _cache.pop(k)
#
#
# def get_statuses(force=False):
#     return _get_data('statuses', STATUSES_FILE, force)
#
#
# def get_boards(force=False):
#     return _get_data('boards', BOARDS_FILE, force)
#
#
# def get_cards(force=False):
#     return _get_data('cards', CARDS_FILE, force)
