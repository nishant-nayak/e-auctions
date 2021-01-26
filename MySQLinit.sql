CREATE DATABASE auction_data CHARACTER SET utf8mb4;
CREATE USER 'djangouser'@'%' IDENTIFIED WITH mysql_native_password BY 'NITK2021';
GRANT ALL ON auction_data.* TO 'djangouser'@'%';
FLUSH PRIVILEGES;