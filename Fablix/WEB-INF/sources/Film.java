import java.io.IOException;
import java.io.*;
import java.net.*;
import java.util.*;

//This class wraps all the information about a film into a convenient bundle.

public class Film {
	private String title;
	private Integer year;
	private String director;
	
	//List of genres the movie belongs to and list of stars that the movie features.
		
	private List<String> genres;
	private List<Star> stars;
		
	public Film() {
		genres = new ArrayList<>();
		stars = new ArrayList<>();
	}
	
	//Display info.
	
	public void printInfo() {
		System.out.println("Title: " + title + " Year: " + year + " Director: " + director);
		
		System.out.print("Genres:");
		for (int i = 0; i < genres.size(); i++) {
			System.out.print(" " + genres.get(i));
		}
		System.out.println();
		
		System.out.print("Stars:");
		for (int i = 0; i < stars.size(); i++) {
			System.out.print(" ");
			System.out.print("First Name: " + stars.get(i).getFirstName() + " Last Name: " + stars.get(i).getLastName() + " Dob: " + stars.get(i).getDob());
		}
		System.out.println();
	}
	
	public void setTitle(String title) {
		this.title = title;
	}
	
	public void setYear(Integer year) {
		this.year = year;
	}
	
	public void setDirector(String director) {
		this.director = director;
	}
	
	public void setGenres(ArrayList<String> genres) {
		this.genres = genres;
	}
	
	public void setStars(ArrayList<Star> stars) {
		this.stars = stars;
	}
	
	public String getTitle() {
		return title;
	}
	
	public Integer getYear() {
		return year;
	}
	
	public String getDirector() {
		return director;
	}
	
	public List<String> getGenres() {
		return genres;
	}
	
	public List<Star> getStars() {
		return stars;
	}
}