import persistence


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

    print(all_board)
    return all_board


def get_statuses_for_specific_board(board_id):
    return [persistence.get_status_title_by_id(card_status['status_id'])['title'] for card_status
            in persistence.get_all_cards_status_id_for_a_board(board_id)]


def get_cards_for_board(board_id):
    status_ids = persistence.all_status_ids_of_a_board(board_id)

    persistence.get_card_name_by_status_id(status_id, board_id)
    return


def get_statuses_from_persistence():
    return persistence.get_statuses

# def get_cards_for_board(board_id):
#     persistence.clear_cache()
#     all_cards = persistence.get_cards()
#     matching_cards = []
#     for card in all_cards:
#         if card['board_id'] == str(board_id):
#             card['status_id'] = get_card_status(card['status_id'])  # Set textual status for the card
#             matching_cards.append(card)
#     return matching_cards
