import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import java.net.*;
import java.util.*;
import java.sql.*;

import javax.naming.InitialContext;
import javax.naming.Context;
import javax.sql.DataSource;

//This servlet inserts a single movie and its related information into the mySQL database.

public class InsertMovie extends HttpServlet {
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
			
			String title = request.getParameter("title");
			String syear = request.getParameter("year");
			Integer year = null;
			
			try {
				year = Integer.parseInt(syear);
			} catch (Exception e) {
				out.println("Invalid input for the year.");
			}
			
			//Call the mySQL stored procedure to insert the movie into the mySQL database.
			
			String director = request.getParameter("director");
			String simfirstname = request.getParameter("simfirstname");
			String simlastname = request.getParameter("simlastname");
			String genre = request.getParameter("genre");
			String query = "{CALL add_movie(?,?,?,?,?,?)}";
			
			CallableStatement stmt = dbcon.prepareCall(query);
			
			stmt.setString(1, title);
			stmt.setInt(2, year);
			stmt.setString(3, director);
			stmt.setString(4, simfirstname);
			stmt.setString(5, simlastname);
			stmt.setString(6, genre);
			stmt.execute();
			
		} catch (SQLException e) {
			while (e != null) {
				out.println("SQL Exception:  " + e.getMessage());
                e = e.getNextException();
            }
			return;
        }

        catch (java.lang.Exception ex) {
            out.println("<HTML>" + "<HEAD><TITLE>" + "Search Error" + "</TITLE></HEAD>\n<BODY>"
            + "<P>Error in doGet: " + ex.getMessage() + "</P></BODY></HTML>");
			return;
        }
		
		out.println("<head>\n" +
			    "<style>\n" +
					"	body {\n" +
					"		background-image: url('https://previews.123rf.com/images/apostrophe/apostrophe1403/apostrophe140300013/26540708-bright-yellow-background-solid-color-primary-image-with-soft-vintage-grunge-background-texture-desig-Stock-Photo.jpg');\n" +
					"	}\n" +
					"	</style>\n" +
					"</head>\n");
		
		//Print out a confirmation page for the employee.
		
		out.println("<body>\n<h1 style='text-align:center'>A new movie has been entered successfully!</h1>\n");
		out.println("<p style='text-align:center'> <button type='button' onclick=window.location.assign('/Fablix/servlet/dashboarding')>" +
					"Back to the employee dashboard</button> </p>");
		out.println("<p style='text-align:center'> <button type='button' onclick=window.location.assign('/Fablix/servlet/Home')>" +
					"Back to the home page</button> </p></body>");
	}
	
	public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		doGet(request, response);
    }
}
