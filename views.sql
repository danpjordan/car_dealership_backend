CREATE VIEW customer_car_view AS
  SELECT id,
    vin,
    make,
    model,
    year,
    "imageUrl",
    price,
    miles,
    "timeCreated"
    description
    FROM car
   WHERE is_sold::text = 'N'::text;


CREATE VIEW customer_team_view AS
  SELECT u_.id,
    u_.name,
    u_.role,
    e_."imageUrl",
    e_."xUrl",
    e_."linkedinUrl"
    FROM employee e_
      JOIN "user" u_ ON e_.id = u_.id
   WHERE u_.active_status::text = 'Y'::text;


CREATE VIEW salerep_customer_view AS
  SELECT u_.id,
    u_.name,
    u_.username,
    u_.email,
    u_.phone,
    u_."timeCreated"
  FROM customer c_
    JOIN "user" u_ ON c_.id = u_.id
  WHERE u_.active_status::text = 'Y'::text;


CREATE VIEW manager_salesrep_view AS
 SELECT s_.id,
    su_.username,
    su_.name,
    su_.email,
    su_.phone,
    e_.salary,
    su_."timeCreated",
    mu_.name AS manager_name
   FROM sales_rep s_
     JOIN "user" su_ ON s_.id = su_.id
     JOIN manager m_ ON s_.manager_id = m_.id
     JOIN "user" mu_ ON m_.id = mu_.id
     JOIN employee e_ ON s_.id = e_.id;


-- Not a view but is a quary
  SELECT p_.id,
    c_.id AS customer_id,
    c_.username AS customer_username,
    c_.name AS customer_name,
    s_.id AS sales_rep_id,
    s_.username AS sales_rep_username,
    s_.name AS sales_rep_name,
    car.id AS car_id,
    car.vin AS car_vin,
    car.make AS car_make,
    car.model AS car_model,
    car.year AS car_year,
    car."imageUrl" AS car_imageurl,
    car.price AS car_price,
    car.miles AS car_miles,
    car.description AS car_description,
    p_.time_purchased
   FROM purchase p_
     JOIN "user" c_ ON p_.customer_id = c_.id
     JOIN "user" s_ ON p_.sales_rep_id = s_.id
     JOIN car car ON p_.car_id = car.id;