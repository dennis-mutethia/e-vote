DROP TABLE IF EXISTS e_vote.counties;
CREATE TABLE e_vote.counties (
  id TEXT PRIMARY KEY,
  code TEXT,
  name TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT,
  UNIQUE (name)
);

DROP TABLE IF EXISTS e_vote.constituencies;
CREATE TABLE e_vote.constituencies (
  id TEXT PRIMARY KEY,
  code TEXT,
  county_id TEXT,
  name TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT,
  UNIQUE (name)
);

DROP TABLE IF EXISTS e_vote.wards;
CREATE TABLE e_vote.wards (
  id TEXT PRIMARY KEY,
  code TEXT,
  constituency_id TEXT,
  name TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT,
  UNIQUE (name)
);

DROP TABLE IF EXISTS e_vote.polling_stations; 
CREATE TABLE e_vote.polling_stations (
  id TEXT PRIMARY KEY,
  code TEXT,
  ward_id TEXT,
  name TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT,
  UNIQUE (name)
);

DROP TABLE IF EXISTS e_vote.voters;
CREATE TABLE e_vote.voters (
  id TEXT PRIMARY KEY,
  id_number TEXT,
  fingerprint_hash TEXT,
  first_name TEXT,
  last_name TEXT,
  other_name TEXT,
  phone TEXT,
  polling_station_id TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT,
  UNIQUE (id_number)
);

DROP TABLE IF EXISTS e_vote.sms_codes; 
CREATE TABLE e_vote.sms_codes (
  id TEXT PRIMARY KEY,
  voter_id TEXT,
  code TEXT,
  status INT DEFAULT 0,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT
);

DROP TABLE IF EXISTS e_vote.elections; 
CREATE TABLE e_vote.elections (
  id TEXT PRIMARY KEY,
  code TEXT,
  name TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT,
  UNIQUE (name)
);
