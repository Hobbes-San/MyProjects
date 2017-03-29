import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import java.net.*;
import java.util.*;
import java.sql.*;

import javax.naming.InitialContext;
import javax.naming.Context;
import javax.sql.DataSource;

//This servlet displays information related to one particular movie.

public class SingleMovie extends HttpServlet {
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
			
			int movieid = Integer.parseInt(request.getParameter("movieid"));
			PreparedStatement moviestmt = dbcon.prepareStatement("SELECT * FROM movies WHERE id = ?");
			moviestmt.setInt(1, movieid);
			ResultSet moviers = moviestmt.executeQuery();
			moviers.next();
		
			out.println("<head>\n" +
						"	<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js'></script>\n" +
						"	<link rel='stylesheet' href='https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/themes/smoothness/jquery-ui.css'>\n" +
						"	<script src='https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js'></script>\n" +
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
						"		&nbsp|&nbsp <a href='/Fablix/servlet/Checkout'>Checkout</a>\n &nbsp|&nbsp <a href='/Fablix/dashboard.html'>Employee Dashboard</a>" +
						"	</form>\n" +
						"<H1 style='clear:both;text-align:center'>Movie Info</H1>\n" +
						"<TABLE style='margin-left:auto;margin-right:auto'>\n" +
						"<TR> <TH>ID</TH> <TH>Title</TH> <TH>Year</TH> <TH>Director</TH> <TH>Poster</TH> <TH>Trailer</TH> <TH>Genres</TH> <TH>Stars</TH> <TH>&nbsp</TH> </TR>");
			
			//Display relevant movie information
			
			for (int i = 1; i < 5; i++) {
				out.print("<TD>" + moviers.getString(i) + "</TD>");
			}
			
			try {
				URL posterURL = new URL(moviers.getString(5));
				out.print("<TD> <img src=" + posterURL + "> </TD>");
			} catch (Exception e) {
				out.print("<TD>N/A</TD>");
			}
			
			try {
				URL trailerURL = new URL(moviers.getString(6));
				out.print("<TD> <A HREF=" + trailerURL + ">" + "trailer" + "</A></TD>");
			} catch (Exception e) {
				out.print("<TD>N/A</TD>");
			}
			
			moviers.close();
			moviestmt.close();
			
			PreparedStatement gimstmt = dbcon.prepareStatement("SELECT genres.name FROM genres " +
										"INNER JOIN genres_in_movies ON genres.id = genres_in_movies.genre_id " +
										"WHERE genres_in_movies.movie_id = ?");
				
			PreparedStatement simstmt = dbcon.prepareStatement("SELECT stars.id, stars.first_name, stars.last_name FROM stars " +
										"INNER JOIN stars_in_movies ON stars.id = stars_in_movies.star_id " +
										"WHERE stars_in_movies.movie_id = ?");
			
			gimstmt.setInt(1, movieid);
			ResultSet gimrs = gimstmt.executeQuery();
			out.println("<TD> <UL>");
			
			//Display all the genres the movie belongs to.
			
			while(gimrs.next()) {
				out.print("<LI>" + gimrs.getString(1) + "</LI>");
			}
					
			out.println("</TD> </UL>");
			gimrs.close();
					
			simstmt.setInt(1, movieid);
			ResultSet simrs = simstmt.executeQuery();
						
			out.println("<TD> <UL>");
			
			//Display all the stars the movie features.
			
			while (simrs.next()) {
				int starid = simrs.getInt(1);
				URL starURL = new URL("http://52.37.235.2/Fablix/servlet/SingleStar?starid=" + starid);
				out.print("<LI> <A HREF=" + starURL + ">" + simrs.getString(2) + " " + simrs.getString(3) + "</A> </LI>");
			}
					
			out.println("</TD> </UL>");
			simrs.close();
			
			//Allow the customer to add the movie to the cart.
			
			out.println("<TD> <button type='button' onclick=window.location.assign('/Fablix/servlet/ShoppingCart?movieid=" + movieid + "&quantity=1')>Add to shopping cart</button> </TD>");
			
			out.println("</TR>");
		
			out.println("</TABLE>");
			gimstmt.close();
			simstmt.close();
			
			dbcon.close();
			
		} catch (SQLException e) {
			while (e != null) {
                out.println("SQL Exception:  " + e.getMessage());
                e = e.getNextException();
            }
		}
		
		catch (Exception ex) {
			out.println("<HTML>" + "<HEAD><TITLE>" + "SingleMovie Error" + "</TITLE></HEAD>\n<BODY>"
                    + "<P>Error in doGet: " + ex.getMessage() + "</P></BODY></HTML>");
		}
		
		out.close();
	}
	
	public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		doGet(request, response);
	}
}