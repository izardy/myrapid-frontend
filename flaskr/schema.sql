 DROP TABLE IF EXISTS idea;

 CREATE TABLE idea (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 idea_name TEXT UNIQUE NOT NULL,
 idea_status TEXT NOT NULL,
 idea_statement TEXT NOT NULL,
 idea_issue TEXT NOT NULL,
 idea_strategy TEXT NOT NULL,
 issue_depot TEXT NOT NULL,
 issue_driver TEXT NOT NULL,
 issue_bus TEXT NOT NULL,
 issue_trip TEXT NOT NULL, 
 pitch_date TEXT NOT NULL,
 phone INT NOT NULL
 );