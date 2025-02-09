INSERT INTO e_vote.counties (id, code, name, created_at, created_by, updated_at, updated_by) VALUES 
('577b89d8-7318-5314-b5c1-1bca1d398acf','1','Mombasa', CURRENT_TIMESTAMP, NULL, CURRENT_TIMESTAMP, NULL);

INSERT INTO e_vote.constituencies (id, code, county_id, name, created_at, created_by, updated_by) VALUES 
('f7bfa687-f949-55e9-a692-3ef974dee8d2', '1', '577b89d8-7318-5314-b5c1-1bca1d398acf', 'Changamwe', CURRENT_TIMESTAMP, NULL, NULL);

INSERT INTO e_vote.wards (id, code, constituency_id, name, created_at, created_by, updated_by) VALUES 
('761ac5b3-2e74-547d-9e45-a6f07d2cc1c3', '1', 'f7bfa687-f949-55e9-a692-3ef974dee8d2', 'Airport', CURRENT_TIMESTAMP, NULL, NULL);

INSERT INTO e_vote.polling_stations (id, code, ward_id, name, created_at, created_by, updated_by) VALUES 
('31174a9a-3253-54af-9b92-e63ceef8bf13', '1', '761ac5b3-2e74-547d-9e45-a6f07d2cc1c3', 'Airport Primary School', CURRENT_TIMESTAMP, NULL, NULL);

INSERT INTO e_vote.voters (id, id_number, fingerprint_hash, first_name, last_name, other_name, phone, polling_station_id, created_at, created_by, updated_by) VALUES 
('f0fe10ca-4354-53df-b570-03980eb10b9e', '12345678', 'ad9a41a5-7c29-47e1-8584-3fa1da2c379c', 'DENNIS', 'MUGA', 'MUTETHIA', '254759697757', '31174a9a-3253-54af-9b92-e63ceef8bf13', CURRENT_TIMESTAMP, NULL, NULL),
('50298d17-4289-563b-a37c-29019ffbe682', '23456789', 'ad9a41a5-7c29-47e1-8584-3fa1da2c379c', 'WILLIAM', 'RUTO', 'SAMOE', '254712345678', '31174a9a-3253-54af-9b92-e63ceef8bf13', CURRENT_TIMESTAMP, NULL, NULL),
('713059af-3045-5a55-89b3-77daeb2f8fd8', '34567890', 'ad9a41a5-7c29-47e1-8584-3fa1da2c379c', 'KITHURE', 'KINDIKI', 'IBRAHIM', '254798765432', '31174a9a-3253-54af-9b92-e63ceef8bf13', CURRENT_TIMESTAMP, NULL, NULL);

INSERT INTO e_vote.candidates (id, voter_id, party_id, icon, running_mate_voter_id, running_mate_icon, election_id, unit) VALUES 
('beec3d26-03b9-566e-9102-b5951dd0814f', '50298d17-4289-563b-a37c-29019ffbe682', '3823fecc-fc95-5933-9abe-9a80e4e3be0c', 'ruto.jpg', '713059af-3045-5a55-89b3-77daeb2f8fd8', 'kindiki.jpg', 'f12b6364-bc63-57b2-9ab1-3c19d5973218', 'country' );
