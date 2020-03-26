ALTER TABLE IF EXISTS ONLY public.cards
    DROP CONSTRAINT IF EXISTS pk_cards_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.cards
    DROP CONSTRAINT IF EXISTS fk_status_id_cards CASCADE;
ALTER TABLE IF EXISTS ONLY public.cards
    DROP CONSTRAINT IF EXISTS fk_board_id_cards CASCADE;
ALTER TABLE IF EXISTS ONLY public.board
    DROP CONSTRAINT IF EXISTS pk_board_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.statuses
    DROP CONSTRAINT IF EXISTS pk_statuses_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.users
    DROP CONSTRAINT IF EXISTS pk_users_id CASCADE;


DROP TABLE IF EXISTS public.board;
CREATE TABLE board
(
    id      serial NOT NULL,
    title   text,
    user_id integer
);

DROP TABLE IF EXISTS public.cards;
CREATE TABLE cards
(
    id        serial NOT NULL,
    board_id  integer,
    title     text,
    status_id integer,
    "order"   integer,
    user_id   integer,
    status_order integer
);

DROP TABLE IF EXISTS public.statuses;
CREATE TABLE statuses
(
    id serial NOT NULL,
    title text
);

DROP TABLE IF EXISTS public.users;
CREATE TABLE users
(
    id       serial,
    name     text,
    password text,
    registration_date timestamp without time zone
);

ALTER TABLE ONLY users
    ADD CONSTRAINT pk_users_id PRIMARY KEY (id);

ALTER TABLE ONLY board
    ADD CONSTRAINT pk_board_id PRIMARY KEY (id),
    ADD CONSTRAINT pk_users_id
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE;

ALTER TABLE ONLY statuses
    ADD CONSTRAINT pk_statuses_id PRIMARY KEY (id);

ALTER TABLE cards
    ADD CONSTRAINT pk_cards_id PRIMARY KEY (id),
    ADD CONSTRAINT pk_board_id
        foreign key (board_id) references board (id) on delete cascade,
    ADD CONSTRAINT pk_statuses_id
        foreign key (status_id) references statuses (id) on delete cascade,
    ADD CONSTRAINT pk_users_id
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE;

INSERT INTO board (title)
VALUES ('Board 1');
INSERT INTO board (title)
VALUES ('Board 2');

INSERT INTO statuses (title)
VALUES ('new');
INSERT INTO statuses (title)
VALUES ('in progress');
INSERT INTO statuses (title)
VALUES ('testing');
INSERT INTO statuses (title)
VALUES ('done');

INSERT INTO cards (board_id, title, status_id, "order", status_order)
VALUES (1, 'new card 1', 1, 0, 0);
INSERT INTO cards (board_id, title, status_id, "order", status_order)
VALUES (1, 'new card 2', 1, 1, 0);
INSERT INTO cards (board_id, title, status_id, "order", status_order)
VALUES (1, 'in progress card', 2, 0, 1);
INSERT INTO cards (board_id, title, status_id, "order", status_order)
VALUES (1, 'planning', 3, 0, 2);
INSERT INTO cards (board_id, title, status_id, "order", status_order)
VALUES (1, 'done card 1', 4, 0, 3);
INSERT INTO cards (board_id, title, status_id, "order", status_order)
VALUES (1, 'done card 1', 4, 1, 3);
INSERT INTO cards (board_id, title, status_id, "order", status_order)
VALUES (2, 'new card 1', 1, 0, 0);
INSERT INTO cards (board_id, title, status_id, "order", status_order)
VALUES (2, 'new card 2', 1, 1, 0);
INSERT INTO cards (board_id, title, status_id, "order", status_order)
VALUES (2, 'in progress card', 2, 0, 1);
INSERT INTO cards (board_id, title, status_id, "order", status_order)
VALUES (2, 'planning', 3, 0, 2);
INSERT INTO cards (board_id, title, status_id, "order", status_order)
VALUES (2, 'done card 1', 4, 0, 3);
INSERT INTO cards (board_id, title, status_id, "order", status_order)
VALUES (2, 'done card 1', 4, 1, 3);

