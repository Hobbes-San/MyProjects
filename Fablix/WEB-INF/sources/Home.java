import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import java.net.*;
import java.util.*;
import java.sql.*;

import javax.naming.InitialContext;
import javax.naming.Context;
import javax.sql.DataSource;

//This servlet is the home page.

public class Home extends HttpServlet {
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
			
			//Check whether the customer is currently logged in or not.
			
			String inorout = null;
			URL inoroutURL = null;
			
			if (session.getAttribute("loggedIn") != null) {
				inorout = "Log Out";
				inoroutURL = new URL("http://52.37.235.2/Fablix/servlet/LogOut");
			} else {
				inorout = "Log In";
				inoroutURL = new URL("http://52.37.235.2/Fablix/LogInPage.html");
			}
			
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
						"	<style>\n" +
						"	body {\n" +
						"		background-image: url('https://previews.123rf.com/images/apostrophe/apostrophe1403/apostrophe140300013/26540708-bright-yellow-background-solid-color-primary-image-with-soft-vintage-grunge-background-texture-desig-Stock-Photo.jpg');\n" +
						"	}\n" +
						"	</style>\n" +
						"</head>\n" +
						"<body>\n" +
						
						//Default format for the website.
						
						"	<p style='float:left;font-size:40px;margin-top:10px;margin-left:30px'>Fablix... One stop shop for your favorite flix!</p>\n" +
						"	<form action='/Fablix/servlet/Searching' style='float:right;margin-top:20px;margin-right:30px' name='titleSearch' method='get'>\n" +
						"		<input type='text' id='title' name='title' placeholder='Search for a movie...'>\n" +
						"		<input type='submit' value='Search'><br>\n" +
						"		<a href='/Fablix/servlet/Home'>Home</a> &nbsp|&nbsp <a href='/Fablix/Search.html'>Advanced Search</a>\n " +
						"		&nbsp|&nbsp <a href='" + inoroutURL + "'>" + inorout + "</a> &nbsp|&nbsp <a href='/Fablix/servlet/ShoppingCart'>My Cart</a>\n " + 
						"		&nbsp|&nbsp <a href='/Fablix/servlet/Checkout'>Checkout</a> &nbsp|&nbsp <a href='/Fablix/dashboard.html'>Employee Dashboard</a>\n" +
						"	</form>\n" +
						"	<p style='clear:both;font-size:30px;margin-left:30px;text-align:center'>Guided Search</p>");

			out.println("<p style='float:left;max-width:150px;margin-left:400px;line-height: 200%'>\n" +
						"<span>Browse by movie title</span><br>\n");
			
			//Browse for movie titles alphabetically.
			
			for (int i = 0; i < 10; i++) {
				URL numURL = new URL("http://52.37.235.2/Fablix/servlet/Searching" +
									 "?firstorgenre=byfirst&first=" + i);
				out.println("<a href=" + numURL + ">" + i + "&nbsp</a>");
			}
				
			for (char alph = 'A'; alph <= 'Z'; alph++) {
				URL alphURL = new URL("http://52.37.235.2/Fablix/servlet/Searching" +
									  "?firstorgenre=byfirst&first=" + alph);
				out.println("<a href=" + alphURL + ">" + alph + "&nbsp</a>");
			}
				
			Statement allgenrestmt = dbcon.createStatement();
			ResultSet allgenrers = allgenrestmt.executeQuery("SELECT * FROM genres");
			
			out.println("<p style='float:right;max-width:400px;margin-right:300px;line-height: 200%'>\n" +
						"<span>Browse by movie genre</span><br>\n");
			
			int i = 0;
			
			//Browse for movie titles by genre.
				
			while (allgenrers.next()) {
				StringBuilder sbURL = new StringBuilder("http://52.37.235.2/Fablix/servlet/Searching" +
														"?firstorgenre=bygenre&genreid=" + allgenrers.getInt(1));
				URL genreURL = new URL(sbURL.toString());
				out.println("<a href="+ genreURL + ">" + allgenrers.getString(2) + "</a>&nbsp&nbsp\n");
				
			}
				
			allgenrers.close();
			allgenrestmt.close();
				
			out.println("</body>");
			dbcon.close();
			
		} catch (SQLException e) {
			while (e != null) {
                out.println("SQL Exception:  " + e.getMessage());
                e = e.getNextException();
            }
		}
		
		catch (java.lang.Exception ex) {
			out.println("<HTML>" + "<HEAD><TITLE>" + "Search Error" + "</TITLE></HEAD>\n<BODY>"
                    + "<P>Error in doGet: " + ex.getMessage() + "</P></BODY></HTML>");
		}
		
		out.close();
	}
	
	public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		doGet(request, response);
	}
}