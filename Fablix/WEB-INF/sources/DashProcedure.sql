DELIMITER //
DROP PROCEDURE IF EXISTS `moviedb`.`add_movie`//
CREATE PROCEDURE `moviedb`.add_movie (IN newtitle varchar(100), IN newyear INT, IN newdirector varchar(100), IN star_first varchar(50), IN star_last varchar(50), IN newgenre varchar(32))
main:BEGIN
	DECLARE starid INT;
	DECLARE genreid INT;
	DECLARE movieid INT;
	DECLARE EXIT HANDLER FOR SQLEXCEPTION
	BEGIN
	SELECT 'There was an error in entering the movie info into the movies table.' as '';
	ROLLBACK;
	END;
	
	SELECT id INTO movieid FROM movies WHERE title = newtitle AND year = newyear AND director = newdirector;
	SELECT id INTO starid FROM stars WHERE first_name = star_first AND last_name = star_last;
	SELECT id INTO genreid FROM genres WHERE name = newgenre;
	
	IF movieid IS NOT null THEN
	SELECT 'The movie is already in the database.' as '';
	LEAVE main;
	END IF;
	
	IF starid IS null THEN
	INSERT INTO stars (first_name,last_name)
	VALUES (star_first,star_last);
	SET starid = LAST_INSERT_ID();
	END IF;
	SELECT 'The star info has been processed' as '';
	
	IF genreid IS null THEN
	INSERT INTO genres (name)
	VALUES (newgenre);
	SET genreid = LAST_INSERT_ID();
	END IF;
	SELECT 'The genre info has been processed' as '';
	
	INSERT INTO movies (title,year,director)
	VALUES (newtitle,newyear,newdirector);
	SET movieid = LAST_INSERT_ID();
	SELECT 'The movie info has been entered into the movies table.' as '';
	
	INSERT INTO stars_in_movies (star_id, movie_id)
	VALUES (starid, movieid);
	SELECT 'The star/movie pairing has been entered into the stars_in_movies table.' as '';
	
	INSERT INTO genres_in_movies (genre_id, movie_id)
	VALUES (genreid, movieid);
	SELECT 'The genre/movie pairing has been entered into the genres_in_movies table.' as '';
	
END //
DELIMITER ;