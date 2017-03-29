import java.io.IOException;
import java.io.*;
import java.net.*;
import java.util.*;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;

import org.xml.sax.Attributes;
import org.xml.sax.SAXException;

import org.xml.sax.helpers.DefaultHandler;

//This java file uses SAX to parse multiple XML files containing movie/star data and
//save the information into an ArrayList and a HashMap.

public class MoviedbParser extends DefaultHandler {
	
	//The variables with temp as part of their name are placeholders.
	
	private String temp;
	private Film tempFilm;
	private Star tempStar;
	private String tempDirector;
	
	//filmid variable is a convenient key in the XML file to facilitate lookups.
	
	private String filmid;
	private boolean checkDirector;
	
	//The following two will contain all the information from XML file.
	
	private Map<String,Film> filmTable;
	private List<Star> starList;
	
	public MoviedbParser() {
		filmTable = new HashMap<>();
		starList = new ArrayList<>();
		checkDirector = false;
	}
	
	public List<Star> getStarList() {
		return starList;
	}
	
	public Map<String,Film> getFilmTable() {
		return filmTable;
	}
	
	public void parseDocument() {
		
		//get a factory
		SAXParserFactory spf = SAXParserFactory.newInstance();
		try {
		
			//get a new instance of parser
			SAXParser sp = spf.newSAXParser();
			
			//parse the file and also register this class for call backs
			sp.parse("../sources/actors63.xml", this);
			sp.parse("../sources/mains243.xml", this);
			sp.parse("../sources/casts124.xml", this);
			
		} catch(SAXException se) {
			se.printStackTrace();
		} catch(ParserConfigurationException pce) {
			pce.printStackTrace();
		} catch (IOException ie) {
			ie.printStackTrace();
		}
	}
	
	//Helper functions to parse star names.
	
	public String parseFirstName(String s) {
		int i = 0;
		while (i < s.length()) {
			if (s.charAt(i) == ' ') {
				break;
			}
			i++;
		}
		return s.substring(0, i);
	}
	
	public String parseLastName(String s) {
		int i = s.length()-1;
		while (i >= 0) {
			if (s.charAt(i) == ' ') {
				break;
			}
			i--;
		}
		return s.substring(i+1);
	}
	
	//Override the startElement method.
	
	public void startElement(String uri, String localName, String qName, Attributes attributes) throws SAXException {
		temp = "";
		
		//Reset the director.
		
		if (qName.equalsIgnoreCase("director")) {
			checkDirector = true;
			tempDirector = null;
			
		}
		
		//Reset the star featured in a given film.
		
		if (qName.equalsIgnoreCase("f")) {
			tempStar = new Star();
			filmid = null;
		}
		
		//Reset the film.
		
		if ((qName.equalsIgnoreCase("fid")) || (qName.equalsIgnoreCase("filmed"))) {
			tempFilm = new Film();
			filmid = null;
		}
		
		//Reset the star.
		
		if (qName.equalsIgnoreCase("actor")) {
			tempStar = new Star();
		}
	}
	
	public void characters(char[] ch, int start, int length) throws SAXException {
		temp = (new String(ch, start, length)).trim();
	}
	
	//Override the endElement method.
	
	public void endElement(String uri, String localName, String qName) throws SAXException {
		if (((qName.equalsIgnoreCase("dirname")) || (qName.equalsIgnoreCase("dirn"))) && checkDirector && !(temp.equals(""))) {
			tempDirector = temp;
			
		} else if (((qName.equalsIgnoreCase("fid")) || (qName.equalsIgnoreCase("filmed"))) && !(temp.equals(""))) {
			filmid = temp;
			
		} else if ((qName.equalsIgnoreCase("t")) && !(temp.equals(""))) {
			tempFilm.setTitle(temp);
			
		} else if ((qName.equalsIgnoreCase("year")) && !(temp.equals(""))) {
			try {
				tempFilm.setYear(Integer.parseInt(temp));
			} catch (Exception e) {
				tempFilm.setYear(null);
			}
			
		} else if ((qName.equalsIgnoreCase("cat")) && !(temp.equals(""))) {
			tempFilm.getGenres().add(temp);
			
		} else if (qName.equalsIgnoreCase("director")) {
			checkDirector = false;
		
		//Collect title, year, director information for the movie and if the information is valid,
		//save it into the HashMap with the film ID in the XML file as the key for easy access in the future.
		
		} else if (qName.equalsIgnoreCase("cats")) {
			tempFilm.setDirector(tempDirector);
			
			String title = tempFilm.getTitle();
			Integer year = tempFilm.getYear();
			String director = tempFilm.getDirector();
			
			if ((filmid == null) || (title == null) || (year == null) || (director == null)) {
				System.out.println("Error in processing the movie with Film ID: " + filmid + " Title: " + title + " Year: " + year + " Director: " + director);
				
			} else {
				filmTable.put(filmid, tempFilm);
				
			}
			
		} else if ((qName.equalsIgnoreCase("stagename")) && !(temp.equals(""))) {
			String firstname = parseFirstName(temp);
			String lastname = parseLastName(temp);
			
			if ((firstname != null) && (lastname != null) && firstname.equals(lastname)) {
				firstname = "";
			}
			
			tempStar.setFirstName(firstname);
			tempStar.setLastName(lastname);
			
		} else if (qName.equalsIgnoreCase("dob") && !(temp.equals(""))) {
			tempStar.setDob(temp);
		
		//Collect first name, last name, and date of birth information for the star and if information is valid,
		//save it into the ArrayList to be processed.
		
		} else if (qName.equalsIgnoreCase("dod")) {
			String firstname = tempStar.getFirstName();
			String lastname = tempStar.getLastName();
			String dob = tempStar.getDob();
			
			if ((firstname == null) || (lastname == null)) {
				System.out.println("Error in processing the star with First Name: " + firstname + " Last Name: " + lastname + " Dob: " + dob);
			} else {
				starList.add(tempStar);
			}
			
		} else if (qName.equalsIgnoreCase("f") && !(temp.equals(""))) {
			filmid = temp;
			
		} else if (qName.equalsIgnoreCase("a") && !(temp.equals(""))) {
			String firstname = parseFirstName(temp);
			String lastname = parseLastName(temp);
			
			if ((firstname != null) && (lastname != null) && firstname.equals(lastname)) {
				firstname = "";
			}
			
			tempStar.setFirstName(firstname);
			tempStar.setLastName(lastname);
		
		//Collect all the stars featured in a given movie and if information is valid,
		//save it to the star list attribute of the Film object.
		
		} else if (qName.equalsIgnoreCase("p")) {
			String firstname = tempStar.getFirstName();
			String lastname = tempStar.getLastName();
			
			if ((firstname == null) || (lastname == null) || (filmid == null)) {
				System.out.println("Error in processing a star with First Name: " + firstname + " Last Name: " + lastname + "in the movie with Film ID: " + filmid);
			} else {
				if (!(((firstname.equals("s")) && (lastname.equals("a"))) || (lastname.equals("sa")))) {
					Film tFilm = filmTable.get(filmid);
					if (tFilm != null) {
						tFilm.getStars().add(tempStar);
					} else {
						System.out.println("No film found with Film ID: " + filmid);
					}
				}
			}
			
		}
	}
}
