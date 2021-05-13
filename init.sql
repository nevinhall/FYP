CREATE DATABASE IF NOT EXISTS users;
CREATE DATABASE IF NOT EXISTS user_profiles;

      

USE users;
CREATE TABLE IF NOT EXISTS users(
    user_id varchar(255) NOT NULL UNIQUE,
    email varchar(255) NOT NULL UNIQUE,
    password varchar(255) NOT NULL
);


INSERT IGNORE INTO `users`
SET `user_id` = 'admin1',
`email` = 'admin@gmail.com',
`password` = 'admin';


USE user_profiles;
CREATE TABLE IF NOT EXISTS user_profiles(
    user_id varchar(255) UNIQUE,
    height int, 
    weight int,
    bmi int, 
    activity_level varchar(255),
    dietary_options varchar(255),
    allergies varchar(255),
    age int,
    calories int, 
    gender varchar(255)
   
);





