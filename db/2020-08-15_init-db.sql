CREATE TABLE location (
    id SERIAL PRIMARY KEY,
    person_id INT NOT NULL,
    coordinate GEOMETRY NOT NULL,
    creation_time TIMESTAMP NOT NULL DEFAULT NOW(),
    FOREIGN KEY (person_id) REFERENCES person(id)
);
CREATE INDEX coordinate_idx ON location (coordinate);
CREATE INDEX creation_time_idx ON location (creation_time);
