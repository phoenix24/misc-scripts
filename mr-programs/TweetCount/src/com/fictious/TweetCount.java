package com.fictious;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class TweetCount {

	public static void main(String[] args) throws Exception {
		// if (args.length != 2) {
		// System.err.println("Usage: TweetCount <input tweet> <output stats> ");
		// System.exit(-1);
		// }

		Job job = new Job();
		job.setJarByClass(TweetCount.class);

		FileInputFormat.addInputPath(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));

		job.setMapperClass(TweetCountMapper.class);
		job.setReducerClass(TweetCountReducer.class);

		job.setOutputKeyClass(LongWritable.class);
		job.setOutputValueClass(Text.class);

		job.waitForCompletion(true);
	}
}
