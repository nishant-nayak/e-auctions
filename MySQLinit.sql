-- Create a new database for the web application
CREATE DATABASE auction_data CHARACTER SET utf8mb4;

-- Create a new user and provide full access to the newly created database
CREATE USER 'djangouser'@'%' IDENTIFIED WITH mysql_native_password BY 'NITK2021';
GRANT ALL ON auction_data.* TO 'djangouser'@'%';
FLUSH PRIVILEGES;