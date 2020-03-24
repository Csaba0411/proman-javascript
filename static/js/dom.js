// It uses data_handler.js to visualize elements
import {dataHandler} from "./data_handler.js";

export let dom = {
    init: function () {
        // This function should run once, when the page is loaded.
    },
    loadBoards: function () {
        document.querySelector('#boards').textContent = '';
        // retrieves boards and makes showBoards called
        document.querySelector('#boards').textContent = '';
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
                <div class="board-header"><button class="board-title" data-board-id="${board['id']}">${board.title}</button>
                <button class="board-add add-card" data-board-id="${board['id']}">Add Card</button>
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
        addBoard();
        renameFunction();
        hideShowColumn();
        addColumn();
        deleteBoard();
        addCard();
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
    for (let boardName of rename) {
        boardName.addEventListener('dblclick', function (event) {
            let newBoardName = prompt('New board name:');
            renameBoardApi(newBoardName, boardName.dataset.boardId, boardName, changeTextContent);
            event.preventDefault();
        })
    }

    function renameBoardApi(newBoardName, boardId, boardName, callback) {
        fetch(`/rename-board/${boardId}/${newBoardName}`)
            .then(response => response.json())
            .then(data => callback(data, boardName))
    }

    function changeTextContent(data, boardName) {
        boardName.textContent = data;
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
            let board = button.dataset.boardId;
            apiFetch(board, name, dom.loadBoards);
            e.preventDefault()
        })
    }

    function apiFetch(board, name, callback) {
        fetch(`/new-status/${board}/${name}`)
            .then(response => response)
            .then(data => callback(data))
    }
};


let deleteBoard = function () {
    let deleteButtonsForBoard = document.querySelectorAll('.board-delete');
    for (let button of deleteButtonsForBoard) {
        button.addEventListener('click', function (event) {
            let boardId = button.dataset.boardId;
            sendDataAPI(boardId, dom.loadBoards);
            event.preventDefault()
        })
    }

    function sendDataAPI(data, callback) {
        fetch(`/delete/${data}`)
            .then(response => response)
            .then(data => callback(data))
    }
};


function addCard() {
    let addCardButtons = document.getElementsByClassName("add-card");
    for (let addButton of addCardButtons) {
        addButton.addEventListener('click', function (event) {
            let boardId = addButton.dataset.boardId;
            NewCardInsertApi(boardId, addButton, addNewCardHTML);
            event.preventDefault();
        })
    }

    function NewCardInsertApi(boardId, addButton, callback) {

        fetch(`/save-new-card/${boardId}`)
            .then(response => response.json())
            .then(data => callback(data, addButton))
    }

    function addNewCardHTML(data, addButton) {
        let boardId = addButton.dataset.boardId;
        let allCardContainer = document.getElementsByClassName('column-for-new-cards');
        let newCard =
            `<div class="card">
                    <div class="card-remove"><i class="fas fa-trash-alt"></i></div>
                    <div class="card-title">New Card</div>
                </div>`;
        for (let cardContainer of allCardContainer) {
            if (cardContainer.dataset.boardId === boardId) {
                cardContainer.insertAdjacentHTML("beforeend", newCard)
            }
        }
    }
}

function addBoard() {
    let plusSign = document.querySelector('#plus-sign');
    plusSign.addEventListener('click', function () {
        let newBoardName = prompt('Board name: ');
        addBoardApi(newBoardName, insertNewBoard)
    });

    function addBoardApi(boardName, callback) {
        fetch(`/save-new-board/${boardName}`)
            .then(promise => promise.json())
            .then(data => callback(data, boardName))
    }

    function insertNewBoard(data, newBoardName) {
        let boardContainer = document.querySelector('.board-container');
        let board = `
                <section class="board">
                <div class="board-header"><button class="board-title" data-board-id="${data}">${newBoardName}</button>
                    <button class="board-add add-card" data-board-id="${data}">Add Card</button>
                    <button class="board-add add-status" data-board-id="${data}">Add status</button>
                    <button class="board-toggle"><i class="fas fa-chevron-down toggle-button"></i></button>
                    <div class="board-toggle"><i class="fas fa-trash-alt board-delete" data-board-id="${data}"></i></div>
                </div>
                <div class="board-columns">`;
        for (let stats of ['new', 'in progress', 'testing', 'done']) {
            if (stats === 'new') {
                board += `<div class="board-column column-for-new-cards" data-board-id="${data}">`
            } else {
                board += `<div class="board-column" data-board-id="${data}">`
            }
            board += `<div class="board-column-title">${stats}</div>
                        <div class="board-column-content">
                            <div class="card">
                            <div class="card-remove"><i class="fas fa-trash-alt"></i></div>
                            <div class="card-title">New card</div>
        </div>
        </div>
        </div>`
        }
        board += `</div>
                   </section>`;
    boardContainer.insertAdjacentHTML("beforeend",board)
    }
}
console.log('Hello');