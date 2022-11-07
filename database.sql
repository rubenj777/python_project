-- DROP TABLE app_user;
-- DROP TABLE appointment;

CREATE TABLE IF NOT EXISTS app_user(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   firstName TEXT,
   lastName TEXT,
   username TEXT,
   password TEXT,
   address TEXT,
   email TEXT,
   phone TEXT,
   specialization TEXT NULL,
   role INTEGER
);

CREATE TABLE IF NOT EXISTS appointment(
   user_id INTEGER,
   doc_id INTEGER,
   appointment_time DATETIME,
   cause TEXT,
   PRIMARY KEY(user_id, doc_id),
   FOREIGN KEY(user_id) REFERENCES app_user(id),
   FOREIGN KEY(doc_id) REFERENCES app_user(id)
);


-- INSERT INTO app_user ('firstName', 'lastName', 'username', 'password', 'address', 'email', 'phone', 'role') VALUES ('ruben', 'jallifier', 'rub', 'mdp', 'lyon', 'mail', '06', '1');
-- INSERT INTO app_user ('firstName', 'lastName', 'username', 'password', 'address', 'email', 'phone', 'role') VALUES ('docteur', 'jean', 'jean', 'mdp', 'lyon', 'mail', '06', '2');


