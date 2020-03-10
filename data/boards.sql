CREATE TABLE IF NOT EXISTS board(
    id serial NOT NULL primary key ,
    title text
);

INSERT INTO board (title) VALUES ('Board 1');
INSERT INTO board (title) VALUES ('Board 2');

CREATE TABLE IF NOT EXISTS cards (
    id serial NOT NULL primary key ,
    board_id integer,
    title text,
    status_id integer,
    order boolean

);

ALTER TABLE cards
    ADD CONSTRAINT fk_board_id_cards
        foreign key (board_id) references board (id) on delete cascade,
    ADD CONSTRAINT fk_status_id_cards
        foreign key (status_id) references statuses(id) on delete cascade;

INSERT INTO cards (board_id, title, status_id, "order")
VALUES (1, 'new card 1', 0, 0);

INSERT INTO cards (board_id, title, status_id, "order")
VALUES (1, 'new card 2', 0, 1);

INSERT INTO cards (board_id, title, status_id, "order")
VALUES (1, 'in progress card', 1, 0);

INSERT INTO cards (board_id, title, status_id, "order")
VALUES (1, 'planning', 2, 0);

INSERT INTO cards (board_id, title, status_id, "order")
VALUES (1, 'done card 1', 3, 0);

INSERT INTO cards (board_id, title, status_id, "order")
VALUES (1, 'done card 1', 3, 1);

INSERT INTO cards (board_id, title, status_id, "order")
VALUES (2, 'new card 1', 0, 0);

INSERT INTO cards (board_id, title, status_id, "order")
VALUES (2, 'new card 2', 0, 1);

INSERT INTO cards (board_id, title, status_id, "order")
VALUES (2, 'in progress card', 1, 0);

INSERT INTO cards (board_id, title, status_id, "order")
VALUES (2, 'planning', 2, 0);

INSERT INTO cards (board_id, title, status_id, "order")
VALUES (2, 'done card 1', 3, 0);

INSERT INTO cards (board_id, title, status_id, "order")
VALUES (2, 'done card 1', 3, 1);


CREATE TABLE IF NOT EXISTS statuses (
    id serial NOT NULL primary key,
    title text
);

INSERT INTO statuses (title) VALUES ('new');

INSERT INTO statuses (title) VALUES ('in progress');

INSERT INTO statuses (title) VALUES ('testing');

INSERT INTO statuses (title) VALUES ('done');
