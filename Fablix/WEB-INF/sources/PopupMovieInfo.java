import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import java.net.*;
import java.util.*;
import java.sql.*;

import javax.naming.InitialContext;
import javax.naming.Context;
import javax.sql.DataSource;

//This servlet queries the mySQL database to get movie information to be displayed in a pop-up.

public class PopupMovieInfo extends HttpServlet {
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
			
			int movieid = Integer.parseInt(request.getParameter("movieid"));
			
			PreparedStatement moviestmt = dbcon.prepareStatement("SELECT * FROM movies WHERE id = ?");
			moviestmt.setInt(1, movieid);
			ResultSet moviers = moviestmt.executeQuery();
			
			//Get all the revelant movie information.
			
			moviers.next();
			int year = moviers.getInt(3);
			
			out.println("<style>\n" +
						"table, th, td {\n" +
						"	border: 1px solid black;\n" +
						"}\n	" +
						"</style>\n" +
						"<table style='margin-left:auto;margin-right:auto'> <tr> <th>Poster</th> <th>Stars</th> <th>Year</th> <th>&nbsp</th> </tr>\n" +
						"<tr>\n");
			try {
				URL posterURL = new URL(moviers.getString(5));
				out.print("<TD> <img src='" + posterURL + "' style='width:150px;height:250px'> </TD>\n");
			} catch (Exception e) {
				out.print("<TD>N/A</TD>");
			}
			
			PreparedStatement simstmt = dbcon.prepareStatement("SELECT stars.id, stars.first_name, stars.last_name FROM stars " +
										"INNER JOIN stars_in_movies ON stars.id = stars_in_movies.star_id " +
										"WHERE stars_in_movies.movie_id = ?");
			
			simstmt.setInt(1, movieid);
			ResultSet simrs = simstmt.executeQuery();
			
			out.println("<td> <ul>\n");
					
			while (simrs.next()) {
				int starid = simrs.getInt(1);
				URL starURL = new URL("http://52.37.235.2/Fablix/servlet/SingleStar?starid=" + starid);
				out.print("<LI> <A HREF=" + starURL + ">" + simrs.getString(2) + " " + simrs.getString(3) + "</A> </LI>");
			}
					
			simrs.close();
			simstmt.close();
			
			//Allows the customer to add movie to the cart.
			
			out.println("</ul> </td>\n <td>" + year + "</td>\n");
			out.println("<TD> <a href='/Fablix/servlet/ShoppingCart?movieid=" + movieid + "&quantity=1'>Add to shopping cart</a> </TD>\n");
				
			out.println("</TR> </table>");
			
			moviers.close();
			moviestmt.close();
			dbcon.close();
		
		} catch (Exception ex) {
			out.println("<HTML>" + "<HEAD><TITLE>" + "Search Error" + "</TITLE></HEAD>\n<BODY>"
                    + "<P>Error in doGet: " + ex.getMessage() + "</P></BODY></HTML>");
		}
		
		out.close();
	}
	
	public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		doGet(request, response);
	}
}