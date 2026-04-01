-- id, name, network-relevant
INSERT INTO entity_types VALUES (0, 'Room', 0);
INSERT INTO entity_types VALUES (1, 'Cabinet', 0);
INSERT INTO entity_types VALUES (2, 'Server-rack', 0);
INSERT INTO entity_types VALUES (3, 'PC', 1);
INSERT INTO entity_types VALUES (4, 'Laptop', 1);
INSERT INTO entity_types VALUES (5, 'Server', 1);
INSERT INTO entity_types VALUES (6, 'SSD', 0);
INSERT INTO entity_types VALUES (7, 'HDD', 0);
INSERT INTO entity_types VALUES (8, 'CPU', 0);
INSERT INTO entity_types VALUES (9, 'DIMM', 0); -- Ram
INSERT INTO entity_types VALUES (10, 'Switch', 1);
INSERT INTO entity_types VALUES (11, 'Router', 1);
INSERT INTO entity_types VALUES (12, 'Phone', 1);
INSERT INTO entity_types VALUES (13, 'Dock', 0);
INSERT INTO entity_types VALUES (14, 'Virtual_Machine', 1);
INSERT INTO entity_types VALUES (15, 'Tablet', 1);
INSERT INTO entity_types VALUES (16, 'Monitor', 0);
INSERT INTO entity_types VALUES (17, 'GPU', 0);

-- Storage / Components
INSERT INTO entity_types VALUES (18, 'NIC', 1);
INSERT INTO entity_types VALUES (19, 'Mainboard', 0);
INSERT INTO entity_types VALUES (20, 'Power_Supply', 0);
INSERT INTO entity_types VALUES (21, 'Cooling_Fan', 0);
INSERT INTO entity_types VALUES (22, 'Heat_Sink', 0);
INSERT INTO entity_types VALUES (23, 'RAID_Controller', 1);
INSERT INTO entity_types VALUES (24, 'Battery', 0);
INSERT INTO entity_types VALUES (25, 'TPM_Module', 0);

-- Storage Devices
INSERT INTO entity_types VALUES (30, 'NAS', 1);
INSERT INTO entity_types VALUES (31, 'SAN', 1);
INSERT INTO entity_types VALUES (32, 'External_HDD', 0);
INSERT INTO entity_types VALUES (33, 'External_SSD', 0);
INSERT INTO entity_types VALUES (34, 'Tape_Drive', 0);
INSERT INTO entity_types VALUES (35, 'Tape_Library', 1);
INSERT INTO entity_types VALUES (36, 'USB_Stick', 0);
INSERT INTO entity_types VALUES (37, 'SD_Card', 0);

-- Network Equipment
INSERT INTO entity_types VALUES (40, 'Firewall', 1);
INSERT INTO entity_types VALUES (41, 'Access_Point', 1);
INSERT INTO entity_types VALUES (42, 'Load_Balancer', 1);
INSERT INTO entity_types VALUES (43, 'Network_Card', 1);
INSERT INTO entity_types VALUES (44, 'Patch_Panel', 0);
INSERT INTO entity_types VALUES (45, 'Network_Module', 0);
INSERT INTO entity_types VALUES (46, 'SFP_Module', 0);
INSERT INTO entity_types VALUES (47, 'Media_Converter', 1);

-- Infrastructure
INSERT INTO entity_types VALUES (60, 'UPS', 0);
INSERT INTO entity_types VALUES (61, 'PDU', 0);
INSERT INTO entity_types VALUES (62, 'Power_Distributor', 0);
INSERT INTO entity_types VALUES (63, 'Air_Conditioning', 0);
INSERT INTO entity_types VALUES (64, 'Cooling_Unit', 0);
INSERT INTO entity_types VALUES (65, 'Temperature_Sensor', 0);
INSERT INTO entity_types VALUES (66, 'Humidity_Sensor', 0);
INSERT INTO entity_types VALUES (67, 'Security_Camera', 1);

-- Office Hardware
INSERT INTO entity_types VALUES (80, 'Printer', 1);
INSERT INTO entity_types VALUES (81, 'Scanner', 0);
INSERT INTO entity_types VALUES (82, 'Plotter', 0);
INSERT INTO entity_types VALUES (83, 'Projector', 0);
INSERT INTO entity_types VALUES (84, 'Conference_System', 1);
INSERT INTO entity_types VALUES (85, 'Smart_Board', 1);

-- Peripherals
INSERT INTO entity_types VALUES (100, 'Keyboard', 0);
INSERT INTO entity_types VALUES (101, 'Mouse', 0);
INSERT INTO entity_types VALUES (102, 'Headset', 0);
INSERT INTO entity_types VALUES (103, 'Speakers', 0);
INSERT INTO entity_types VALUES (104, 'Webcam', 1);
INSERT INTO entity_types VALUES (105, 'Microphone', 0);
INSERT INTO entity_types VALUES (106, 'USB_Hub', 0);
INSERT INTO entity_types VALUES (107, 'Docking_Station', 0);

-- Mobile Devices
INSERT INTO entity_types VALUES (120, 'Smartphone', 1);
INSERT INTO entity_types VALUES (121, 'Smartwatch', 1);
INSERT INTO entity_types VALUES (122, 'Handheld_Scanner', 1);

-- Virtualization / Cloud
INSERT INTO entity_types VALUES (150, 'Hypervisor', 1);
INSERT INTO entity_types VALUES (151, 'Container_Host', 1);
INSERT INTO entity_types VALUES (152, 'Container', 1);
INSERT INTO entity_types VALUES (153, 'Kubernetes_Node', 1);
INSERT INTO entity_types VALUES (154, 'Virtual_Network', 1);
INSERT INTO entity_types VALUES (155, 'Virtual_Disk', 0);

-- Security Hardware
INSERT INTO entity_types VALUES (180, 'HSM', 1);
INSERT INTO entity_types VALUES (181, 'Smartcard_Reader', 0);
INSERT INTO entity_types VALUES (182, 'Biometric_Scanner', 0);
INSERT INTO entity_types VALUES (183, 'Door_Controller', 1);

-- Datacenter Structures
INSERT INTO entity_types VALUES (200, 'Datacenter', 0);
INSERT INTO entity_types VALUES (201, 'Building', 0);
INSERT INTO entity_types VALUES (202, 'Floor', 0);
INSERT INTO entity_types VALUES (203, 'Zone', 0);
INSERT INTO entity_types VALUES (204, 'Rack_Unit', 0);

-- Lab / Development Equipment
INSERT INTO entity_types VALUES (230, 'Raspberry_Pi', 1);
INSERT INTO entity_types VALUES (231, 'Development_Board', 1);
INSERT INTO entity_types VALUES (232, 'Logic_Analyzer', 0);
INSERT INTO entity_types VALUES (233, 'Oscilloscope', 0);

-- Backup Systems
INSERT INTO entity_types VALUES (260, 'Backup_Server', 1);
INSERT INTO entity_types VALUES (261, 'Backup_Appliance', 1);
INSERT INTO entity_types VALUES (262, 'Backup_Storage', 1);
