package com.fictious;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class Tweets {

	public static void main(String[] args) throws Exception {
		
		Configuration conf = new Configuration();
		
		Job job = new Job(conf, "Extract Tweets");
		job.setJarByClass(Tweets.class);

		FileInputFormat.addInputPath(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));

		job.setMapperClass(TweetsMapper.class);
		job.setReducerClass(TweetsReducer.class);

		job.setOutputKeyClass(LongWritable.class);
		job.setOutputValueClass(Text.class);

		job.waitForCompletion(true);
	}
}
