package com.fictious;

import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.json.JSONObject;

public class TweetCountMapper extends 
		Mapper<LongWritable, Text, LongWritable, Text> {

	JSONObject json;
	JSONObject user;

	String line;
	String lang;
	String tweet;
	String id_str;
	String created_at;
	String verified;
	
	long user_id;
	long tweet_id;
	long count = 0;
	long followers;
	long following;
	long listed_count;
	long statuses_count;
	long retweet_count;
	long favourites_count;
	
	long maxstatuses_count = 0;
	long totalstatuses_count = 0;

	public void map(LongWritable key, Text value, Context context)
			throws IOException, InterruptedException {

		try {
			line = value.toString();
			
			json = new JSONObject(line);
			tweet = json.getString("text");
			tweet_id = json.getLong("id_str");
			created_at = json.getString("created_at");
			retweet_count = json.getLong("retweet_count");
			
			user = json.getJSONObject("user");
			
			user_id = user.getLong("id");
			lang = user.getString("lang");
			verified = user.getString("verified");
			following = user.getLong("friends_count");
			followers = user.getLong("followers_count");
			statuses_count = user.getLong("statuses_count");
			favourites_count = user.getLong("favourites_count");
			listed_count = user.getLong("listed_count");
			
			line = tweet_id + "," + verified + "," + followers + "," + following + "," + statuses_count + "," + retweet_count + "," + favourites_count + "," + listed_count + "," + lang + "," + created_at;
			
			context.write(new LongWritable(user_id), new Text(line));
			
		} catch (Exception ex) {

		}
	}
}
