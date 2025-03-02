import mysql.connector
import os
from dotenv import load_dotenv
import colorlog
import logging
from twitchAPI.object.eventsub import ChannelSubscribeEvent, ChannelRaidEvent, ChannelFollowEvent,StreamOnlineEvent,StreamOfflineEvent,ChannelUpdateEvent, GoalEvent, ChannelPredictionEvent, ChannelPointsCustomRewardRedemptionUpdateEvent, ChannelPointsCustomRewardRedemptionAddEvent,ChannelPointsCustomRewardUpdateEvent,ChannelPointsCustomRewardRemoveEvent, ChannelPointsCustomRewardAddEvent, HypeTrainEvent, HypeTrainEndEvent, ChannelUnbanRequestResolveEvent,ChannelBanEvent,ChannelUnbanEvent, ChannelUnbanRequestCreateEvent, CharityCampaignProgressEvent, CharityCampaignStartEvent, CharityCampaignStopEvent, CharityDonationEvent, ChannelSubscriptionEndEvent, ChannelSubscriptionGiftEvent, ChannelSubscriptionMessageEvent, ChannelShoutoutCreateEvent, ChannelShoutoutReceiveEvent

class Twitch:

    def __init__(self):
        """
        opens connection to specific db
        """
        self.initLogger()
        self.setEnv()
        self.connect()
        
    def connect(self):
        """
        connects to db and creates an curser

        """
        self.conn = mysql.connector.connect(host      = self.host_,
                                          user      = self.user,
                                          password  = self.pw,
                                          database  = self.sdb
                                        )
        self.cursor = self.db.cursor()
    
    def close_connection(self):
        """
        close cursor and connection
        """
        self.cursor.close()
        self.conn.close()

    def initLogger(self):
        """
        inits the logger
        """
        handler = colorlog.StreamHandler()
        formatter = colorlog.ColoredFormatter(
            '%(asctime)s - %(log_color)s%(levelname)-8s%(reset)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'blue',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )

        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def setEnv(self):
        """
        sets variables..
        """
        self.host_   =   os.getenv("mysql_host")
        self.user   =   os.getenv("mysql_user")
        self.pw     =   os.getenv("mysql_password")
        self.sdb     =   os.getenv("mysql_database")

    def create_tables(self):
        """
        creates needed tables if they not exist
        """

        self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id             INT PRIMARY KEY,
                            username       VARCHAR(55),
                            displayname    VARCHAR(55), 
                            created_at     DATETIME ,
                            ismod          TINYINT(1),
                            isvip          TINYINT(1)


                        );
                        """)
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS eventtypes (
                            id          INT AUTO_INCREMENT PRIMARY KEY,
                            name        text,
                            subscribed  TINYINT(1),
                            cli         varchar(255)

                        );
                            """)
        

        self.cursor.execute("""
                                CREATE TABLE IF NOT EXISTS event (
                                    id              INT AUTO_INCREMENT PRIMARY KEY,
                                    event_type      VARCHAR(50) NOT NULL,
                                    sub_id          VARCHAR(255) NOT NULL,
                                    json_data       JSON NOT NULL, 
                                    timestamp       DATETIME NOT NULL
                                );
                            """)


        self.cursor.execute("""
                                CREATE TABLE IF NOT EXISTS event_streaminfo (
                                id                              INT AUTO_INCREMENT PRIMARY KEY,
                                event_id                        INT NOT NULL,
                                stream_id                       VARCHAR(255),
                                broadcaster_user_id             INT,
                                stream_type                     VARCHAR(255),
                                startet_at                      DATETIME, 
                                stream_language                 VARCHAR(55),
                                category_id                     INT, 
                                content_classification_labels   VARCHAR(255),
                                stream_title                    VARCHAR(255) NOT NULL,
                                FOREIGN KEY (broadcaster_user_id) REFERENCES users(id), 
                                FOREIGN KEY (event_id) REFERENCES event(id) ON DELETE CASCADE
                                );
                            """)
        
        self.cursor.execute("""
                                CREATE TABLE IF NOT EXISTS event_goals (
                                    id                      INT AUTO_INCREMENT PRIMARY KEY,
                                    event_id                INT NOT NULL,
                                    goal_id                 VARCHAR(255),
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
                            """)
        self.cursor.execute("""
                               CREATE TABLE IF NOT EXISTS event_polls (
                                    id                          INT AUTO_INCREMENT PRIMARY KEY,
                                    event_id                    INT NOT NULL,
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
                            """)
        self.cursor.execute("""
                                CREATE TABLE IF NOT EXISTS event_predictions (
                                    id                      INT AUTO_INCREMENT PRIMARY KEY,
                                    event_id                INT NOT NULL,
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
                            """)
        self.cursor.execute("""
                                CREATE TABLE IF NOT EXISTS event_channelpoints (
                                    id                                      INT AUTO_INCREMENT PRIMARY KEY,
                                    event_id                                INT NOT NULL,
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
                                );                         """)
        self.cursor.execute("""
                                CREATE TABLE IF NOT EXISTS event_hypetrain (
                                    id                          INT AUTO_INCREMENT PRIMARY KEY,
                                    event_id                    INT NOT NULL,
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
                         """)
        
        self.cursor.execute("""
                                CREATE TABLE IF NOT EXISTS event_shoutout (
                                    id                          INT AUTO_INCREMENT PRIMARY KEY,
                                    event_id                    INT NOT NULL,
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
        
                            """)
        
        self.cursor.execute(""" 
                            CREATE TABLE IF NOT EXISTS event_subscribe (
                                id                      INT AUTO_INCREMENT PRIMARY KEY,
                                event_id                INT NOT NULL,
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
                            """)    
        self.cursor.execute(""" 
                            CREATE TABLE IF NOT EXISTS event_follow (
                                id                      INT AUTO_INCREMENT PRIMARY KEY,
                                event_id                INT NOT NULL,
                                userid                 INT,  
                                broadcaster_user_id     INT,
                                followed_at             DATETIME NOT NULL,
                                FOREIGN KEY (broadcaster_user_id) REFERENCES users(id), 
                                FOREIGN KEY (userid) REFERENCES users(id), 
                                FOREIGN KEY (event_id) REFERENCES event(id) ON DELETE CASCADE
                                );
                            """)
      
        self.conn.commit()

    def streamonline_event(self, x: StreamOnlineEvent):
        """
        callback fkt for stream online

        receives the data from stream_online Event
        """
        
        self.cursor.execute(""" 
                            INSERT INTO event (
                                id
                                event_type,
                                sub_id,
                                json_data,
                                timestamp
                            ) VALUES (
                                %s,
                                %s,
                                %s,
                                %s,
                                NOW()
                            );
                            """,
                            (
                                x.event.id
                                x.subscription.type,
                                {x.event.type},

                                x.event.type,
                                x.subscription.id,  # Hier war der Fehler!
                                x.subscription.to_dict(),
                                x.event.type,
                                x.subscription.id,
                                x.subscription.to_dict()
                            ))
        self.cursor.execute("""
                            INSERT INTO event_streaminfo (
                                event_id,
                                stream_id,
                                broadcaster_user_id,
                                stream_type,
                                startet_at,
                                stream_language,
                                category_id,
                                content_classification_labels,
                                stream_title
                            ) VALUES (
                                (SELECT id FROM event WHERE sub_id = %s),
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s
                            );
                            """,
                            (
                                x.subscription.id,
                                x.event.id,
                                x.event.broadcaster_user_id,
                                x.event.type,
                                x.event.started_at,
                                x.event.language,
                                x.event.category_id,
                                x.event.content_classification_labels,
                                x.event.title
                            )
                        )
        self.conn.commit()
