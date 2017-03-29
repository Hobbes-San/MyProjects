/*This is the file containing table creation statements for the Movie Database*/

CREATE TABLE movies
(
id integer not null AUTO_INCREMENT,
title varchar(100) not null,
year integer not null,
director varchar(100) not null,
banner_url varchar(200),
trailer_url varchar(200),
primary key(id),
unique key movie_key (title,year)
) ENGINE = MyISAM;

CREATE TABLE stars
(
id integer not null AUTO_INCREMENT,
first_name varchar(50) not null,
last_name varchar(50) not null,
dob date,
photo_url varchar(200),
primary key(id),
unique key star_key (first_name,last_name)
) ENGINE = MyISAM;

CREATE TABLE stars_in_movies
(
star_id integer not null,
movie_id integer not null,
foreign key(star_id) references stars(id),
foreign key(movie_id) references movies(id)
) ENGINE = MyISAM;

CREATE TABLE genres
(
id integer not null AUTO_INCREMENT,
name varchar(32) not null,
primary key(id),
unique key genre_key (name)
) ENGINE = MyISAM;

CREATE TABLE genres_in_movies
(
genre_id integer not null,
movie_id integer not null,
foreign key(genre_id) references genres(id),
foreign key(movie_id) references movies(id)
) ENGINE = MyISAM;

CREATE TABLE creditcards
(
id varchar(20) not null,
first_name varchar(50) not null,
last_name varchar(50) not null,
expiration date not null,
primary key(id)
) ENGINE = MyISAM;

CREATE TABLE customers
(
id integer not null AUTO_INCREMENT,
first_name varchar(50) not null,
last_name varchar(50) not null,
cc_id varchar(20) not null,
address varchar(200) not null,
email varchar(50) not null,
password varchar(20) not null,
primary key(id),
foreign key(cc_id) references creditcards(id)
) ENGINE = MyISAM;

CREATE TABLE sales
(
id integer not null AUTO_INCREMENT,
customer_id integer not null,
movie_id integer not null,
sale_date date not null,
primary key(id),
foreign key(customer_id) references customers(id),
foreign key(movie_id) references movies(id)
) ENGINE = MyISAM;

CREATE TABLE employees
(
email varchar(50) not null,
password varchar(20) not null,
fullname varchar(100),
primary key(email)
) ENGINE = MyISAM;
