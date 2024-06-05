-- Your SQL goes here

CREATE TABLE rules (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT NOT NULL
);

CREATE TABLE vulnerabilities (
  id SERIAL PRIMARY KEY,
  rule_id INTEGER NOT NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  severity VARCHAR NOT NULL,
  FOREIGN KEY (rule_id) REFERENCES rules(id)
);

