CREATE TABLE e_vote.counties (
  id SERIAL PRIMARY KEY,
  name TEXT,
  created_at TIMESTAMP,
  created_by INT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by INT,
  UNIQUE (name)
);