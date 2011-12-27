package com.fictious;

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.json.JSONObject;

public class TweetWordCountMapper extends
		Mapper<LongWritable, Text, Text, IntWritable> {

	private final static IntWritable one = new IntWritable(1);
	private Text word = new Text();
	
	public void map(LongWritable key, Text value, Context context)
			throws IOException, InterruptedException {

		String line = value.toString();
		JSONObject json;sz
		JSONObject user;

		try {
			json = new JSONObject(line);
			user = json.getJSONObject("user");
			String tweet = json.getString("text");
			String lang = user.getString("lang");
			long following = user.getLong("friends_count");
			long followers = user.getLong("followers_count");
			long statuses_count = user.getLong("statuses_count");

			if (followers > 1 && following > 1 && statuses_count > 1
					&& lang != null && "en".equalsIgnoreCase(lang)) {

				StringTokenizer tokens = new StringTokenizer(tweet);
				while (tokens.hasMoreTokens()) {
					word.set(tokens.nextToken());
					context.write(word, one);
				}
			}

		} catch (Exception e) {

		}
	}
}
