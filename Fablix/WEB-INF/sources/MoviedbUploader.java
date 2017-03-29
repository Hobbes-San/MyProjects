import java.io.IOException;
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import java.net.*;
import java.util.*;
import java.sql.*;

//This java file takes the filmTable and the starList from MoviedbParser.java file
//and uploads the information into the mySQL database.

public class MoviedbUploader {
	
	public void uploadData(List<Star> starList, Map<String,Film> filmTable) throws SQLException {
		try {
			Class.forName("com.mysql.jdbc.Driver").newInstance();
			Connection dbcon = DriverManager.getConnection("jdbc:mysql:///moviedb?autoReconnect=true&useSSL=false", "testuser", "testpassword");
			
			//Set autocommit to false because we will use batch updates.
			
			dbcon.setAutoCommit(false);
			
			PreparedStatement insertmovie = dbcon.prepareStatement("INSERT IGNORE INTO movies (title,year,director) VALUES (?,?,?)");
			PreparedStatement searchmovie = dbcon.prepareStatement("SELECT id FROM movies WHERE title = ? AND year = ? AND director = ?");
			
			PreparedStatement insertstar = dbcon.prepareStatement("INSERT IGNORE INTO stars (first_name,last_name,dob) VALUES (?,?,?)");
			PreparedStatement searchstar = dbcon.prepareStatement("SELECT id FROM stars WHERE first_name = ? AND last_name = ?");
			
			PreparedStatement searchgenre = dbcon.prepareStatement("SELECT id FROM genres WHERE name LIKE ?");
			PreparedStatement insertgenre = dbcon.prepareStatement("INSERT IGNORE INTO genres (name) VALUES (?)", Statement.RETURN_GENERATED_KEYS);
			
			PreparedStatement insertgim = dbcon.prepareStatement("INSERT IGNORE INTO genres_in_movies (genre_id,movie_id) VALUES (?,?)");
			PreparedStatement insertsim = dbcon.prepareStatement("INSERT IGNORE INTO stars_in_movies (star_id,movie_id) VALUES (?,?)");
			
			//Upload stars from starList into the mySQL database.
			
			for (int i = 0; i < starList.size(); i++) {
				Star tempStar = starList.get(i);
				String firstname = tempStar.getFirstName();
				String lastname = tempStar.getLastName();
				String dob = tempStar.getDob();
				
				try {
					insertstar.setString(1, firstname);
					insertstar.setString(2, lastname);
					
					//See if the year in the date of birth column is valid.
					
					try {
						int test = Integer.parseInt(dob);
						insertstar.setString(3, test + "-1-1");
					} catch (Exception e) {
						insertstar.setString(3, null);
					}
					
					insertstar.addBatch();
						
				} catch (Exception e) {
					System.out.println(e.getMessage() + " Error in inserting the star with First Name: " + firstname + " Last Name: " + lastname + " DOB: " + dob);
				}
			}
			
			//Batch for faster updates.
			
			insertstar.executeBatch();
			dbcon.commit();
			
			//Upload movies from filmTable into the mySQL database.
			
			for (Film film : filmTable.values()) {
				String title = film.getTitle();
				Integer year = film.getYear();
				String director = film.getDirector();
				
				//See if the information is valid.
				
				try {
					insertmovie.setString(1, title);
					insertmovie.setInt(2, year);
					insertmovie.setString(3, director);
					
					insertmovie.addBatch();
					
				} catch (SQLException e) {
					System.out.println(e.getMessage() + " Error in inserting the movie with Title: " + title + " Year: " + year + " Director: " + director);
				}
			}
			
			//Batch for faster updates.
			
			insertmovie.executeBatch();
			dbcon.commit();
			
			//Upload stars_in_movies and genres_in_movies information from the filmTable into the mySQL database.
			
			for (Film film : filmTable.values()) {
				String title = film.getTitle();
				Integer year = film.getYear();
				String director = film.getDirector();
				
				Integer movieid = null;
				
				//Get the movie id from the database.
				
				searchmovie.setString(1, title);
				searchmovie.setInt(2, year);
				searchmovie.setString(3, director);
				
				ResultSet searchmoviers = searchmovie.executeQuery();
				
				if (searchmoviers.next()) {
					movieid = searchmoviers.getInt(1);
					
					//Get the genre ids from the database.
					
					try {
						List<String> genres = film.getGenres();
						
						//If the genre name is "close enough" to one already in the database,
						//we use the one in the database.
						
						for (int i = 0; i < genres.size(); i++) {
							String genre = genres.get(i);
							StringBuilder like = new StringBuilder();
							
							for (int j = 0; j < genre.length(); j++) {
								like.append(genre.charAt(j));
								like.append('%');
							}
							
							searchgenre.setString(1, like.toString());
							ResultSet searchgenrers = searchgenre.executeQuery();
							
							if (searchgenrers.next()) {
								insertgim.setInt(1, searchgenrers.getInt(1));
								
							//If we had to insert a new genre, get the generated id so that
							//we can put it in the genres_in_movies table.
								
							} else {
								insertgenre.setString(1, genre);
								insertgenre.executeUpdate();
								
								ResultSet insertgenrers = insertgenre.getGeneratedKeys();
								insertgenrers.next();
											
								insertgim.setInt(1, insertgenrers.getInt(1));
								insertgenrers.close();
							}
							
							searchgenrers.close();
							
							insertgim.setInt(2, movieid);
							insertgim.addBatch();
							
						}
					} catch (SQLException e) {
						System.out.println(e.getMessage() + " Error in handling genre information for the movie with Title: " + title + " Year: " + year + " Director: " + director);
					}
					
					//Get the database ids of the stars featured in the movie.
					
					try {
						List<Star> stars = film.getStars();
						
						for (int i = 0; i < stars.size(); i++) {
							Star tempStar = stars.get(i);
							String firstname = tempStar.getFirstName();
							String lastname = tempStar.getLastName();
							
							searchstar.setString(1, firstname);
							searchstar.setString(2, lastname);
							
							ResultSet searchstarrs = searchstar.executeQuery();
							
							if (searchstarrs.next()) {
								insertsim.setInt(1, searchstarrs.getInt(1));
								insertsim.setInt(2, movieid);
								insertsim.addBatch();
							}
							
							searchstarrs.close();
						}
								
					} catch (SQLException e) {
						System.out.println(e.getMessage() + " Error in handling star information for the movie with Title: " + title + " Year: " + year + " Director: " + director);
					}
					
					insertsim.executeBatch();
					dbcon.commit();
					
				}
				
				searchmoviers.close();
			}
			
			//Batch for faster updates.
			
			insertgim.executeBatch();
			dbcon.commit();
			
			insertsim.executeBatch();
			dbcon.commit();
			
			dbcon.setAutoCommit(true);
			
			insertmovie.close();
			insertstar.close();
				
			searchstar.close();
			searchmovie.close();
			
			searchgenre.close();
			insertgenre.close();
			
			insertgim.close();
			insertsim.close();
			
			dbcon.close();
			
		} catch (SQLException e) {
			while (e != null) {
                System.out.println("SQL Exception:  " + e.getMessage());
                e = e.getNextException();
            }
		} catch (Exception ex) {
			System.out.println("Error: " + ex.getMessage());
		}
	}
	
	//Run the uploader.
	
	public static void main(String[] args) throws SQLException {
		MoviedbParser mp = new MoviedbParser();
		mp.parseDocument();
		
		MoviedbUploader mu = new MoviedbUploader();
		mu.uploadData(mp.getStarList(), mp.getFilmTable());
	}
}
