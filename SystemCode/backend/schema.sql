
CREATE TABLE IF NOT EXISTS adopter (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    adopter_name VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    accomodation INTEGER,
    prefer_age_group INTEGER,
    prefer_gender INTEGER,
    personality_preference TEXT,
    recommend_dog_index VARCHAR(255),
    boring_tags VARCHAR(255)
);