package com.example.daniel.favorflix;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.TypedValue;
import android.view.Gravity;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TextView;

import java.util.ArrayList;

public class SearchResult extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_search_result);
        init();
    }

    public void init() {
        Intent intent = this.getIntent();
        ArrayList<String> movietitles = intent.getStringArrayListExtra("movietitles");

        //Get the list of titles from the StringArrayList attribute of the titleIntent, then
        //display them in a table.

        TableLayout movieTable = (TableLayout) findViewById(R.id.table_main);
        TableRow row0 = new TableRow(this);

        TextView tv1 = new TextView(this);

        tv1.setText("Movie Titles");
        tv1.setGravity(Gravity.CENTER);
        tv1.setTextSize(TypedValue.COMPLEX_UNIT_SP, 25);
        row0.addView(tv1);

        movieTable.addView(row0);

        //Add rows with titles into the table.

        for (int i = 0; i < movietitles.size(); i++) {
            TableRow row = new TableRow(this);

            TextView tvtitle = new TextView(this);
            tvtitle.setText(movietitles.get(i));
            row.addView(tvtitle);

            movieTable.addView(row);
        }
    }
}
