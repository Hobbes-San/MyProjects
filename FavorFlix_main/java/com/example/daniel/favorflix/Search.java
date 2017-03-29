package com.example.daniel.favorflix;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.EditText;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class Search extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_search);
    }

    public void searchByTitle(View view) {
        final String title = ((EditText)findViewById(R.id.title)).getText().toString();

        final Intent titleIntent = new Intent(this, SearchResult.class);

        RequestQueue queue = Volley.newRequestQueue(this);

        //Send the search terms to the servlet side, then
        //receive the search results and save them into the
        //StringArrayList attribute of the titleIntent.

        String url = "http://52.37.235.2/Fablix/servlet/FullTextSearch";
        StringRequest request = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>() {

                    //Decode the JSON response from the servlet.

                    public void onResponse(String response) {
                        try {
                            ArrayList<String> movietitles = new ArrayList<String>();
                            JSONArray jArray = new JSONArray(response);

                            for (int i = 0; i < jArray.length(); i++) {
                                movietitles.add(jArray.getString(i));
                            }

                            //Save the results into the titleIntent.

                            titleIntent.putStringArrayListExtra("movietitles", (ArrayList<String>) movietitles);

                            startActivity(titleIntent);

                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                },
                new Response.ErrorListener() {
                    public void onErrorResponse(VolleyError error) {
                        Log.d("error", error.toString());
                    }
                }
        ) {
            protected Map<String,String> getParams() {
                Map<String,String> params = new HashMap<String,String>();
                params.put("term", title);
                return params;
            }
        };

        queue.add(request);
    }

    //Don't remove the search term if back button is pressed.

    public void onBackPressed() {
        moveTaskToBack(false);
    }
}
