USE SolarX;

INSERT INTO Batteries  VALUES (NULL, 'Battery 1',12, 1);
INSERT INTO Batteries  VALUES (NULL, 'Battery 2',12, 1);
INSERT INTO Batteries  VALUES (NULL, 'Battery 3',12, 1);

INSERT INTO Battery_readings VALUES (NULL, 1, 1024.54, 4012.36, 'ideal', NOW());
INSERT INTO Battery_readings VALUES (NULL, 2, 0, 12000, 'ideal', NOW());
INSERT INTO Battery_readings VALUES (NULL, 3, 2014.51, 9985.49, 'discharging', NOW());


INSERT INTO Solar_pannels VALUES (NULL, 'Roof Panel', 10);
INSERT INTO Solar_pannel_readings VALUES (NULL, 1, 50642.42, 3021.23, NOW(), NOW());



INSERT INTO Home VALUES (NULL, 'Family Home');
INSERT INTO Home_readings VALUES (NULL, 1, 50642.42, 3021.23, NOW(), NOW());