-- add PC-one ('Omega')
INSERT INTO entities (id, type_id, serial, name) VALUES ('003-000000', 3, 0, 'Omega');
-- assign properties
INSERT INTO entity_properties VALUES ('003-000000', 1, 'HP');
INSERT INTO entity_properties VALUES ('003-000000', 0, '512');
INSERT INTO entity_properties VALUES ('003-000000', 2, '12');
INSERT INTO entity_properties VALUES ('003-000000', 14, 'NixOS');
INSERT INTO entity_properties VALUES ('003-000000', 5, 'ULTRA-nice-PC');

-- add PC-two ('Bravo')
INSERT INTO entities (id, type_id, serial, name) VALUES ('003-000001', 3, 1, 'Bravo');
-- assign properties
INSERT INTO entity_properties VALUES ('003-000001', 1, 'Apple');
INSERT INTO entity_properties VALUES ('003-000001', 0, '1024');
INSERT INTO entity_properties VALUES ('003-000001', 2, '10');
INSERT INTO entity_properties VALUES ('003-000001', 14, 'MacOS-X');
INSERT INTO entity_properties VALUES ('003-000001', 5, 'Mac-Book-Pro');



-- add SSD-one ('Omega's-ssd')
INSERT INTO entities (id, type_id, serial, name) VALUES ('006-000000', 6, 0, 'Omega-SSD');
-- assign properties
INSERT INTO entity_properties VALUES ('006-000000', 1, 'Samsung');
INSERT INTO entity_properties VALUES ('006-000000', 0, '512');
INSERT INTO entity_properties VALUES ('006-000000', 15, 'btrfs');
INSERT INTO entity_properties VALUES ('006-000000', 8, '7450');
INSERT INTO entity_properties VALUES ('006-000000', 9, '6900');

-- add SSD-two ('Bravo's-ssd')
INSERT INTO entities (id, type_id, serial, name) VALUES ('006-000001', 6, 1, 'Bravo-SSD');
-- assign properties
INSERT INTO entity_properties VALUES ('006-000001', 1, 'Kingston');
INSERT INTO entity_properties VALUES ('006-000001', 0, '1024');
INSERT INTO entity_properties VALUES ('006-000001', 15, 'APFS');
INSERT INTO entity_properties VALUES ('006-000001', 8, '6000');
INSERT INTO entity_properties VALUES ('006-000001', 9, '4000');



-- add containment
INSERT INTO containment VALUES ('003-000000', '006-000000', '1');
INSERT INTO containment VALUES ('003-000001', '006-000001', '1');
