import java.io.IOException;
import java.io.*;
import java.net.*;
import java.util.*;

//This class wraps all the information about a star into a convenient bundle.

public class Star {
	private String firstname;
	private String lastname;
	
	private String dob;
	
	public void printInfo() {
		System.out.println("First Name: " + firstname + " Last Name: " + lastname + " Dob: " + dob);
	}
	
	public void setFirstName(String firstname) {
		this.firstname = firstname;
	}
	
	public void setLastName(String lastname) {
		this.lastname = lastname;
	}
	
	public void setDob(String dob) {
		this.dob = dob;
	}
	
	public String getFirstName() {
		return firstname;
	}
	
	public String getLastName() {
		return lastname;
	}
	
	public String getDob() {
		return dob;
	}
}