-- DROP TABLE patient;
-- DROP TABLE doctor;
-- DROP TABLE visit;

CREATE TABLE if NOT EXISTS patient(
   id INT,
   firstName VARCHAR(50),
   lastName VARCHAR(50),
   username VARCHAR(50),
   password VARCHAR(50),
   PRIMARY KEY(id)
);

CREATE TABLE if NOT EXISTS doctor(
   id INT,
   firstName VARCHAR(50),
   lastName VARCHAR(50),
   password VARCHAR(50),
   username VARCHAR(50),
   specialisation VARCHAR(50),
   PRIMARY KEY(id)
);

CREATE TABLE if NOT EXISTS VISIT(
   id INT,
   id_1 INT,
   appointed_time DATETIME,
   cause VARCHAR(500),
   PRIMARY KEY(id, id_1),
   FOREIGN KEY(id) REFERENCES patient(id),
   FOREIGN KEY(id_1) REFERENCES doctor(id)
);

