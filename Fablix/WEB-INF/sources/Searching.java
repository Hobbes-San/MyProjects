import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import java.net.*;
import java.util.*;
import java.sql.*;

import javax.naming.InitialContext;
import javax.naming.Context;
import javax.sql.DataSource;

//This servlet allows customers to search for movies by a number of different categories.

public class Searching extends HttpServlet {
	public void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		
		response.setContentType("text/html");
		PrintWriter out = response.getWriter();
		HttpSession session = request.getSession();
		
		try {
			
			//Use connection pooling to access the mySQL database.
			
			Context initCtx = new InitialContext();
			if (initCtx == null) {
				out.println("initCtx is NULL");
			}
			
			Context envCtx = (Context) initCtx.lookup("java:comp/env");
			if (envCtx == null) {
				out.println("envCtx is NULL");
			}
			
			DataSource ds = (DataSource) envCtx.lookup("jdbc/TestDB");
			if (ds == null) {
				out.println("ds is NULL");
			}
			
			Connection dbcon = ds.getConnection();
			if(dbcon == null) {
				out.println("dbcon is NULL");
			}
			
			String inorout = null;
			URL inoroutURL = null;
			
			//Check if the customer is logged in or not.
			
			if (session.getAttribute("loggedIn") != null) {
				inorout = "Log Out";
				inoroutURL = new URL("http://52.37.235.2/Fablix/servlet/LogOut");
			} else {
				inorout = "Log In";
				inoroutURL = new URL("http://52.37.235.2/Fablix/LogInPage.html");
			}
			
			String firstorgenre = request.getParameter("firstorgenre");
			
			String movieQ = "";
			PreparedStatement moviestmt = null;
			ResultSet moviers = null;
			
			String first = "";
			Integer genreid = null;
			
			String title = "";
			String year = "";
			String director = "";
			String firstname = "";
			String lastname = "";
			
			StringBuilder sb = new StringBuilder();
			
			URL titleURL = null;
			URL yearURL = null;
			
			URL prev = null;
			URL next = null;
			URL update = null;
			
			//A non-null firstorgenre value denotes the customer is trying to browse for movies
			//alphabetically or by genre.
			
			//A null firstorgenre value denotes the customer is trying to search for movies
			//by title/year/director/star name.
			
			if (firstorgenre == null) {
			
				title = request.getParameter("title");
				year = request.getParameter("year");
				director = request.getParameter("director");
				firstname = request.getParameter("firstname");
				lastname = request.getParameter("lastname");
				
				if (title == null) {
					title = "";
				}
				
				if (year == null) {
					year = "";
				}
				
				if (director == null) {
					director = "";
				}
				
				if (firstname == null) {
					firstname = "";
				}
				
				if (lastname == null) {
					lastname = "";
				}
				
				title = title.trim();
				year = year.trim();
				director = director.trim();
				firstname = firstname.trim();
				lastname = lastname.trim();
				
				//Carry out inner join of movies and stars_in_movies table in order to
				//get all movies featuring a given star.
				
				if (!(firstname.equals("")) || !(lastname.equals(""))) {
					sb.append("SELECT movies.title, movies.id, movies.year, movies.director FROM movies " +
							  "INNER JOIN stars_in_movies ON movies.id = stars_in_movies.movie_id " +
							  "WHERE movies.title LIKE ? AND CAST(movies.year AS CHAR) LIKE ? AND movies.director LIKE ?");
					String starQ = "SELECT id FROM stars WHERE first_name LIKE ? AND last_name LIKE ?";
					PreparedStatement starstmt = dbcon.prepareStatement(starQ);
					starstmt.setString(1, "%" + firstname + "%");
					starstmt.setString(2, "%" + lastname + "%");
					ResultSet starrs = starstmt.executeQuery();
					
					if (starrs.next()) {
						sb.append(" AND stars_in_movies.star_id IN (");
						sb.append(starrs.getInt(1));
						while (starrs.next()) {
							sb.append(", " + starrs.getInt(1));
						}
						sb.append(")");
					}
					
					starrs.close();
					starstmt.close();
				
				//If the user did not input any information for a star, then carry out the search
				//just by title/year/director.
				
				} else if (!title.equals("") || !year.equals("") || !director.equals("")) {
					sb.append("SELECT title, id, year, director FROM movies " +
							  "WHERE title LIKE ? AND CAST(year AS CHAR) LIKE ? AND director LIKE ?");
				}
				
			} else {
				firstorgenre = request.getParameter("firstorgenre");
				
				if (firstorgenre.equals("bygenre")) {
					genreid = Integer.parseInt(request.getParameter("genreid").trim());
					
					//Carry out inner join of movies and genres_in_movies table in order to
					//get all movies of a given genre.
					
					sb.append("SELECT movies.title, movies.id, movies.year, movies.director FROM movies " +
							 "INNER JOIN genres_in_movies ON movies.id = genres_in_movies.movie_id " +
							 "WHERE genres_in_movies.genre_id = ?");
							 
				} else if (firstorgenre.equals("byfirst")) {
					
					//Get all movies starting with a given number or alphabet.
					
					first = request.getParameter("first").trim();
					sb.append("SELECT title, id, year, director FROM movies WHERE title LIKE ?");
				}
			}
			
			Integer start = 0;
			Integer perpage = 10;
			String sortparam = null;
			
			Integer newstart = 0;
			String sort = "";
			
			//Order the search results by either title or year.
			
			if (sb.length() != 0) {
				sortparam = request.getParameter("sortBy");
				if (sortparam != null) {
					if (sortparam.equals("title")) {
						sb.append(" ORDER BY title");
						sort = "title";
					}
					if (sortparam.equals("year")) {
						sb.append(" ORDER BY year");
						sort = "year";
					}
				}
				
				//Modify the search query depending on the starting index of the search result.
				
				String temp1 = request.getParameter("start");
				if (temp1 == null) {
					start = 0;
					sb.append(" LIMIT 0,");
				} else {
					try {
						start = Integer.parseInt(temp1);
						sb.append(" LIMIT " + start + ", ");
					} catch (Exception e) {
						out.println("Starting index not an integer");
					}
				}
				
				//Modify the search query depending on how many results to display per page.
				
				String temp2 = request.getParameter("perpage");
				if (temp2 == null) {
					perpage = 10;
					sb.append("10");
				} else {
					try {
						perpage = Integer.parseInt(temp2);
						sb.append(perpage);
					} catch (Exception e) {
						out.println("Number of entries per page not an integer");
					}
				}
				
			}
			
			if (start != 0) {
				newstart = start-perpage;
			}
			
			Integer nextstart = start+perpage;
			
			movieQ = sb.toString();
			
			String _title = urlFormat(title);
			String _director = urlFormat(director);
			
			if (firstorgenre == null) {
				if (!(movieQ.equals(""))) {
					moviestmt = dbcon.prepareStatement(movieQ);
					moviestmt.setString(1, "%" + title + "%");
					moviestmt.setString(2, "%" + year + "%");
					moviestmt.setString(3, "%" + director + "%");
					
					//Prepare to search for movies and set the appropriate URLs
					//for sorting by title/year, examining prev/next results, and updating the numebr of results per page.
					
					titleURL = new URL("http://52.37.235.2/Fablix/servlet/Searching?sortBy=title&start=" + start + "&perpage=" + perpage + "&title=" + _title +
									   "&year=" + year + "&director=" + _director + "&firstname=" + firstname + "&lastname=" + lastname);
									   
					yearURL = new URL("http://52.37.235.2/Fablix/servlet/Searching?sortBy=year&start=" + start + "&perpage=" + perpage + "&title=" + _title +
									  "&year=" + year + "&director=" + _director + "&firstname=" + firstname + "&lastname=" + lastname);
					
					prev = new URL("http://52.37.235.2/Fablix/servlet/Searching?sortBy=" + sort + "&start=" + newstart + "&perpage=" + perpage + "&title=" + _title +
								   "&year=" + year + "&director=" + _director + "&firstname=" + firstname + "&lastname=" + lastname);
								   
					next = new URL("http://52.37.235.2/Fablix/servlet/Searching?sortBy=" + sort + "&start=" + nextstart + "&perpage=" + perpage + "&title=" + _title +
								   "&year=" + year + "&director=" + _director + "&firstname=" + firstname + "&lastname=" + lastname);
				
					update = new URL("http://52.37.235.2/Fablix/servlet/Searching?sortBy=" + sort + "&start=0" + "&title=" + _title +
									 "&year=" + year + "&director=" + _director + "&firstname=" + firstname + "&lastname=" + lastname);
				}									 
				
			} else {
				moviestmt = dbcon.prepareStatement(movieQ);
				
				//Prepare to browse for movies and set the appropriate URLs
				//for sorting by title/year, examining prev/next results, and updating the numebr of results per page.
				
				if (firstorgenre.equals("bygenre")) {
					moviestmt.setInt(1, genreid);
					
					titleURL = new URL("http://52.37.235.2/Fablix/servlet/Searching?sortBy=title&start=" + start + "&perpage=" + perpage +
									   "&genreid=" + genreid + "&firstorgenre=bygenre");
									   
					yearURL = new URL("http://52.37.235.2/Fablix/servlet/Searching?sortBy=year&start=" + start + "&perpage=" + perpage +
									   "&genreid=" + genreid + "&firstorgenre=bygenre");
									   
					prev = new URL("http://52.37.235.2/Fablix/servlet/Searching?sortBy=" + sort + "&start=" + newstart + "&perpage=" + perpage +
								   "&genreid=" + genreid + "&firstorgenre=bygenre");
								   
					next = new URL("http://52.37.235.2/Fablix/servlet/Searching?sortBy=" + sort + "&start=" + nextstart + "&perpage=" + perpage +
								   "&genreid=" + genreid + "&firstorgenre=bygenre");
								   
					update = new URL("http://52.37.235.2/Fablix/servlet/Searching?sortBy=" + sort + "&start=0" +
								     "&genreid=" + genreid + "&firstorgenre=bygenre");
					
				} else if (firstorgenre.equals("byfirst")) {
					moviestmt.setString(1, first + "%");
					
					titleURL = new URL("http://52.37.235.2/Fablix/servlet/Searching?sortBy=title&start=" + start + "&perpage=" + perpage +
									   "&first=" + first + "&firstorgenre=byfirst");
									   
					yearURL = new URL("http://52.37.235.2/Fablix/servlet/Searching?sortBy=year&start=" + start + "&perpage=" + perpage +
									   "&first=" + first + "&firstorgenre=byfirst");
									   
					prev = new URL("http://52.37.235.2/Fablix/servlet/Searching?sortBy=" + sort + "&start=" + newstart + "&perpage=" + perpage +
								   "&first=" + first + "&firstorgenre=byfirst");
								   
					next = new URL("http://52.37.235.2/Fablix/servlet/Searching?sortBy=" + sort + "&start=" + nextstart + "&perpage=" + perpage +
								   "&first=" + first + "&firstorgenre=byfirst");
								   
					update = new URL("http://52.37.235.2/Fablix/servlet/Searching?sortBy=" + sort + "&start=0" +
								     "&first=" + first + "&firstorgenre=byfirst");
				}
			}
			
			if (moviestmt != null) {
				moviers = moviestmt.executeQuery();
			}
			
			out.println("<head>\n" +
						"<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css'>\n" +
						"<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js'></script>\n" +
						"<script src='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js'></script>\n" +
						"<link rel='stylesheet' href='https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/themes/smoothness/jquery-ui.css'>\n" +
						"<script src='https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js'></script>\n" +
						"	<script>\n" +
						
						//The autocomplete feature breaks up the search words in real time
						//into keywords, then sends them to the FullTextSearch servlet in order to perform
						//full text search in the mySQL database in real time to suggest titles to the user.
						
						"	$(document).ready(function() {\n" +
						"		$('#title').autocomplete({\n" +
						"			source: function(request, response) {\n" +
						"				$.ajax({\n" +
						"					url: '/Fablix/servlet/FullTextSearch',\n" +
						"					type: 'GET',\n" +
						"					data: {\n" +
						"						term: request.term\n" +
						"					},\n" +
						"					datType: 'json',\n" +
						"					success: function(data) {\n" +
						"						console.log(data);\n" +
						"						response(data);\n" +
						"					}\n" +
						"				});\n" +
						"			}\n" +
						"		});\n" +
						"	});\n" +
						"	</script>\n" +
						"<style>\n" +
						"	.popover {\n" +
						"		max-width: 100%;\n" +
						"	}\n" +
						"  /* Popover Header */\n" +
						"  .popover-title {\n" +
						"	  background-color: lightgreen; \n" +
						"	  text-align:center;\n" +
						"  }\n" +
						"  /* Popover Body */\n" +
						"  .popover-content {\n" +
						"	  background-color: lightgreen;\n" +
						"  }\n" +
						"	table, th, td {\n" +
						"		border: 1px solid black;\n" +
						"	}\n	" +
						"	body {\n" +
						"		background-image: url('https://previews.123rf.com/images/apostrophe/apostrophe1403/apostrophe140300013/26540708-bright-yellow-background-solid-color-primary-image-with-soft-vintage-grunge-background-texture-desig-Stock-Photo.jpg');\n" +
						"	}\n" +
						"</style>\n" +
						"</head>\n" +
						"<BODY>\n" +
						
						//Default format for the website.
						
						"	<p style='float:left;font-size:40px;margin-top:10px;margin-left:30px'>Fablix... One stop shop for your favorite flix!</p>\n" +
						"	<form action='/Fablix/servlet/Searching' style='float:right;margin-top:20px;margin-right:30px' name='titleSearch' method='get'>\n" +
						"		<input type='text' id='title' name='title' placeholder='Search for a movie...'>\n" +
						"		<input type='submit' value='Search'><br>\n" +
						"		<a href='/Fablix/servlet/Home'>Home</a> &nbsp|&nbsp <a href='/Fablix/Search.html'>Advanced Search</a>\n " +
						"		&nbsp|&nbsp <a href='" + inoroutURL + "'>" + inorout + "</a> &nbsp|&nbsp <a href='/Fablix/servlet/ShoppingCart'>My Cart</a>\n " + 
						"		&nbsp|&nbsp <a href='/Fablix/servlet/Checkout'>Checkout</a> &nbsp|&nbsp <a href='/Fablix/dashboard.html'>Employee Dashboard</a>\n" +
						"	</form>\n" +
						"<H1 style='clear:both;text-align:center'>Search Results</H1>\n" +
						"<TABLE style='margin-left:auto;margin-right:auto'>\n" +
						"<TR> <TH><A HREF=" + titleURL + ">Title</A></TH> <TH>ID</TH> <TH><A HREF=" + yearURL + ">Year</A></TH> <TH>Director</TH> <TH>Genres</TH> <TH>Stars</TH> <TH>&nbsp</TH> </TR>\n");
								
			if (moviers != null) {
				
				//Prepare to search for all genres that the movie belongs to
				//and all stars that the movie features.
				
				PreparedStatement gimstmt = dbcon.prepareStatement("SELECT genres.name FROM genres " +
											"INNER JOIN genres_in_movies ON genres.id = genres_in_movies.genre_id " +
											"WHERE genres_in_movies.movie_id = ?");
				
				PreparedStatement simstmt = dbcon.prepareStatement("SELECT stars.id, stars.first_name, stars.last_name FROM stars " +
											"INNER JOIN stars_in_movies ON stars.id = stars_in_movies.star_id " +
											"WHERE stars_in_movies.movie_id = ?");
				
				while (moviers.next()) {
					out.print("<TR>");
					int movieid = moviers.getInt(2);
				
					URL movieURL = new URL("http://52.37.235.2/Fablix/servlet/SingleMovie?movieid=" + movieid);
					
					//Display the pop-up containing information related to the movie.
					
					out.println("<script>\n" +
								"$(document).ready(function(){\n" +
								"	if ($('#" + movieid + "').data('bs.popover') == null) {\n" +
								"		$.ajax({\n" +
								"			url: '/Fablix/servlet/PopupMovieInfo?movieid=" + movieid + "',\n" +
								"			dataType: 'html',\n" +
								"			success: function(html) {\n" +
								"				$('#" + movieid + "').popover({\n" +
								"					title: 'Info',\n" +
								"					animation: false,\n" +
								"					content: html,\n" +
								"					container: $('#" + movieid + "'),\n" +
								"					html: true,\n" +
								"					trigger: 'hover'\n" +
								"				})\n" +
								"			}\n" +
								"		});\n" +
								"	}\n" +
								"});\n" +
								"</script>\n");
								
					out.print("<TD>\n" +
							  "<A HREF='" + movieURL + "' id='" + movieid + "'>" + moviers.getString(1) + "</A>\n" +
							  "</TD>\n");
					
					//Display all the relevant movie information in a table format.
					
					for (int i = 2; i < 5; i++) {
						out.print("<TD>" + moviers.getString(i) + "</TD>");
					}
					
					gimstmt.setInt(1, movieid);
					ResultSet gimrs = gimstmt.executeQuery();
					out.println("<TD> <UL>");
					
					//Display all genres the movie belongs to.
					
					while(gimrs.next()) {
						out.print("<LI>" + gimrs.getString(1) + "</LI>");
					}
					
					out.println("</TD> </UL>");
					gimrs.close();
					
					simstmt.setInt(1, movieid);
					ResultSet simrs = simstmt.executeQuery();
						
					out.println("<TD> <UL>");
					
					//Display all star the movie features.
					
					while (simrs.next()) {
						int starid = simrs.getInt(1);
						URL starURL = new URL("http://52.37.235.2/Fablix/servlet/SingleStar?starid=" + starid);
						out.print("<LI> <A HREF=" + starURL + ">" + simrs.getString(2) + " " + simrs.getString(3) + "</A> </LI>");
					}
					
					out.println("</TD> </UL>");
					simrs.close();
					
					//Allow customer to add the movie to the cart.
					
					out.println("<TD> <button type='button' onclick=window.location.assign('/Fablix/servlet/ShoppingCart?movieid=" + movieid + "&quantity=1')>Add to shopping cart</button> </TD>");
				
					out.println("</TR>");
				}		
				
				moviers.close();
				gimstmt.close();
				simstmt.close();
				
			}
			
			out.println("</TABLE>\n");
			
			if (moviestmt != null) {
				moviestmt.close();
			}
			
			//Let the customer know how many results are currently displayed per page, and allow him/her to change it.
			//Also allow him/her to look at prev/next search results.
			
			out.println("<form action=" + update + " method=post> <p style=text-align:right> <A HREF=" + prev + ">Prev</A> <A HREF=" + next + ">Next</A> Currently " + perpage + " Per page</p>\n" +
						"<p style=text-align:center> <select name='perpage'><option value=10>10</option> <option value=25>25</option> <option value=50>50</option> <option value=100>100</option> </select> " +
						" Per page <input type=submit value=Update> </p> </form> </body>");
			
			dbcon.close();
			
		} catch (SQLException e) {
			while (e != null) {
                out.println("SQL Exception:  " + e.getMessage());
                e = e.getNextException();
            }
		}
		
		catch (Exception ex) {
			out.println("<HTML>" + "<HEAD><TITLE>" + "Search Error" + "</TITLE></HEAD>\n<BODY>"
                    + "<P>Error in doGet: " + ex.getMessage() + "</P></BODY></HTML>");
		}
		
		out.close();
	}
	
	public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		doGet(request, response);
	}
	
	public String urlFormat(String input) {
		String[] A = input.split("\\s+");
		
		if (A.length == 0) {
			return "";
		}
		
		StringBuilder sb = new StringBuilder(A[0]);
		for (int i = 1; i < A.length; i++) {
			sb.append("+" + A[i]);
		}
		
		return sb.toString();
	}
}