USE chicago_taxi;

CREATE TABLE IF NOT EXISTS taxi (
    taxi_id VARCHAR(255) PRIMARY KEY,
    public_vehicle_number INT,
    vehicle_make VARCHAR(255),
    vehicle_model_year INT,
    vehicle_color VARCHAR(255),
    vehicle_fuel_source VARCHAR(255),
    company_id INT
);

CREATE TABLE IF NOT EXISTS community (
    community_number INT PRIMARY KEY,
    community_name VARCHAR(255),
    population INT
);

CREATE TABLE IF NOT EXISTS company (
    company_id INT PRIMARY KEY,
    company VARCHAR(255),
    taxi_exterior_color VARCHAR(255),
    business_phone VARCHAR(255),
    dispatch_phone VARCHAR(255),
    address VARCHAR(255),
    city_state VARCHAR(255),
    zip INT,
    email VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS location (
    location_coordinates VARCHAR(255) PRIMARY KEY,
    address VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS trips (
    unique_key VARCHAR(255) PRIMARY KEY,
    taxi_id VARCHAR(255),
    trip_start_timestamp DATETIME,
    trip_end_timestamp DATETIME,
    trip_seconds FLOAT,
    trip_miles FLOAT,
    pickup_community_area INT,
    dropoff_community_area INT,
    fare DECIMAL(10, 2),
    tips DECIMAL(10, 2),
    extras DECIMAL(10, 2),
    trip_total DECIMAL(10, 2),
    payment_type VARCHAR(255),
    pickup_latitude DECIMAL(9, 6),
    pickup_longitude DECIMAL(9, 6),
    dropoff_latitude DECIMAL(9, 6),
    dropoff_longitude DECIMAL(9, 6),
    pickup_location VARCHAR(255),
    dropoff_location VARCHAR(255),
    company_id INT
);


