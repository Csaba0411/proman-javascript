import persistence
# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

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


# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


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
            board[stat] = [card['card'] for card in cards if card['status'] == stat]
    return all_board


def get_statuses_for_specific_board(board_id):
    return [persistence.get_status_title_by_id(card_status['status_id'])['title'] for card_status
            in persistence.get_all_cards_status_id_for_a_board(board_id)]


# def get_cards_for_board(board_id):
#     status_ids = persistence.all_status_ids_of_a_board(board_id)
#     persistence.get_card_name_by_status_id(status_id, board_id)
#     return


def get_statuses_from_persistence():

    return persistence.get_statuses


def update_with_boardname(oldname, newname):
    oldnameid = persistence.get_board_id_by_name(oldname)
    persistence.update_boardname(oldnameid['id'], newname)


def saving_new_board():
    return persistence.save_new_board()


def add_new_status(status_name):
    persistence.add_new_status(status_name)


def delete_board(board_id):
    persistence.delete_board(board_id)


# def get_cards_for_board(board_id):
#     persistence.clear_cache()
#     all_cards = persistence.get_cards()
#     matching_cards = []
#     for card in all_cards:
#         if card['board_id'] == str(board_id):
#             card['status_id'] = get_card_status(card['status_id'])  # Set textual status for the card
#             matching_cards.append(card)
#     return matching_cards
