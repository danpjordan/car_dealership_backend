-- cd car-dealership/project-backend 
-- psql postgres -p 5433 -U postgres
-- \c car-dealership
-- \i startup.sql 
\copy employee FROM 'data/employees.csv' WITH DELIMITER ',' CSV HEADER;
\copy car FROM 'data/cars.csv' WITH DELIMITER ',' CSV HEADER;

