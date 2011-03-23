package android.talkcode;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.utils.URLEncodedUtils;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.protocol.BasicHttpContext;
import org.apache.http.protocol.HttpContext;

import android.app.Activity;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;

public class TalkCode extends Activity implements OnClickListener {
    
    private static final int VOICE_RECOGNITION_REQUEST_CODE = 1234;
    private static final String separator = "|";
    
    private static final String user = "disbeat";
    private static final String pass = "treta";

    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        
        // Get display items for later interaction
        Button speakButton = (Button) findViewById(R.id.Button01);

      
        // Check to see if a recognition activity is present
        PackageManager pm = getPackageManager();
        List<ResolveInfo> activities = pm.queryIntentActivities(
                new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH), 0);
        if (activities.size() != 0) {
            speakButton.setOnClickListener(this);
        } else {
            speakButton.setEnabled(false);
            speakButton.setText("Recognizer not present");
        }
    }

    /**
     * Handle the click on the start recognition button.
     */
    public void onClick(View v) {
        if (v.getId() == R.id.Button01) {
            startVoiceRecognitionActivity();
        }
    }

    /**
     * Fire an intent to start the speech recognition activity.
     */
    private void startVoiceRecognitionActivity() {
        Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Speech recognition demo");
        startActivityForResult(intent, VOICE_RECOGNITION_REQUEST_CODE);
    }

    /**
     * Handle the results from the recognition activity.
     */
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == VOICE_RECOGNITION_REQUEST_CODE && resultCode == RESULT_OK) {
            // Fill the list view with the strings the recognizer thought it could have heard
            ArrayList<String> matches = data.getStringArrayListExtra(
                    RecognizerIntent.EXTRA_RESULTS);
            
            Log.d("Recognition", "output starts here");
            for (String s : matches)
                Log.d("recognized", s);
            Log.d("Recognition", "output ends here");
            
            postData(user, pass, matches);
        }

        super.onActivityResult(requestCode, resultCode, data);
    }
    
     public void postData(String user, String pass, ArrayList<String> matches) {  
         // Create a new HttpClient and Post Header  
         HttpClient httpClient = new DefaultHttpClient();
         HttpContext localContext = new BasicHttpContext();
         String joined = "";
         
         for (String part : matches)
             joined = joined.concat(part).concat(separator);
         
         try {  
             
             
             // Add your data  
             List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(2);  
             nameValuePairs.add(new BasicNameValuePair("user", user));  
             nameValuePairs.add(new BasicNameValuePair("pass", pass));
             nameValuePairs.add(new BasicNameValuePair("matches", joined));
             
             String params = URLEncodedUtils.format(nameValuePairs,"UTF8");
             
                 
             
             HttpGet httpget = new HttpGet("http://talkcode.pagekite.me/add"+ "?"+params);
             
             
             HttpResponse response = httpClient.execute(httpget, localContext);
             String result = "";
              
             BufferedReader reader = new BufferedReader(
                 new InputStreamReader(
                   response.getEntity().getContent()
                 )
               );
              
             String line = null;
             while ((line = reader.readLine()) != null){
               result += line + "\n";
             }
             
             Log.d("talkcode_response", "========================");
             Log.d("talkcode_response", "out: "+result);
          
/*
         
           
       
             Log.d("talkcode_request", joined);
             
             // Execute HTTP Post Request  
             HttpResponse response = httpclient.execute(httppost);
             
             String sb = new String();
             char [] buf = new char[2048];
             int len;
             
             InputStream is = response.getEntity().getContent();
             InputStreamReader isr = new InputStreamReader(is);
             while(is.available() > 0) {
                 len = isr.read(buf);
                 sb += String.valueOf(buf);
             }
               
    */         
         } catch (ClientProtocolException e) {  
             // TODO Auto-generated catch block
             Log.d("talkcode_error", e.getMessage());
         } catch (IOException e) {  
             // TODO Auto-generated catch block
             Log.d("talkcode_error", e.getMessage());
         }  
     }  
    
}
 