import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import java.net.*;
import java.util.*;
import java.sql.*;
import java.text.*;
import java.time.LocalDateTime;

import javax.naming.InitialContext;
import javax.naming.Context;
import javax.sql.DataSource;

//This servlet allows customers to check out by entering valid credit card information.

public class Checkout extends HttpServlet {
	
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
			
			String ccid = request.getParameter("ccid");
			String xdate = request.getParameter("xdate");
			String firstname = request.getParameter("firstname");
			String lastname = request.getParameter("lastname");
			
			boolean infosent = false;
			
			//Check whether or not the customer has input credit card information.
			
			if ((ccid != null) && (xdate != null) && (firstname != null) && (lastname != null)) {
				infosent = true;
				
				ccid = ccid.trim();
				xdate = xdate.trim();
				firstname = firstname.trim();
				lastname = lastname.trim();
			}
			
			
			//Access all the movies in the customer's cart during his/her current session.
			
			Map<Integer, Integer> moviesincart = (Map<Integer, Integer>)session.getAttribute("moviesincart");
			
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
							"	</form>\n");
			
			//Error message in case the cart is empty.
			
			if ((moviesincart == null) || moviesincart.isEmpty()) {
				out.println("<script>alert('The shopping cart is currently empty. Please add items to the cart before checking out.');</script>\n");
				out.println("<p style='clear:both;text-align:center'> <button type='button' onclick=window.location.assign('/Fablix/servlet/Home')>" +
							"Back to the home page</button> </p>");
			
			//Error message in case the customer is not currently logged in.
			
			} else if (session.getAttribute("loggedIn") == null) {
				out.println("<script>alert('You are not logged in. Please log in before checking out');</script>\n");
				out.println("<p style='clear:both;text-align:center'> <button type='button' onclick=window.location.assign('/Fablix/servlet/Home')>" +
							"Back to the home page</button> </p>");
			
			//Ask the customer for credit card information in case he/she has not input the information yet.
			
			} else if (!infosent) {
				out.println("<h1 style='clear:both;text-align:center'>Please enter your credit card information</h1>\n" +
							"<form style='text-align:center' action ='/Fablix/servlet/Checkout' method = 'post'>\n" +
							"Credit Card Number:\n" +
							"<input type='number' name='ccid'><br>\n" +
							"Expiration Date:\n" +
							"<input type='date' name='xdate'><br>\n" +
							"First Name:\n" +
							"<input type='text' name='firstname'><br>\n" +
							"Last Name:\n" +
							"<input type='text' name='lastname'><br>\n" +
							"<center>\n" +
							"	<input type='submit' value='submit'>\n" +
							"</center>" +
							"</form>");
			} else {
				
				PreparedStatement cardstmt = dbcon.prepareStatement("SELECT * FROM creditcards WHERE id = ? AND first_name = ? AND last_name = ? AND expiration = ?");
				
				cardstmt.setString(1, ccid);
				cardstmt.setString(2, firstname);
				cardstmt.setString(3, lastname);
				cardstmt.setString(4, xdate);
				
				ResultSet cardrs = cardstmt.executeQuery();
				
				//Check with the mySQL database to see if the credit card information is valid.
				
				if (cardrs.next()) {
					PreparedStatement customerstmt = dbcon.prepareStatement("SELECT id FROM customers WHERE first_name = ? AND last_name = ? AND cc_id = ?");
					customerstmt.setString(1, firstname);
					customerstmt.setString(2, lastname);
					customerstmt.setString(3, ccid);
					
					ResultSet customerrs = customerstmt.executeQuery();
					customerrs.next();
					
					int customerid = customerrs.getInt(1);
					LocalDateTime now = LocalDateTime.now();
					String month = null;
					
					if (now.getMonthValue() < 10) {
						month = "0" + now.getMonthValue();
					} else {
						month = Integer.toString(now.getMonthValue());
					}
					String date = now.getYear() + "-" + month + "-" + now.getDayOfMonth();
					
					customerrs.close();
					customerstmt.close();
					
					//Get the customer information and prepare to insert the sales record into the mySQL database.
					
					PreparedStatement insertstmt = dbcon.prepareStatement("INSERT INTO sales (customer_id, movie_id, sale_date) VALUES (?,?,?)");
					PreparedStatement confirmstmt = dbcon.prepareStatement("SELECT title from movies WHERE id = ?");
					
					out.println("<style>\n" +
								"table, th, td {\n" +
								"	border: 1px solid black;\n" +
								"}\n	" +
								"</style>\n" +
								"<H1 style='clear:both;text-align:center'>Confirmation Page</H1>\n" +
								"<p style='text-align:center'>Your transaction has been completed successfully!</p>\n" +
								"<p style='text-align:center'>You have bought</p>");
					
					//Print out confirmation page for the customer.
					
					for (Integer id : moviesincart.keySet()) {
						insertstmt.setInt(1, customerid);
						insertstmt.setInt(2, id);
						insertstmt.setString(3, date);
						insertstmt.executeUpdate();
						
						confirmstmt.setInt(1, id);
						ResultSet confirmrs = confirmstmt.executeQuery();
						confirmrs.next();
						out.println("<p style='text-align:center'>" + moviesincart.get(id) + " copies of " + confirmrs.getString(1) + "</p>");
						confirmrs.close();
					}
					
					insertstmt.close();
					confirmstmt.close();
					
				} else {
					
					//Error message in case the credit card information is wrong.
					
					out.println("<script>alert('Wrong credit card information. Please try again.');</script>\n");
					out.println("<p style='clear:both;text-align:center'> <button type='button' onclick=window.location.assign('/Fablix/servlet/Checkout')>" +
								"Back to the Checkout page</button> </p>");
				}
				
				out.println("</BODY>");
				
				cardrs.close();
				cardstmt.close();
				
			}
			
			dbcon.close();
			
		} catch (SQLException e) {
			while (e != null) {
                out.println("SQL Exception: " + e.getMessage());
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
}