package com.glass.ios27iconpack;

import android.app.Activity;
import android.os.Bundle;
import android.view.Gravity;
import android.widget.GridLayout;
import android.widget.ImageView;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.LinearLayout;
import java.lang.reflect.Field;

public class MainActivity extends Activity {
    @Override protected void onCreate(Bundle b) {
        super.onCreate(b);
        float d = getResources().getDisplayMetrics().density;
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding((int)(12*d),(int)(32*d),(int)(12*d),(int)(12*d));
        TextView t = new TextView(this);
        t.setText("iOS 27 Glass Icons\nLauncher (Nova / Lawnchair / etc.) settings me is icon pack ko apply karo.");
        t.setTextSize(16);
        root.addView(t);
        GridLayout g = new GridLayout(this);
        g.setColumnCount(4);
        int size = (int)(76*d);
        try {
            for (Field f : R.drawable.class.getFields()) {
                if (f.getName().startsWith("ic_")) continue;
                ImageView v = new ImageView(this);
                v.setImageResource(f.getInt(null));
                GridLayout.LayoutParams lp = new GridLayout.LayoutParams();
                lp.width = size; lp.height = size;
                lp.setMargins((int)(6*d),(int)(6*d),(int)(6*d),(int)(6*d));
                lp.setGravity(Gravity.CENTER);
                g.addView(v, lp);
            }
        } catch (Exception e) { t.append("\n" + e); }
        root.addView(g);
        ScrollView sv = new ScrollView(this);
        sv.addView(root);
        setContentView(sv);
    }
}
