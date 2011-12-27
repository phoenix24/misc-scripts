#drop the databse if it already exists.
drop database if exists icrackitdb2;

#create a new database named icrackitdb2.
create database icrackitdb2;

#grant all privileges to the user "icrackituser"
grant all on icrackitdb2.* to 'icrackituser'@'localhost';


