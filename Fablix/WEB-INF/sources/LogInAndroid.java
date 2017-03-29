import java.io.*;
import java.net.*;
import java.sql.*;
import java.text.*;
import java.util.*;
import javax.servlet.*;
import javax.servlet.http.*;
import com.google.gson.*;

import javax.naming.InitialContext;
import javax.naming.Context;
import javax.sql.DataSource;

//This servlet allows customers to log in to the android app.

public class LogInAndroid extends HttpServlet {
	public void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		
		response.setContentType("application/json");
		Writer out = response.getWriter();
		
		try {
			
			//Use connection pooling to access the mySQL database.
			
			Context initCtx = new InitialContext();
			
			Context envCtx = (Context) initCtx.lookup("java:comp/env");
			
			DataSource ds = (DataSource) envCtx.lookup("jdbc/TestDB");
			
			Connection dbcon = ds.getConnection();
			
			String email = request.getParameter("email");
			String password = request.getParameter("password");
			String search = "SELECT * FROM customers WHERE email = ? AND password = ?";
			
			PreparedStatement stmt = dbcon.prepareStatement(search);
			stmt.setString(1, email);
			stmt.setString(2, password);
			ResultSet rs = stmt.executeQuery();
			
			//Check with the mySQL database to see if the customer information is valid.
			//Send the result back to the android app front end.
			
			if (rs.next()) {
				out.write("{'info': 'success'}");
			} else {
				out.write("{'info': 'fail'}");
			}
			
			rs.close();
            stmt.close();
            dbcon.close();
		} catch (Exception e) {
			System.out.println("Exception occured.");
		}
		
		out.close();
		
	}
	
	public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		doGet(request, response);
	}
}
