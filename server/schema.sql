CREATE TABLE IF NOT EXISTS weather (
  timestamp TIMESTAMP NOT NULL PRIMARY KEY,
  wind_speed REAL NOT NULL,
  temperature REAL NOT NULL,
  gas REAL NOT NULL,
  relative_humidity REAL NOT NULL,
  pressure REAL NOT NULL
);
