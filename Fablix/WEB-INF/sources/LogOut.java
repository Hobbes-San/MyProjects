import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import java.net.*;
import java.util.*;
import java.sql.*;
import java.text.*;

//This servlet allows customers to log out.

public class LogOut extends HttpServlet {
	public void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		
		//Destroy the current customer session and redirect him/her to the home page.
		
		request.getSession().invalidate();
		response.sendRedirect("/Fablix/servlet/Home");
	}
	
	public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		doGet(request, response);
	}
}