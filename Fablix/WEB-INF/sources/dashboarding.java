import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import java.net.*;
import java.util.*;
import java.sql.*;

import javax.naming.InitialContext;
import javax.naming.Context;
import javax.sql.DataSource;

//This servlet allows employees to manually enter data into the mySQL database.

public class dashboarding extends HttpServlet {
	public void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

            response.setContentType("text/html");
            PrintWriter out = response.getWriter();

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
			
				String insertstar = request.getParameter("insertstar");
				String insertmovie = request.getParameter("insertmovie");
				
				out.println("<head>\n" +
					    "<style>\n" +
							"	body {\n" +
							"		background-image: url('https://previews.123rf.com/images/apostrophe/apostrophe1403/apostrophe140300013/26540708-bright-yellow-background-solid-color-primary-image-with-soft-vintage-grunge-background-texture-desig-Stock-Photo.jpg');\n" +
							"	}\n" +
							"	</style>\n" +
							"</head>\n");
				
				//Ask for star information to be put in.
				
				if (insertstar != null && insertstar.equals("true")) {
					out.println("<body>\n" +
								"<h1 style='text-align:center'>Insert a star</h1>\n" +
								"<form action='/Fablix/servlet/InsertStar' method='post'>\n" +
								"<p style='text-align:center'>" +
								"First Name: <input type='text' name='firstname'><br>\n" +
								"Last Name: <input type='text' name='lastname'><br>\n" +
								"<input type='submit' value='submit'>" +
								"</p></form></body></html>");
								
				//Ask for movie information to be put in.
				
				} else if (insertmovie != null && insertmovie.equals("true")) {
					out.println("<body>\n" +
								"<h1 style='text-align:center'>Insert a movie</h1>\n" +
								"<form action='/Fablix/servlet/InsertMovie' method='post'>\n" +
								"<p style='text-align:center'>" +
								"Title: <input type='text' name='title'><br>\n" +
								"Year: <input type='number' name='year'><br>\n" +
								"Director: <input type='text' name='director'><br>\n" +
								"First Name of the Featured Star: <input type='text' name='simfirstname'><br>\n" +
								"Last Name of the Featured Star: <input type='text' name='simlastname'><br>\n" +
								"Genre: <input type='text' name='genre'><br>\n" +
								"<input type='submit' value='submit'>\n" +
								"</p></form></body></html>");
								
				//Ask the employee to choose to enter either a star or a movie into the mySQL database.
				
				} else {
					out.println("<body><h1 style='text-align:center'>Choose one of the options below</h1><p style='text-align:center'>\n" +
								"<button type='button' onclick=window.location.assign('/Fablix/servlet/dashboarding?insertstar=true')>Insert Star</button>&nbsp" +
								"<button type='button' onclick=window.location.assign('/Fablix/servlet/dashboarding?insertmovie=true')>Insert Movie</button>" +
								"</p>\n");
					out.println("<p style='text-align:center'> <button type='button' onclick=window.location.assign('/Fablix/servlet/dashboarding')>" +
								"Back to the employee dashboard</button> </p>");
					out.println("<p style='text-align:center'> <button type='button' onclick=window.location.assign('/Fablix/servlet/Home')>" +
								"Back to the home page</button> </p></body>");
				}
			
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
        }

        public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
                doGet(request, response);
        }
}
