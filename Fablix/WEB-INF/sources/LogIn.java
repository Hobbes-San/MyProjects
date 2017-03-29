import java.io.*;
import java.net.*;
import java.sql.*;
import java.text.*;
import java.util.*;
import javax.servlet.*;
import javax.servlet.http.*;

import javax.naming.InitialContext;
import javax.naming.Context;
import javax.sql.DataSource;

//This servlet allows customers to log in.

public class LogIn extends HttpServlet {
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
			
			String email = request.getParameter("email");
			String password = request.getParameter("password");
			String search = "SELECT * FROM customers WHERE email = ? AND password = ?";
			
			PreparedStatement stmt = dbcon.prepareStatement(search);
			stmt.setString(1, email);
			stmt.setString(2, password);
			ResultSet rs = stmt.executeQuery();
			
			//Check with the mySQL database to see if the customer information is valid.
			//If it is valid, set the status to logged in and go to the home page.
			//If not, then redirect the customer back to the log in page.
			
			if (rs.next()) {
				session.setAttribute("loggedIn", true);
				response.sendRedirect("/Fablix/servlet/Home");
			} else {
				out.println("<head>\n" +
							"	body {\n" +
							"		background-image: url('https://previews.123rf.com/images/apostrophe/apostrophe1403/apostrophe140300013/26540708-bright-yellow-background-solid-color-primary-image-with-soft-vintage-grunge-background-texture-desig-Stock-Photo.jpg');\n" +
							"	}\n" +
							"	</style>\n" +
							"</head>\n");
				out.println("<script>alert('Wrong email or password. Please try again.')</script>\n");
				out.println("<body><p style='clear:both;text-align:center'> <button type='button' onclick=window.location.assign('/Fablix/LogInPage.html')>" +
							"Back to the log in page</button> </p></body>");
			}
			
			rs.close();
            stmt.close();
            dbcon.close();
			
		} catch (SQLException e) {
			while (e != null) {
                out.println("SQL Exception:  " + e.getMessage());
                e = e.getNextException();
            }
		}
		
		catch (Exception ex) {
            out.println("<HTML>" + "<HEAD><TITLE>" + "LogIn Error" + "</TITLE></HEAD>\n<BODY>"
                    + "<P>Error in doGet: " + ex.getMessage() + "</P></BODY></HTML>");
        }
        out.close();
	}
	
	public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		doGet(request, response);
	}
}
