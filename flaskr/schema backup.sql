 DROP TABLE IF EXISTS user;
 DROP TABLE IF EXISTS property;
 DROP TABLE IF EXISTS todos;
 DROP TABLE IF EXISTS tohosts;

 CREATE TABLE user (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 username TEXT UNIQUE NOT NULL,
 password TEXT NOT NULL,
 nickname TEXT NOT NULL,
 countryInput TEXT NOT NULL,
 stateInput TEXT NOT NULL,
 districtInput TEXT NOT NULL,
 phone INT NOT NULL
 );

 CREATE TABLE property (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 property_name TEXT UNIQUE NOT NULL,
 property_status TEXT NOT NULL,
 property_address TEXT NOT NULL,
 stateInput TEXT NOT NULL,
 districtInput TEXT NOT NULL,
 ttl_room INT NOT NULL,
 ttl_bathroom INT NOT NULL,
 aircond TEXT NOT NULL, 
 wifi TEXT NOT NULL, 
 washing TEXT NOT NULL, 
 cooking TEXT NOT NULL, 
 homestay_rate REAL NOT NULL,
 phone INT NOT NULL
 );

 CREATE TABLE todos (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 todo_owner TEXT NOT NULL,
 task_name TEXT NOT NULL,
 task_description TEXT NOT NULL,
 due_date TEXT NOT NULL,
 status TEXT NOT NULL
 );

 CREATE TABLE tohosts (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 guest_name TEXT NOT NULL,
 guest_email TEXT NOT NULL,
 check_in_date TEXT NOT NULL,
 check_out_date TEXT NOT NULL,
 total_days INTEGER,
 daily_rate REAL,
 total_rate REAL,
 payment_status TEXT NOT NULL
 );