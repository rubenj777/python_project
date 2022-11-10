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

INSERT OR IGNORE INTO app_user ('firstName', 'lastName', 'username', 'password', 'address', 'email', 'phone', 'specialization', 'role') VALUES ('jean', 'michel', 'jm', 'mdp', 'lyon', 'jm@mail.com', '0660598045', 'chiropractor', '2');