INSERT INTO properties VALUES (0, 'storage_GB', 'float');
INSERT INTO properties VALUES (1, 'manufacturer', 'text');
INSERT INTO properties VALUES (2, 'cores', 'int');
INSERT INTO properties VALUES (3, 'ip_address', 'text');
INSERT INTO properties VALUES (4, 'mac_address', 'text');
INSERT INTO properties VALUES (5, 'manufacture_name', 'text');
INSERT INTO properties VALUES (6, 'friendly_name', 'text');
INSERT INTO properties VALUES (7, 'clock_speed_GHz', 'float');
INSERT INTO properties VALUES (8, 'read_speed_MB/s', 'float');
INSERT INTO properties VALUES (9, 'write_speed_MB/s', 'float');
INSERT INTO properties VALUES (10, 'USB-C_ports_count', 'int');
INSERT INTO properties VALUES (11, 'USB-A_ports_count', 'int');
INSERT INTO properties VALUES (12, 'HDMI_ports_count', 'int');
INSERT INTO properties VALUES (13, 'memory_GB', 'float');
INSERT INTO properties VALUES (14, 'operating_system', 'text');
INSERT INTO properties VALUES (15, 'file_system', 'text');

-- Hardware identification
INSERT INTO properties VALUES (16, 'serial_number', 'text');
INSERT INTO properties VALUES (17, 'model', 'text');
INSERT INTO properties VALUES (18, 'part_number', 'text');
INSERT INTO properties VALUES (19, 'asset_tag', 'text');
INSERT INTO properties VALUES (20, 'firmware_version', 'text');
INSERT INTO properties VALUES (21, 'bios_version', 'text');

-- CPU / processing
INSERT INTO properties VALUES (22, 'threads', 'int');
INSERT INTO properties VALUES (23, 'tdp_watts', 'float');
INSERT INTO properties VALUES (24, 'architecture', 'text');

-- GPU
INSERT INTO properties VALUES (25, 'vram_GB', 'float');
INSERT INTO properties VALUES (26, 'gpu_clock_MHz', 'float');

-- Memory
INSERT INTO properties VALUES (27, 'memory_type', 'text');
INSERT INTO properties VALUES (28, 'memory_speed_MHz', 'int');
INSERT INTO properties VALUES (29, 'memory_slots', 'int');

-- Storage
INSERT INTO properties VALUES (30, 'storage_type', 'text');
INSERT INTO properties VALUES (31, 'iops', 'int');
INSERT INTO properties VALUES (32, 'interface', 'text');
INSERT INTO properties VALUES (33, 'raid_level', 'text');

-- Networking
INSERT INTO properties VALUES (34, 'hostname', 'text');
INSERT INTO properties VALUES (35, 'subnet_mask', 'text');
INSERT INTO properties VALUES (36, 'gateway', 'text');
INSERT INTO properties VALUES (37, 'dns_server', 'text');
INSERT INTO properties VALUES (38, 'network_speed_Gbps', 'float');
INSERT INTO properties VALUES (39, 'wifi_supported', 'int');
INSERT INTO properties VALUES (40, 'bluetooth_supported', 'int');
INSERT INTO properties VALUES (41, 'network_ports', 'int');

-- Datacenter / rack
INSERT INTO properties VALUES (50, 'rack_units', 'int');
INSERT INTO properties VALUES (51, 'rack_position', 'int');
INSERT INTO properties VALUES (52, 'weight_kg', 'float');
INSERT INTO properties VALUES (53, 'depth_mm', 'int');
INSERT INTO properties VALUES (54, 'height_mm', 'int');
INSERT INTO properties VALUES (55, 'width_mm', 'int');

-- Power
INSERT INTO properties VALUES (60, 'power_watts', 'float');
INSERT INTO properties VALUES (61, 'power_supply_count', 'int');
INSERT INTO properties VALUES (62, 'voltage', 'float');
INSERT INTO properties VALUES (63, 'battery_capacity_mAh', 'int');
INSERT INTO properties VALUES (64, 'battery_cycles', 'int');

-- Cooling / environment
INSERT INTO properties VALUES (70, 'temperature_C', 'float');
INSERT INTO properties VALUES (71, 'humidity_percent', 'float');
INSERT INTO properties VALUES (72, 'fan_count', 'int');

-- Display devices
INSERT INTO properties VALUES (80, 'screen_size_inch', 'float');
INSERT INTO properties VALUES (81, 'resolution_x', 'int');
INSERT INTO properties VALUES (82, 'resolution_y', 'int');
INSERT INTO properties VALUES (83, 'refresh_rate_Hz', 'float');
INSERT INTO properties VALUES (84, 'panel_type', 'text');

-- Printer / office devices
INSERT INTO properties VALUES (90, 'print_speed_ppm', 'int');
INSERT INTO properties VALUES (91, 'color_supported', 'int');
INSERT INTO properties VALUES (92, 'duplex_supported', 'int');

-- Virtualization
INSERT INTO properties VALUES (100, 'hypervisor_type', 'text');
INSERT INTO properties VALUES (101, 'vm_count', 'int');
INSERT INTO properties VALUES (102, 'virtual_cpu', 'int');
INSERT INTO properties VALUES (103, 'virtual_memory_GB', 'float');
INSERT INTO properties VALUES (104, 'virtual_disk_GB', 'float');

-- Containers
INSERT INTO properties VALUES (110, 'container_runtime', 'text');
INSERT INTO properties VALUES (111, 'container_count', 'int');

-- Operating system details
INSERT INTO properties VALUES (120, 'kernel_version', 'text');
INSERT INTO properties VALUES (121, 'os_version', 'text');
INSERT INTO properties VALUES (122, 'uptime_seconds', 'int');

-- Backup / storage infrastructure
INSERT INTO properties VALUES (130, 'backup_schedule', 'text');
INSERT INTO properties VALUES (131, 'backup_retention_days', 'int');

-- Security hardware
INSERT INTO properties VALUES (140, 'encryption_supported', 'int');
INSERT INTO properties VALUES (141, 'tpm_version', 'text');
INSERT INTO properties VALUES (142, 'secure_boot_enabled', 'int');

-- Sensors
INSERT INTO properties VALUES (150, 'sensor_type', 'text');
INSERT INTO properties VALUES (151, 'measurement_unit', 'text');
INSERT INTO properties VALUES (152, 'measurement_range', 'text');

-- Cameras
INSERT INTO properties VALUES (160, 'camera_resolution_MP', 'float');
INSERT INTO properties VALUES (161, 'night_vision_supported', 'int');

-- Development boards
INSERT INTO properties VALUES (170, 'gpio_pins', 'int');
INSERT INTO properties VALUES (171, 'soc_model', 'text');

-- Mobile devices
INSERT INTO properties VALUES (180, 'imei', 'text');
INSERT INTO properties VALUES (181, 'sim_slots', 'int');
INSERT INTO properties VALUES (182, 'cellular_supported', 'int');
