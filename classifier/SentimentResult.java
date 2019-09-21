package edu.sjsu.tweentiment.classifier;

import java.util.ArrayList;

import edu.sjsu.tweentiment.SentimentType;

public class SentimentResult {
	public SentimentType sentimentType;
	public double sentimentValue;
	public ArrayList<Word> positiveWordList;
	public ArrayList<Word> negativeWordList;

	public SentimentResult(ArrayList<Word> positiveWordList, ArrayList<Word> negativeWordList, double totalSentimentValue) {
		this.positiveWordList = positiveWordList;
		this.negativeWordList = negativeWordList;
		sentimentValue = totalSentimentValue;

		if (sentimentValue == 0) {
			sentimentType = SentimentType.Neutral;
		} else if (sentimentValue > 0) {
			sentimentType = SentimentType.Positive;
		} else {
			sentimentType = SentimentType.Negative;
		}
	}
}
