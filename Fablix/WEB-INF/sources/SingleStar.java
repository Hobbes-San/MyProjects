import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import java.net.*;
import java.util.*;
import java.sql.*;

import javax.naming.InitialContext;
import javax.naming.Context;
import javax.sql.DataSource;

//This servlet displays information related to one particular star.

public class SingleStar extends HttpServlet {
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
			
			int starid = Integer.parseInt(request.getParameter("starid"));
			PreparedStatement starstmt = dbcon.prepareStatement("SELECT * FROM stars WHERE id = ?");
			starstmt.setInt(1, starid);
			ResultSet starinfors = starstmt.executeQuery();
			starinfors.next();
			String fullName = starinfors.getString(2) + " " + starinfors.getString(3);
		
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
						
						//Default format for the website.
						
						"<BODY>\n" +
						"	<p style='float:left;font-size:40px;margin-top:10px;margin-left:30px'>Fablix... One stop shop for your favorite flix!</p>\n" +
						"	<form action='/Fablix/servlet/Searching' style='float:right;margin-top:20px;margin-right:30px' name='titleSearch' method='get'>\n" +
						"		<input type='text' id='title' name='title' placeholder='Search for a movie...'>\n" +
						"		<input type='submit' value='Search'><br>\n" +
						"		<a href='/Fablix/servlet/Home'>Home</a> &nbsp|&nbsp <a href='/Fablix/Search.html'>Advanced Search</a>\n " +
						"		&nbsp|&nbsp <a href='" + inoroutURL + "'>" + inorout + "</a> &nbsp|&nbsp <a href='/Fablix/servlet/ShoppingCart'>My Cart</a>\n " + 
						"		&nbsp|&nbsp <a href='/Fablix/servlet/Checkout'>Checkout</a>\n &nbsp|&nbsp <a href='/Fablix/dashboard.html'>Employee Dashboard</a>" +
						"	</form>\n" +
						"<H1 style='clear:both;text-align:center'>Star Info</H1>\n" +
						"<TABLE style='margin-left:auto;margin-right:auto'>\n" +
						"<TR> <TH>ID</TH> <TH>Name</TH> <TH>Date of birth</TH> <TH>Picture</TH> <TH>Movies featuring this star</TH> <TR>");
			
			//Display relevant information related to the star.
			
			out.print("<TD>" + starinfors.getString(1) + "</TD>");
			out.print("<TD>" + fullName + "</TD>");
			
			String dob = starinfors.getString(4);
			
			if (!((dob == null) || (dob.equals("")))) {
				out.print("<TD>" + dob + "</TD>");
			} else {
				out.print("<TD>N/A</TD>");
			}
			
			String picture = starinfors.getString(5);
			
			try {
				URL pictureURL = new URL(picture);
				out.print("<TD> <img src=" + pictureURL + "> </TD>");
			} catch (Exception e) {
				out.print("<TD>N/A</TD>");
			}
			
			starstmt.close();
			starinfors.close();
			
			PreparedStatement moviestmt = dbcon.prepareStatement("SELECT movies.title, movies.id FROM movies " +
										  "INNER JOIN stars_in_movies ON movies.id = stars_in_movies.movie_id " +
										  "WHERE stars_in_movies.star_id = ?");
			
			moviestmt.setInt(1, starid);
			ResultSet moviers = moviestmt.executeQuery();

			out.println("<TD> <UL>");
			
			//Display all the movies that feature the given star.
			
			while (moviers.next()) {
				int movieid = moviers.getInt(2);
				URL movieURL = new URL("http://52.37.235.2/Fablix/servlet/SingleMovie?movieid=" + movieid);
				out.print("<LI> <A HREF=" + movieURL + ">" + moviers.getString(1) + "</A> </LI>");
			}
			
			moviers.close();
			moviestmt.close();
			
			out.println("</TD> </UL>");
			out.println("</TR>");
		
			out.println("</TABLE> </BODY>");
			
			dbcon.close();
			
		} catch (SQLException e) {
			while (e != null) {
                out.println("SQL Exception:  " + e.getMessage());
                e = e.getNextException();
            }
		}
		
		catch (Exception ex) {
			out.println("<HTML>" + "<HEAD><TITLE>" + "SingleStar Error" + "</TITLE></HEAD>\n<BODY>"
                    + "<P>Error in doGet: " + ex.getMessage() + "</P></BODY></HTML>");
		}
		
		out.close();
	}
	
	public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		doGet(request, response);
	}
}