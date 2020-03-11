import database_common


@database_common.connection_handler
def collect_all_board(cursor):
    cursor.execute("""
        SELECT id, title
        FROM board;
    """)
    return cursor.fetchall()


@database_common.connection_handler
def get_cards_by_board_id(cursor, board_id):
    cursor.execute("""
    SELECT title
    FROM cards
    WHERE board_id = %(board_id)s
    """, {'board_id': board_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_statuses(cursor):
    cursor.execute("""
    SELECT title status
    FROM statuses;
    """)
    return cursor.fetchall()


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
