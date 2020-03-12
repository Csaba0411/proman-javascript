from flask import Flask, render_template, url_for, session, request, redirect
from util import json_response

import data_handler

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/", methods=['GET', 'POST'])
def index():
    invalid = ''
    if request.method == 'POST':
        if data_handler.get_login_data(request.form, session) is False:
            invalid = 'Your username or password is invalid!'
    return render_template('index.html', invalid_input=invalid, session=session)


@app.route("/get-boards")
@json_response
def get_boards():
    """
    All the boards
    """
    return data_handler.get_boards()


@app.route('/get-statuses')
@json_response
def get_statuses():
    return data_handler.get_statuses_from_persistence()


@app.route("/get-cards/<int:board_id>")
@json_response
def get_cards_for_board(board_id: int):
    """
    All cards that belongs to a board
    :param board_id: id of the parent board
    """
    return data_handler.get_cards_for_board(board_id)


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('logged_in_id', None)
    return redirect('/')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if session:
        return redirect('/')
    if request.method == "POST":
        if data_handler.comparing_passwords(request.form) is False:
            return render_template('user_registration.html', error='Password Does Not Match! :(')
        elif data_handler.comparing_new_user_name(request.form) is False:
            return render_template('user_registration.html', error='Already registered username!')
        data_handler.adding_registration_data(request.form)
        return redirect('/')
    return render_template('user_registration.html')


@app.route('/rename-board', methods=['GET', 'POST'])
def rename_board():
    new_name = request.get_json()
    data_handler.update_with_boardname(new_name['oldboardname'], new_name['newboardname'])
    return ({'newname': new_name['newboardname']})


@app.route("/save-new-board", methods=['POST', 'GET'])
@json_response
def save_new_board():
    if request.method == 'POST':
        return data_handler.saving_new_board()


@app.route('/new-status/<status_name>')
@json_response
def new_status(status_name):
    data_handler.add_new_status(status_name)


@app.route('/delete/<board_id>')
@json_response
def delete_board(board_id):
    data_handler.delete_board(board_id)


def main():
    app.run(debug=True)

    # Serving the favicon
    with app.app_context():
        app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon/favicon.ico'))


if __name__ == '__main__':
    main()
