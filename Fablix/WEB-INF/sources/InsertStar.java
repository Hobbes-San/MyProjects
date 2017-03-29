import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import java.net.*;
import java.util.*;
import java.sql.*;

import javax.naming.InitialContext;
import javax.naming.Context;
import javax.sql.DataSource;

//This servlet inserts a single star and its related information into the mySQL database.

public class InsertStar extends HttpServlet {
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
			
			String firstname = request.getParameter("firstname");
			String lastname = request.getParameter("lastname");
		
			String insert = "INSERT INTO stars (first_name,last_name) VALUES (?,?)";
			PreparedStatement stmt = dbcon.prepareStatement(insert);
			stmt.setString(1, firstname);
			stmt.setString(2, lastname);
			stmt.executeUpdate();
			
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
		
		out.println("<body>\n<h1 style='text-align:center'>A new star has been entered successfully!</h1>\n");
		out.println("<p style='text-align:center'> <button type='button' onclick=window.location.assign('/Fablix/servlet/dashboarding')>" +
					"Back to the employee dashboard</button> </p>");
		out.println("<p style='text-align:center'> <button type='button' onclick=window.location.assign('/Fablix/servlet/Home')>" +
					"Back to the home page</button> </p></body>");
	}
	
	public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		doGet(request, response);
    }
}
