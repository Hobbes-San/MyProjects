import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import java.net.*;
import java.util.*;
import java.sql.*;

import javax.naming.InitialContext;
import javax.naming.Context;
import javax.sql.DataSource;

//This servlet allows an employee to log in to the dashboard.

public class dashboardLogIn extends HttpServlet {
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
			
			String email = request.getParameter("email");
			String password = request.getParameter("password");
			String search = "SELECT * FROM employees WHERE email = ? AND password = ?";
			PreparedStatement stmt = dbcon.prepareStatement(search);
			stmt.setString(1, email);
			stmt.setString(2, password);
			
			ResultSet rs = stmt.executeQuery();
			
			//Check with the mySQL database to see if the employee information is valid.
			//If it is valid, allow access to the dashboard.
			//If not, then redirect the user back to the employee log in page.
			
			if (rs.next()) {
				response.sendRedirect("/Fablix/servlet/dashboarding");
			} else {
				out.println("<script>alert('Wrong email or password. Please try again.');\n" +
							"window.location.assign('/Fablix/dashboard.html');</script>");
			}
				
			
		} catch (SQLException e) {
                while (e != null) {
					out.println("SQL Exception:  " + e.getMessage());
					e = e.getNextException();
            	}
        }

        catch (java.lang.Exception ex) {
			out.println("<HTML>" + "<HEAD><TITLE>" + "Search Error" + "</TITLE></HEAD>\n<BODY>" +
					    "<P>Error in doGet: " + ex.getMessage() + "</P></BODY></HTML>");
        }
	}
		
	public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
                doGet(request, response);
    }
}

