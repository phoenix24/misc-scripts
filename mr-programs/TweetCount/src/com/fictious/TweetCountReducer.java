package com.fictious;

import java.io.IOException;
import java.util.Iterator;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class TweetCountReducer extends
		Reducer<LongWritable, Text, LongWritable, Text> {

	public void reduce(LongWritable key, Iterable<Text> values, Context context)
			throws IOException, InterruptedException {

		String line = "";
		String line1 = "";
		String lines[];
		long tweetid = 0;
		long tweetid1 = 0;
		
		Iterator<Text> it = values.iterator();
		
		while (it.hasNext()) {
			line = it.next().toString();
			lines = line.split(",");
			tweetid = new Long(lines[0]);
			
			if (tweetid > tweetid1) {
				line1 = line;
				tweetid1 = tweetid;
			}
		}
		
		context.write(key, new Text(line1));
	}
}
