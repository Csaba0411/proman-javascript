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
    statuses = persistence.get_statuses()
    all_board = persistence.collect_all_board()
    for board in all_board:
        status_number = 1
        for status in statuses:
            board[f'status{status_number}'] = status['status']
            status_number += 1
    return all_board


def get_cards_for_board(board_id):
    return persistence.get_cards_by_board_id(board_id)


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
