package com.example.daniel.favorflix;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;

public class LogInError extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_log_in_error);
    }

    public void goBack(View view) {
        Intent toLogIn = new Intent(this, LogIn.class);
        startActivity(toLogIn);
    }
}
