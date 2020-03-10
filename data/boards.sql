ALTER TABLE IF EXISTS ONLY public.cards DROP CONSTRAINT IF EXISTS pk_cards_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.cards DROP CONSTRAINT IF EXISTS fk_status_id_cards CASCADE;
ALTER TABLE IF EXISTS ONLY public.cards DROP CONSTRAINT IF EXISTS fk_board_id_cards CASCADE;
ALTER TABLE IF EXISTS ONLY public.board DROP CONSTRAINT IF EXISTS pk_board_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.statuses DROP CONSTRAINT IF EXISTS pk_statuses_id CASCADE;

DROP TABLE IF EXISTS public.board;
CREATE TABLE board(
    id serial NOT NULL,
    title text
);

DROP TABLE IF EXISTS public.cards;
CREATE TABLE cards (
    id serial NOT NULL,
    board_id integer,
    title text,
    status_id integer,
    "order" boolean
);

DROP TABLE IF EXISTS public.statuses;
CREATE TABLE statuses (
    id serial,
    title text
);
ALTER TABLE ONLY board
    ADD CONSTRAINT pk_board_id PRIMARY KEY (id);

ALTER TABLE ONLY statuses
    ADD CONSTRAINT pk_statuses_id PRIMARY KEY (id);

ALTER TABLE cards
    ADD CONSTRAINT pk_cards_id PRIMARY KEY (id),
    ADD CONSTRAINT pk_board_id
        foreign key (board_id) references board (id) on delete cascade,
    ADD CONSTRAINT pk_statuses_id
        foreign key (status_id) references statuses(id) on delete cascade;

INSERT INTO board (title) VALUES ('Board 1');
INSERT INTO board (title) VALUES ('Board 2');
INSERT INTO statuses (id, title) VALUES (0, 'new');
INSERT INTO statuses (id, title) VALUES (1, 'in progress');
INSERT INTO statuses (id, title) VALUES (2, 'testing');
INSERT INTO statuses (id, title) VALUES (3, 'done');
INSERT INTO cards (board_id, title, status_id, "order")
VALUES (1, 'new card 1', 0, false);
INSERT INTO cards (board_id, title, status_id, "order")
VALUES (1, 'new card 2', 0, true);
INSERT INTO cards (board_id, title, status_id, "order")
VALUES (1, 'in progress card', 1, false);
INSERT INTO cards (board_id, title, status_id, "order")
VALUES (1, 'planning', 2, false);
INSERT INTO cards (board_id, title, status_id, "order")
VALUES (1, 'done card 1', 3, false);
INSERT INTO cards (board_id, title, status_id, "order")
VALUES (1, 'done card 1', 3, true);
INSERT INTO cards (board_id, title, status_id, "order")
VALUES (2, 'new card 1', 0, false);
INSERT INTO cards (board_id, title, status_id, "order")
VALUES (2, 'new card 2', 0, true);
INSERT INTO cards (board_id, title, status_id, "order")
VALUES (2, 'in progress card', 1, false);
INSERT INTO cards (board_id, title, status_id, "order")
VALUES (2, 'planning', 2, false);
INSERT INTO cards (board_id, title, status_id, "order")
VALUES (2, 'done card 1', 3, false);
INSERT INTO cards (board_id, title, status_id, "order")
VALUES (2, 'done card 1', 3, true);
