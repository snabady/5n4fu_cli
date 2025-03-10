-- Active: 1741211436712@@127.0.0.1@3306@twitch
CREATE TABLE IF NOT EXISTS users (
    id             INT PRIMARY KEY,
    username       VARCHAR(55),
    displayname    VARCHAR(55), 
    created_at     DATETIME ,
    ismod          TINYINT(1),
    isvip          TINYINT(1)


);

CREATE TABLE IF NOT EXISTS eventtypes (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        text,
    subscribed  TINYINT(1),
    cli         varchar(255)

);

CREATE TABLE IF NOT EXISTS event (

    id              VARCHAR(50) NOT NULL PRIMARY KEY,
    event_type      INT,
    sub_id          VARCHAR(255) NOT NULL,
    json_data       JSON NOT NULL, 
    timestamp       DATETIME NOT NULL,
    FOREIGN KEY (event_type) REFERENCES eventtypes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS event_streaminfo (
    id                              INT AUTO_INCREMENT PRIMARY KEY,
    event_id                        VARCHAR(50) NOT NULL,
    stream_id                       VARCHAR(255),
    broadcaster_user_id             INT NOT NULL,
    stream_type                     VARCHAR(255),
    started_at                      DATETIME, 
    stream_language                 VARCHAR(55),
    category_id                     INT, 
    content_classification_labels   TEXT,  -- Using TEXT for flexibility
    stream_title                    VARCHAR(255) NOT NULL,

    FOREIGN KEY (broadcaster_user_id) REFERENCES users(id) ON DELETE CASCADE, 
    FOREIGN KEY (event_id) REFERENCES event(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS event_goals (
    id                      INT AUTO_INCREMENT PRIMARY KEY,
    event_id                VARCHAR(50) NOT NULL,
    goal_id                 VARCHAR(255) NOT NULL,
    broadcaster_user_id     INT,
    goal_type               VARCHAR(255) NOT NULL,
    goal_description        TEXT,
    current_amount          INT,
    target_amount           INT,
    is_achieved             TINYINT(1),
    started_at              DATETIME,
    ended_at                DATETIME,

    FOREIGN KEY (broadcaster_user_id) REFERENCES users(id), 
    FOREIGN KEY (event_id) REFERENCES event(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS event_polls (
    id                          INT AUTO_INCREMENT PRIMARY KEY,
    event_id                    VARCHAR(255) NOT NULL,
    goal_id                     VARCHAR(255),
    broadcaster_user_id         INT, 
    poll_title                  TEXT, 
    poll_choices                JSON,  
    bits_voting                 JSON,  
    channel_points_voting       JSON, 
    started_at                  DATETIME, 
    ends_at                     DATETIME,
    poll_status                 VARCHAR(255), -- Hier war der Fehler!

    FOREIGN KEY (broadcaster_user_id) REFERENCES users(id), 
    FOREIGN KEY (event_id) REFERENCES event(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS event_predictions (
    id                      INT AUTO_INCREMENT PRIMARY KEY,
    event_id                VARCHAR(255) NOT NULL,
    prediction_id           VARCHAR(55),
    broadcaster_user_id     INT,
    prediction_status       VARCHAR(55),  -- Hier fehlte ein Komma!
    title                   TEXT,
    outcomes                JSON, 
    winning_outcome_id      INT,
    started_at              DATETIME,
    locks_at                DATETIME,
    prediction_question     TEXT NOT NULL,
    total_points            INT NOT NULL,

    FOREIGN KEY (event_id) REFERENCES event(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS event_channelpoints (
    id                                      INT AUTO_INCREMENT PRIMARY KEY,
    event_id                                VARCHAR(255) NOT NULL,
    channelpoints_id                        INT,
    is_enabled                              TINYINT(1),
    is_paused                               TINYINT(1),
    is_in_stock                             TINYINT(1),
    title                                   TEXT,
    cost                                    INT,
    prompt                                  TEXT,
    is_user_input_required                  TINYINT(1),
    shoud_redemptions_skip_request_queue    TINYINT(1),
    cooldown_expires_at                     DATETIME,
    max_per_stream                          JSON,
    max_per_user_per_stream                 JSON,
    global_cooldown                         JSON,
    background_color                        VARCHAR(10),
    channelpoints_image                     JSON,
    channelpoints_default_image             JSON,
    broadcaster_user_id                     INT,
    userid                                  INT,
    reward                                  JSON,
    channelpoints_message                   JSON,
    user_input                              TEXT,
    redeemed_at                             DATETIME,

    FOREIGN KEY (broadcaster_user_id) REFERENCES users(id), 
    FOREIGN KEY (userid) REFERENCES users(id), 
    FOREIGN KEY (event_id) REFERENCES event(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS event_hypetrain (
    id                          INT AUTO_INCREMENT PRIMARY KEY,
    event_id                    VARCHAR(255) NOT NULL,
    hypetrain_id                INT,
    broadcaster_user_id          INT,
    userid                      INT,  -- Fehlte in deiner Version!
    startet_at                  DATETIME,
    expires_at                  DATETIME,
    ended_at                    DATETIME,
    cooldown_ends_at            DATETIME,
    goal_target                 INT,
    top_contributors            JSON,
    last_contribution           JSON,
    hypetrain_level             INT,
    is_golden_kappa_train       TINYINT(1),
    hype_level                  INT NOT NULL,
    hype_total                  INT,
    hype_progress               INT,
    total_contributions         INT NOT NULL,

    FOREIGN KEY (broadcaster_user_id) REFERENCES users(id), 
    FOREIGN KEY (userid) REFERENCES users(id), 
    FOREIGN KEY (event_id) REFERENCES event(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS event_shoutout (
    id                          INT AUTO_INCREMENT PRIMARY KEY,
    event_id                    VARCHAR(255) NOT NULL,
    broadcaster_user_id          INT,
    moderator_user_id            INT,
    from_broadcaster_user_id     INT,
    to_broadcaster_user_id       INT,
    startet_at                  DATETIME, -- Fehlte ein Komma!
    viewer_count                INT,
    cooldown_ends_at            DATETIME,
    target_cooldown_ends_at     DATETIME,

    FOREIGN KEY (broadcaster_user_id) REFERENCES users(id), 
    FOREIGN KEY (from_broadcaster_user_id) REFERENCES users(id), 
    FOREIGN KEY (moderator_user_id) REFERENCES users(id), 
    FOREIGN KEY (event_id) REFERENCES event(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS event_subscribe (
    id                      INT AUTO_INCREMENT PRIMARY KEY,
    event_id                VARCHAR(255) NOT NULL,
    userid                  INT,
    broadcaster_user_id     INT,
    tier                    INT,
    is_gift                 TINYINT(1),
    total                   INT,
    cumulative_total        INT,
    is_anonymous            TINYINT(1),
    sub_message             JSON, 
    cumulative_month        INT,
    streak_month            INT, 
    duration_month          INT,
    FOREIGN KEY (broadcaster_user_id) REFERENCES users(id), 
    FOREIGN KEY (userid) REFERENCES users(id), 
    FOREIGN KEY (event_id) REFERENCES event(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS event_follow (
    id                      INT AUTO_INCREMENT PRIMARY KEY,
    event_id                VARCHAR(255) NOT NULL,
    userid                 INT,  
    broadcaster_user_id     INT,
    followed_at             DATETIME NOT NULL,
    FOREIGN KEY (broadcaster_user_id) REFERENCES users(id), 
    FOREIGN KEY (userid) REFERENCES users(id), 
    FOREIGN KEY (event_id) REFERENCES event(id) ON DELETE CASCADE
);

