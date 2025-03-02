INT           INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
TINYINT       TINYINT(1) NOT NULL DEFAULT 0,
SMALLINT      SMALLINT NOT NULL,
MEDIUMINT     MEDIUMINT NOT NULL,
BIGINT        BIGINT NOT NULL,
DECIMAL       DECIMAL(10,2) NOT NULL,   -- 10 Stellen, 2 Nachkommastellen
FLOAT         FLOAT(10,2) NOT NULL,     -- Gleitkommazahl (weniger genau)
DOUBLE        DOUBLE(16,4) NOT NULL     -- Mehr Präzision als FLOAT


CHAR(10)      CHAR(10) NOT NULL,        -- Feste Länge 10 Zeichen
VARCHAR(255)  VARCHAR(255) NOT NULL,    -- Variable Länge bis 255 Zeichen
TEXT          TEXT NOT NULL,            -- Bis zu 64 KB Text
TINYTEXT      TINYTEXT NOT NULL,        -- Bis zu 255 Zeichen
MEDIUMTEXT    MEDIUMTEXT NOT NULL,      -- Bis zu 16 MB Text
LONGTEXT      LONGTEXT NOT NULL         -- Bis zu 4 GB Text

DATE          DATE NOT NULL,            -- YYYY-MM-DD
DATETIME      DATETIME NOT NULL,        -- YYYY-MM-DD HH:MM:SS
TIMESTAMP     TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Automatische Zeitstempel
TIME          TIME NOT NULL,            -- HH:MM:SS
YEAR          YEAR NOT NULL             -- 4-stellige Jahreszahl (z. B. 2024)

JSON          JSON NOT NULL,             -- JSON-Daten speichern
BLOB          BLOB NOT NULL,             -- Binärdaten (Bilder, Dateien)
TINYBLOB      TINYBLOB NOT NULL,         -- Kleine Binärdaten (255 Bytes)
MEDIUMBLOB    MEDIUMBLOB NOT NULL,       -- Mittlere Binärdaten (16 MB)
LONGBLOB      LONGBLOB NOT NULL          -- Große Binärdaten (4 GB)


git init
git add .
git commit -m "text"
git remote add origin "htt...git"
git branch -M main
git push -origin main
