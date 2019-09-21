package edu.sjsu.tweentiment.classifier;

import com.google.gson.annotations.*;

import edu.sjsu.tweentiment.SentimentType;

public class Word {
	@SerializedName("name")
	public String text;
	@SerializedName("weight")
	public double sentimentValue = 0d;
	@Expose
	public SentimentType sentimentType = SentimentType.Neutral;

	public Word(String text, double sentimentValue) {
		this.text = text;
		this.sentimentValue = sentimentValue;

		if (sentimentValue == 0) {
			sentimentType = SentimentType.Neutral;
		} else if (sentimentValue > 0) {
			sentimentType = SentimentType.Positive;
		} else {
			sentimentType = SentimentType.Negative;
		}
	}

	public Word(Word word) {
		this(word.text, word.sentimentValue);
	}
}
