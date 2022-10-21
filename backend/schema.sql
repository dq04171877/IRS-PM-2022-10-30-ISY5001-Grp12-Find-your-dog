
CREATE TABLE IF NOT EXISTS adopter (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    adopter_name NOT NULL UNIQUE,
    password NOT NULL,
    accomodation INTEGER,
    prefer_age_group INTEGER,
    prefer_gender INTEGER,
    personality_preference TEXT,
    recommend_dog_index VARCHAR(255)
);