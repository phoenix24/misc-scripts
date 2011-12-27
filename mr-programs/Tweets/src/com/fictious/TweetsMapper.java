package com.fictious;

import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.json.JSONObject;

public class TweetsMapper extends 
		Mapper<LongWritable, Text, LongWritable, Text> {

	JSONObject jsonobj;
	JSONObject userobj;

	String line;
	String lang;
	String tweet;
	String source;
	String favorited;
	String created_at;
	String in_reply_to_user_id;
	String in_reply_to_status_id;
	
	long userID;
	long tweetID;
	
	public void map(LongWritable key, Text value, Context context)
			throws IOException, InterruptedException {

		try {
			line = value.toString();
			
			jsonobj = new JSONObject(line);
			tweet = jsonobj.getString("text");
			source = jsonobj.getString("source");
			favorited = jsonobj.getString("favorited");
			created_at = jsonobj.getString("created_at");
			in_reply_to_user_id = jsonobj.getString("in_reply_to_user_id");
			in_reply_to_status_id = jsonobj.getString("in_reply_to_status_id");
			
			tweetID = jsonobj.getLong("id_str");
			
			userobj = jsonobj.getJSONObject("user");
			userID = userobj.getLong("id");
			lang = userobj.getString("lang");
			
			line = userID + "," + source  + "," + favorited  + "," + lang + "," + in_reply_to_user_id + "," + in_reply_to_status_id + "," + created_at + "," + tweet;
			context.write(new LongWritable(tweetID), new Text(line));
			
		} catch (Exception ex) {

		}
	}
}
