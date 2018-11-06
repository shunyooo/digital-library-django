CREATE DATABASE IF NOT EXISTS library CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
CREATE USER IF NOT EXISTS 'libraryuser'@'%' IDENTIFIED BY 'librarypass';
GRANT ALL PRIVILEGES ON library.* TO 'libraryuser'@'%';

FLUSH PRIVILEGES;
