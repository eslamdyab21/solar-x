USE SolarX;

INSERT INTO Batteries  VALUES ('Battery 1',12, 1);
INSERT INTO Batteries  VALUES ('Battery 2',12, 1);
INSERT INTO Batteries  VALUES ('Battery 3',12, 1);

INSERT INTO Batteries_Reads VALUES ('1', 'Battery 1', 1024.54, 4012.36, 40, 'ideal', NOW());
INSERT INTO Batteries_Reads VALUES ('2', 'Battery 2', 0, 12000, 100, 'ideal', NOW());
INSERT INTO Batteries_Reads VALUES ('3', 'Battery 3', 2014.51, 9985.49, 80, 'discharging', NOW());
