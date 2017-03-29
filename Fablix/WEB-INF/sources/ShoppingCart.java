import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import java.net.*;
import java.util.*;
import java.sql.*;
import java.text.*;

import javax.naming.InitialContext;
import javax.naming.Context;
import javax.sql.DataSource;

//This servlet keeps track of all the movies that the customer put in the cart during the session.

public class ShoppingCart extends HttpServlet {
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
			
			//Check if the customer is logged in or not.
			
			String inorout = null;
			URL inoroutURL = null;
			
			if (session.getAttribute("loggedIn") != null) {
				inorout = "Log Out";
				inoroutURL = new URL("http://52.37.235.2/Fablix/servlet/LogOut");
			} else {
				inorout = "Log In";
				inoroutURL = new URL("http://52.37.235.2/Fablix/LogInPage.html");
			}
			
			//Get all the movies in the cart during the current session.
			
			Map<Integer, Integer> moviesincart = new HashMap<Integer, Integer>();
			if (session.getAttribute("moviesincart") != null) {
				moviesincart = (Map<Integer, Integer>)session.getAttribute("moviesincart");
			} else {
				session.setAttribute("moviesincart", moviesincart);
			}
			
			//Change the quantity of a movie in the cart.
			
			if ((request.getParameter("movieid") != null) && (request.getParameter("quantity") != null)) {
				int movieid = Integer.parseInt(request.getParameter("movieid"));
				int quantity = Integer.parseInt(request.getParameter("quantity"));
				if (quantity <= 0) {
					moviesincart.remove(movieid);
				} else {
					moviesincart.put(movieid, quantity);
				}
			}
			
			//Remove a movie from the cart.
			
			if ((request.getParameter("removeid")) != null) {
				int removeid = Integer.parseInt(request.getParameter("removeid"));
				if (moviesincart.containsKey(removeid)) {
					moviesincart.remove(removeid);
				}
			}
			
			PreparedStatement moviestmt = dbcon.prepareStatement("SELECT * FROM movies WHERE id = ?");
			
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
						"</head>\n" +
						"<style>\n" +
						"	table, th, td {\n" +
						"		border: 1px solid black;\n" +
						"	}\n	" +
						"	body {\n" +
						"		background-image: url('https://previews.123rf.com/images/apostrophe/apostrophe1403/apostrophe140300013/26540708-bright-yellow-background-solid-color-primary-image-with-soft-vintage-grunge-background-texture-desig-Stock-Photo.jpg');\n" +
						"	}\n" +
						"</style>\n" +
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
						"<H1 style='clear:both;text-align:center'>Shopping Cart</H1>\n" +
						"<TABLE style='margin-left:auto;margin-right:auto'>\n" +
						"<TR> <TH>ID</TH> <TH>Title</TH> <TH>Year</TH> <TH>Director</TH> <TH>&nbsp</TH> <TH>&nbsp</TH> </TR>\n");
			
			//Display relevant information for each movie in the cart.
			
			for (Integer id : moviesincart.keySet()) {
				out.print("<TR>");
				moviestmt.setInt(1, id);
				ResultSet moviers = moviestmt.executeQuery();
				moviers.next();
				
				for (int i = 1; i < 5; i++) {
					out.print("<TD>" + moviers.getString(i) + "</TD>");
				}
				
				//Display the current quantity for each movie and allow the customer to change it.
				
				out.print("<TD>Current quantity: " + moviesincart.get(id) + "\n" +
						  "<form action='http://52.37.235.2/Fablix/servlet/ShoppingCart?movieid=" + id + "' method = 'post'>" +
						  "Set Quantity: <input type='number' name='quantity'><br> <p style='text-align:center'> <input type='submit' value='Update'></p></form></TD>");
				out.print("<TD><button type='button' onclick=window.location.assign('http://52.37.235.2/Fablix/servlet/ShoppingCart?removeid=" + id + "')>Remove item</button></TD></TR>");
				
				moviers.close();
			}
			
			moviestmt.close();
			
			out.println("</TABLE>");
			
			out.println("<p style='text-align:center'> <button type='button' onclick=window.location.assign('/Fablix/servlet/Checkout')>Checkout</button>\n");
			out.println("</body>");
						
			dbcon.close();
		} catch (SQLException e) {
			while (e != null) {
                out.println("SQL Exception:  " + e.getMessage());
                e = e.getNextException();
            }
		}
		
		catch (Exception ex) {
			out.println("<HTML>" + "<HEAD><TITLE>" + "Shopping Cart Error" + "</TITLE></HEAD>\n<BODY>"
                    + "<P>Error in doGet: " + ex.getMessage() + "</P></BODY></HTML>");
		}
		
		out.close();
	}
	
	public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		doGet(request, response);
	}
}