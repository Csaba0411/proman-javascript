// It uses data_handler.js to visualize elements
import {dataHandler} from "./data_handler.js";

export let dom = {
    init: function () {
        // This function should run once, when the page is loaded.
    },
    loadBoards: function () {
        document.querySelector('#boards').textContent = '';
        // retrieves boards and makes showBoards called
        dataHandler.getBoards(function (boards) {
            dom.showBoards(boards);
        });
    },
    showBoards: function (boards) {
        // shows boards appending them to #boards div
        // it adds necessary event listeners also

        let boardList = '';
        for (let board of boards) {
            boardList += `
                <section class="board">
                <div class="board-header"><button class="board-title">${board.title}</button>
                <button class="board-add" data-board-id="${board['id']}">Add Card</button>
                <button class="board-add add-status" data-board-id="${board['id']}">Add status</button>
                <button class="board-toggle"><i class="fas fa-chevron-down toggle-button"></i></button>
                <div class="board-toggle"><i class="fas fa-trash-alt board-delete" data-board-id="${board['id']}"></i></div>
                </div>
                <div class="board-columns">`;
            for (let stat of board['status']) {
                if (stat === 'new') {
                    boardList +=
                        `<div class="board-column column-for-new-cards" data-board-id="${board['id']}">
                        <div class="board-column-title">${stat}</div>
                        <div class="board-column-content">`;
                } else {
                    boardList +=
                        `<div class="board-column">
                        <div class="board-column-title">${stat}</div>
                        <div class="board-column-content">`;
                }
                for (let card of board[stat]) {
                    boardList +=
                        `<div class="card">
                            <div class="card-remove"><i class="fas fa-trash-alt"></i></div>
                            <div class="card-title">${card}</div>
                        </div>`

                }
                boardList +=
                    `</div>
                     </div>`
            }
            boardList +=
                `</div>
                     </section>`
        }
        const outerHtml = `
            <div class="board-container">
                ${boardList}
            </div>
        `;
        let boardsContainer = document.querySelector('#boards');
        boardsContainer.insertAdjacentHTML("beforeend", outerHtml);
        renameFunction();
        hideShowColumn();
        addColumn();
        deleteBoard();

        document.getElementById("plus-sign").addEventListener("click", function () {
            dataHandler.getBoards(function (boards) {
                let board_id = 0;
                for (let board of boards) {
                    if (board_id < board['id']) {
                        board_id = board['id'];
                    }
                }
                let newBoard =
                    `<section class="board">
                    <div class="board-header"><button class="board-title">New Board</button>
                    <button class="board-add" data-board-id="${board_id}">Add Card</button>
                    <button class="board-add add-status" data-board-id="${board_id}">Add status</button>
                    <button class="board-toggle"><i class="fas fa-chevron-down"></i></button>
                    </div></section>`;

                let boardsContainer = document.querySelector('.board-container');
                boardsContainer.insertAdjacentHTML("beforeend", newBoard);

                let data = "dog";
                dataHandler.addBoard(data, function () {
                    console.log('testing')
                });
                renameFunction();
                let boardsHeaders = document.querySelectorAll('.board-header');
                boardsHeaders[boardsHeaders.length - 1].innerHTML += `<div class="board-toggle"><i class="fas fa-trash-alt board-delete"></i></div>`;
            });
        });

    let addCardButtons = document.getElementsByClassName("board-add");
        for (let button of addCardButtons){
            button.addEventListener("click", function () {
            let newCard =
                `<div class="card">
                            <div class="card-remove"><i class="fas fa-trash-alt"></i></div>
                            <div class="card-title">New Card</div>
                        </div>`;

            let board_id = this.dataset.boardId;
            let allCardContainer = document.getElementsByClassName('column-for-new-cards');
            for (let cardContainer of allCardContainer) {
                if (cardContainer.dataset.boardId === board_id) {
                    cardContainer.insertAdjacentHTML("beforeend", newCard);
                }
            }

            dataHandler.addCard(board_id, function () {
                console.log('testing')
            });
        });
        }
    },
    loadCards: function (boardId) {
        // retrieves cards and makes showCards called
    },
    showCards: function (cards) {
        // shows the cards of a board
        // it adds necessary event listeners also
    },
    // here comes more features
};

function renameFunction() {
    let rename = document.querySelectorAll('.board-title');
    for (let name of rename) {
        name.addEventListener('click', function () {
            let boardName = document.querySelector('.modal-title');
            let modal = document.querySelector('#small-modal');
            boardName.innerHTML = name.innerHTML;
            modal.style.display = "block";
            document.querySelector('.modal-footer').innerHTML =
                `<button id="small-close" type="button" class="btn btn-secondary" data-dismiss="modal">Save</button>`;
            let saveButton = document.querySelector('#small-close');
            saveButton.addEventListener('click', function () {
                modal.style.display = "none";
                let newName = document.getElementById('textarea').value;
                let data = {'oldboardname': name.innerHTML, 'newboardname': newName};
                dataHandler.sendNewName(data, function (brandNewName) {
                    console.log(brandNewName);
                    name.innerHTML = brandNewName.newname;
                    document.querySelector('.modal-footer').innerHTML = '';
                    document.getElementById('textarea').value = '';
                })

            });
            let crossButton = document.querySelector('.close');
            crossButton.addEventListener('click', function () {
                modal.style.display = "none";
                document.querySelector('.modal-footer').innerHTML = '';
                document.getElementById('textarea').value = '';
            })

        })
    }
}

let hideShowColumn = function () {
    let boards = document.querySelectorAll('.board');

    for (let board of boards) {
        let toggleButton = board.querySelector('.board-toggle');
        toggleButton.addEventListener('click', function () {
            let columns = board.querySelector('.board-columns');
            if (columns.classList.contains('hide-element')) {
                columns.classList.remove('hide-element')
            } else {
                columns.classList.add('hide-element')
            }
        })
    }
};

let addColumn = function () {
    let statusButton = document.querySelectorAll('.add-status');
    for (let button of statusButton) {
        button.addEventListener('click', function (e) {
            let name = prompt('New status name:');
            apiFetch(name);
            e.preventDefault()
        })
    }

    function apiFetch(name) {
        fetch(`/new-status/${name}`)
            .then(response => response)
    }
};


let deleteBoard = function () {
    let deleteButtonsForBoard = document.querySelectorAll('.board-delete');
    for (let button of deleteButtonsForBoard) {
        button.addEventListener('click', function (event) {
            let boardId = button.dataset.boardId;
            sendDataAPI(boardId, dom.loadBoards);
        })
    }

    function sendDataAPI(data, callback) {
        fetch(`/delete/${data}`)
            .then(response => response)
            .then(data => callback(data))
    }
};


// let addBoard = function () {
//     let
// }