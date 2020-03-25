import persistence

from datetime import datetime
import bcrypt


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


def comparing_passwords(passwords):
    password = passwords['password']
    password_again = passwords['password_again']
    return password == password_again


def comparing_new_user_name(registration_details):
    all_users = persistence.get_users_data()
    for item in all_users:
        if item['name'] == registration_details['username']:
            return False
    return True


def adding_registration_data(registration_data):
    dt = datetime.now()
    hashed_password = hash_password(registration_data["password"])
    persistence.save_registration_data(hashed_password, registration_data["username"], dt)


def get_login_data(login_data, cookiedata):
    login = persistence.get_login_data(login_data['user'])
    if not login:
        return False
    if login_data['user'] == login['name'] and verify_password(login_data['password'], login['password']) is True:
        cookiedata['username'] = login_data['user']
        cookiedata['logged_in_id'] = login['id']
        return True
    return False


def get_card_status(status_id):
    """
    Find the first status matching the given id
    :param status_id:
    :return: str
    """
    statuses = persistence.get_statuses()
    return next((status['title'] for status in statuses if status['id'] == str(status_id)), 'Unknown')


def get_boards():
    all_board = persistence.collect_all_board()
    for board in all_board:
        cards = persistence.get_card_status_board(board['id'])
        board['status'] = get_statuses_for_specific_board(board['id'])
        for stat in board['status']:
            board[stat] = [(card['card'], card['card_id']) for card in cards if card['status'] == stat]
    return all_board


def get_statuses_for_specific_board(board_id):
    return [persistence.get_status_title_by_id(card_status['status_id'])['title'] for card_status
            in persistence.get_all_cards_status_id_for_a_board(board_id)]


def get_statuses_from_persistence():
    return persistence.get_statuses


def update_with_boardname(oldname, newname):
    oldnameid = persistence.get_board_id_by_name(oldname)
    persistence.update_boardname(oldnameid['id'], newname)


def add_new_status(board_id, status_name):
    latest_status_order = persistence.get_highest_status_order(board_id)
    persistence.add_new_status(status_name)
    status_id = persistence.get_status_by_name(status_name)
    persistence.add_card_by_board_and_status(board_id, status_id['id'], int(latest_status_order['status_order']) + 1)


def delete_board(board_id):
    persistence.delete_board(board_id)


def saving_new_card(board_id):
    highest_order = persistence.get_highest_order(board_id)
    return persistence.save_new_card(board_id, int(highest_order['order_number']) + 1)


def saving_new_board(board_name):
    persistence.add_new_board(board_name)
    board_id = persistence.get_board_id_by_title(board_name)
    persistence.add_default_status_to_new_board(board_id['id'])
    last_card_for_new_board = persistence.get_last_card_by_board_id(board_id['id'])
    return last_card_for_new_board


def rename_board(board_id, new_name_for_board):
    persistence.rename_board_sql(board_id, new_name_for_board)


def rename_column(board_id, column_name, old_col_name):
    persistence.add_new_status(column_name)
    status_id = persistence.get_status_by_name(column_name)
    old_status_id = persistence.get_status_by_name(old_col_name)
    persistence.rename_column(board_id, status_id['id'], old_status_id['id'])


def get_last_card():
    return persistence.get_last_card()


def change_card_name_data_handler(card_id, new_name):
    persistence.change_card_name(card_id, new_name)


def delete_card(card_id):
    persistence.delete_card_sql(card_id)


def change_card_status(card_id, board_id, new_status_name):
    status_id = persistence.get_status_by_name(new_status_name)
    persistence.change_card_status(card_id, board_id, status_id['id'])
