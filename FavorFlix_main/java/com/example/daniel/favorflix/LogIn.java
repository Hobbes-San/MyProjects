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

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class LogIn extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_log_in);
    }

    public void sendInfo(View view) {
        final String email = ((EditText)findViewById(R.id.email)).getText().toString();
        final String password = ((EditText)findViewById(R.id.password)).getText().toString();

        final Intent searchIntent = new Intent(this, Search.class);
        final Intent errorIntent = new Intent(this, LogInError.class);

        RequestQueue queue = Volley.newRequestQueue(this);

        //Send the customer email and password input to the servlet side,
        //then receive confirmation whether the information is valid or not.

        //Allow access to title search if valid, and
        //redirect to log in error page if not.

        String url = "http://52.37.235.2/Fablix/servlet/LogInAndroid";
        StringRequest request = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>() {

                    //Decode the JSON response from the servlet.

                    public void onResponse(String response) {
                        try {
                            JSONObject jObj = new JSONObject(response);

                            String success = jObj.getString("info");

                            if (success.equals("success")){
                                startActivity(searchIntent);
                            } else {
                                startActivity(errorIntent);
                            }
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
                params.put("email", email);
                params.put("password", password);
                return params;
            }
        };

        queue.add(request);
    }

    //Don't remove the email and password info if the back button is pressed.

    public void onBackPressed() {
        moveTaskToBack(false);
    }
}
