import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import java.net.*;
import java.util.*;
import java.sql.*;

import com.google.gson.*;

import javax.naming.InitialContext;
import javax.naming.Context;
import javax.sql.DataSource;

//This servlet carries out full text search on the title index of the movies table in the mySQL database and
//sends the result back to the autocomplete feature in the front end.

public class FullTextSearch extends HttpServlet {
	public void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		response.setContentType("application/json");
		PrintWriter out = response.getWriter();
		
		try {
			
			//Use connection pooling to access the mySQL database.
			
			Context initCtx = new InitialContext();
			
			Context envCtx = (Context) initCtx.lookup("java:comp/env");
			
			DataSource ds = (DataSource) envCtx.lookup("jdbc/TestDB");
			
			Connection dbcon = ds.getConnection();
			
			PreparedStatement stmt = dbcon.prepareStatement("SELECT title FROM movies WHERE MATCH (title) AGAINST (? IN BOOLEAN MODE)");
			String term = request.getParameter("term");
			String[] keywords = null;
			StringBuilder sb = new StringBuilder();
			List<String> res = new ArrayList<String>();
			
			//Split the input into keywords then carry out full text search.
			
			if (term != null) {
				keywords = term.split("\\s+");
				sb.append("+" + keywords[0]);
				
				for (int i = 1; i < keywords.length; i++) {
					sb.append(" +" + keywords[i]);
				}
				sb.append("*");
				stmt.setString(1, sb.toString());
				ResultSet rs = stmt.executeQuery();
				int j = 0;
				
				while ((rs.next()) && (j < 20)) {
					String temp = rs.getString(1);
					
					res.add(temp);
					j++;
				}
				
				rs.close();
			}
			
			stmt.close();
			dbcon.close();
			
			//Encode the result in JSON format then send it back to the autocomplete feature in the front end.
			
			String json = new Gson().toJson(res);
			out.write(json);

		} catch (Exception e) {
            out.println("Exception: " + e.getMessage());
		}
		
		out.close();
	}
	
	public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		doGet(request, response);
	}
}