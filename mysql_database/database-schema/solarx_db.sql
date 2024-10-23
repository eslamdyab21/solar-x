
CREATE DATABASE IF NOT EXISTS SolarX;

USE SolarX;

CREATE TABLE Batteries(
    id INT AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
	capacity_kwh  FLOAT NOT NULL,
    charge_max_speed_watt_second FLOAT NOT NULL,

    PRIMARY KEY (id),
    CHECK(capacity_kwh > 0)
);


CREATE TABLE Battery_readings(
	id INT AUTO_INCREMENT,
    battery INT,
    current_energy_watt FLOAT NOT NULL,
    current_hourly_consumption_watt FLOAT NOT NULL,
    status VARCHAR(11),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (id),
    FOREIGN KEY (battery) REFERENCES Batteries(id),

    CHECK(current_hourly_consumption_watt >= 0),
    CHECK(current_energy_watt >= 0),

    CHECK (status IN ('ideal', 'charging', 'discharging'))
);


CREATE TABLE Solar_pannels(
    id INT AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    capacity_kwh FLOAT NOT NULL,

    PRIMARY KEY (id),
    CHECK(capacity_kwh >= 0)
);


CREATE TABLE Solar_pannel_readings(
    id INT AUTO_INCREMENT,
    pannel INT,
    current_generation_watt FLOAT NOT NULL,
    current_generation_hourly_watt FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (id),
    FOREIGN KEY (pannel) REFERENCES Solar_pannels(id),

    CHECK(current_generation_watt >=0),
    CHECK(current_generation_hourly_watt >=0)
);


CREATE TABLE Home(
    id INT AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,

    PRIMARY KEY (id)
);


CREATE TABLE Home_devices_power_rating(
    id INT AUTO_INCREMENT,
    home INT,
    name VARCHAR(100) NOT NULL,
    consumption_min_wh FLOAT NOT NULL,
    consumption_max_wh FLOAT NOT NULL,
    time_of_use VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (id),
    FOREIGN KEY (home) REFERENCES Home(id),

    CHECK(consumption_min_wh >= 0),
    CHECK(consumption_max_wh >= 0)
);


CREATE TABLE Home_readings(
    id INT AUTO_INCREMENT,
    home INT,
    current_consumption_watt FLOAT NOT NULL,
    current_consumption_hourly_watt FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (id),
    FOREIGN KEY (home) REFERENCES Home(id),

    CHECK(current_consumption_watt >=0),
    CHECK(current_consumption_hourly_watt >=0)
);
