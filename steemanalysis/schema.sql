CREATE TABLE IF NOT EXISTS comments
(
    id             integer PRIMARY KEY,
    post_id        integer,
    post_author    text,
    post_title     text,
    comment_author text,
    comment_title  text,
    file_name      text,
    update_time    datetime NOT NULL default current_timestamp,
    create_time    datetime NOT NULL default current_timestamp
);
CREATE TABLE IF NOT EXISTS urls
(
    id          integer PRIMARY KEY,
    post_id     integer,
    comment_id  integer,
    other_id    integer,
    post_url    text UNIQUE,
    comment_url text UNIQUE,
    other_url   text,
    update_time datetime NOT NULL default current_timestamp,
    create_time datetime NOT NULL default current_timestamp,
    CONSTRAINT fk_column
        FOREIGN key (post_id)
            REFERENCES comments (id) ON DELETE CASCADE,
    FOREIGN key (comment_id)
        REFERENCES comments (id) ON DELETE CASCADE,
    FOREIGN key (other_id)
        REFERENCES comments (id)
        ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS responses
(
    id          integer PRIMARY KEY,
    url_id      integer  NOT NULL UNIQUE,
    response    json     NOT NULL,
    update_time datetime NOT NULL default current_timestamp,
    create_time datetime NOT NULL default current_timestamp,
    CONSTRAINT fk_column
        FOREIGN key (url_id)
            REFERENCES urls (id)
            ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS google_responses
(
    id          integer PRIMARY KEY,
    url_id      integer  NOT NULL UNIQUE,
    response    json     NOT NULL,
    update_time datetime NOT NULL default current_timestamp,
    create_time datetime NOT NULL default current_timestamp,
    CONSTRAINT fk_column
        FOREIGN key (url_id)
            REFERENCES urls (id)
            ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS ibm_responses
(
    id          integer PRIMARY KEY,
    url_id      integer  NOT NULL UNIQUE,
    response    json     NOT NULL,
    update_time datetime NOT NULL default current_timestamp,
    create_time datetime NOT NULL default current_timestamp,
    CONSTRAINT fk_column
        FOREIGN key (url_id)
            REFERENCES urls (id)
            ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS textblob_responses
(
    id          integer PRIMARY KEY,
    url_id      integer  NOT NULL UNIQUE,
    response    json     NOT NULL,
    update_time datetime NOT NULL default current_timestamp,
    create_time datetime NOT NULL default current_timestamp,
    CONSTRAINT fk_column
        FOREIGN key (url_id)
            REFERENCES urls (id)
            ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS flair_responses
(
    id          integer PRIMARY KEY,
    url_id      integer  NOT NULL UNIQUE,
    response    json     NOT NULL,
    update_time datetime NOT NULL default current_timestamp,
    create_time datetime NOT NULL default current_timestamp,
    CONSTRAINT fk_column
        FOREIGN key (url_id)
            REFERENCES urls (id)
            ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS value_earned
(
    id             integer PRIMARY KEY,
    url_id         integer  NOT NULL UNIQUE,
    value_earned   number   NOT NULL,
    extracted_text text     NOT NULL,
    update_time    datetime NOT NULL default current_timestamp,
    create_time    datetime NOT NULL default current_timestamp,
    CONSTRAINT fk_column
        FOREIGN key (url_id)
            REFERENCES urls (id)
            ON DELETE CASCADE
);
CREATE TRIGGER IF NOT EXISTS UPDATE_GOOGLE_RESPONSES_TRIGGER
    AFTER UPDATE
    ON google_responses
BEGIN
    UPDATE comments SET update_time = current_timestamp WHERE ID = old.rowid;
END;
CREATE TRIGGER IF NOT EXISTS UPDATE_IBM_RESPONSES_TRIGGER
    AFTER UPDATE
    ON ibm_responses
BEGIN
    UPDATE comments SET update_time = current_timestamp WHERE ID = old.rowid;
END;
CREATE TRIGGER IF NOT EXISTS UPDATE_TEXTBLOB_RESPONSES_TRIGGER
    AFTER UPDATE
    ON textblob_responses
BEGIN
    UPDATE comments SET update_time = current_timestamp WHERE ID = old.rowid;
END;
CREATE TRIGGER IF NOT EXISTS UPDATE_FLAIR_RESPONSES_TRIGGER
    AFTER UPDATE
    ON flair_responses
BEGIN
    UPDATE comments SET update_time = current_timestamp WHERE ID = old.rowid;
END;
CREATE TRIGGER IF NOT EXISTS UPDATE_COMMENTS_TRIGGER
    AFTER UPDATE
    ON comments
BEGIN
    UPDATE comments SET update_time = current_timestamp WHERE ID = old.rowid;
END;
CREATE TRIGGER IF NOT EXISTS UPDATE_URLS_TRIGGER
    AFTER UPDATE
    ON urls
BEGIN
    UPDATE comments SET update_time = current_timestamp WHERE ID = old.rowid;
END;
CREATE TRIGGER IF NOT EXISTS UPDATE_RESPONSES_TRIGGER
    AFTER UPDATE
    ON responses
BEGIN
    UPDATE comments SET update_time = current_timestamp WHERE ID = old.rowid;
END;
CREATE TRIGGER IF NOT EXISTS UPDATE_RESPONSES_TRIGGER
    AFTER UPDATE
    ON responses
BEGIN
    UPDATE comments SET update_time = current_timestamp WHERE ID = old.rowid;
END;