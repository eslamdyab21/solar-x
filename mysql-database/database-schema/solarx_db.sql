
CREATE DATABASE SolarX;

USE SolarX;

CREATE TABLE Batteries(
    id INT AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
	capacity_kwh  FLOAT NOT NULL,
    charge_max_speed_watt_second FLOAT NOT NULL,

    PRIMARY KEY (id),
    CHECK(capacity_kwh > 0)
);


CREATE TABLE Batteries_Reads(
	id INT AUTO_INCREMENT,
    battery INT,
    current_hourly_consumption_watt FLOAT NOT NULL,
	current_energy_watt FLOAT NOT NULL,
    current_precentage INT NOT NULL,
    status VARCHAR(30),
    time_stamp TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (id),
    FOREIGN KEY (battery) REFERENCES Batteries(id),

    CHECK(current_hourly_consumption_watt >= 0),
    CHECK(current_energy_watt > 0),

    CHECK (current_precentage BETWEEN 0 AND 100),
    CHECK (status IN ('ideal', 'charging', 'discharging'))
);
