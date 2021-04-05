CREATE TABLE auth_user (
  id INTEGER NOT NULL AUTO_INCREMENT,
  username VARCHAR(70) UNIQUE NOT NULL,
  password VARCHAR(70) NOT NULL,
  fullname VARCHAR(100), 
  email VARCHAR(70) UNIQUE NOT NULL,
  phone VARCHAR(25),
  birth DATETIME,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  is_staff TINYINT(1) NOT NULL DEFAULT 0,
  is_superuser TINYINT(1) NOT NULL DEFAULT 0,
  last_login DATETIME DEFAULT NULL,
  dh_insert DATETIME DEFAULT NOW(),
  PRIMARY KEY(id)
);

CREATE TABLE auth_group (
  id INTEGER NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  dh_update DATETIME,
  dh_insert DATETIME DEFAULT NOW(),
  PRIMARY KEY(id)
);

CREATE TABLE auth_user_group (
  id INTEGER NOT NULL AUTO_INCREMENT,
  user_id INTEGER NOT NULL,
  group_id INTEGER NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(user_id) REFERENCES auth_user(id),
  FOREIGN KEY(group_id) REFERENCES auth_group(id)
);

CREATE TABLE auth_permission (
  id INTEGER NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  dh_update DATETIME,
  dh_insert DATETIME DEFAULT NOW(),
  PRIMARY KEY(id)
);

CREATE TABLE auth_user_permission (
  id INTEGER NOT NULL AUTO_INCREMENT,
  user_id INTEGER NOT NULL,
  permission_id INTEGER NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(user_id) REFERENCES auth_user(id),
  FOREIGN KEY(permission_id) REFERENCES auth_permission(id)
);

CREATE TABLE auth_session (
  id INTEGER NOT NULL AUTO_INCREMENT,
  user_id INTEGER NOT NULL UNIQUE,
  access_token LONGTEXT NOT NULL UNIQUE
  expire_date DATETIME NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(user_id) REFERENCES auth_user(id)
);

CREATE TABLE password_reset (
  id INTEGER NOT NULL AUTO_INCREMENT,
  user_id INTEGER NOT NULL,
  reset_key VARCHAR(200) NOT NULL UNIQUE,
  is_active TINYINT(1),
  expire_date DATETIME NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(user_id) REFERENCES auth_user(id)
);

INSERT INTO auth_user (
  username,
  password,
  email
) VALUES (
  'admin',
  '$2b$12$e.L97G95MrCQpta7SBTEkeyRAqPeUMdTkTp3pugkseTy9Q7Fqy6XS',
  'admin'
)
