from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentParser:
    """
    SentimentParser parses the sentiment value from given text and returns the score.
    Arguments:
        text - text to sentiment score.
    """

    def __new__(cls, text):
        analyzer = SentimentIntensityAnalyzer()
        score = analyzer.polarity_scores(text)['compound']

        return score
