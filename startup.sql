-- psql postgres -p 5433 -U postgres
-- \c car-dealership
-- \i startup.sql 
\copy employee FROM 'data/employees.csv' WITH DELIMITER ',' CSV HEADER;

