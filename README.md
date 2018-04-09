## News Sentiment

This package analyzes the sentiment of each article in a given RSS feed. 

The package provides statistics about article sentiment.

![statistics](https://github.com/escottgoodwin/news_sentiment/raw/master/static/screenshot2.png)

 There is a chart tracking the change in sentiment throughout the article 
![chart](https://github.com/escottgoodwin/news_sentiment/raw/master/static/screenshot3.png)

Finally, the text article's text is provided with a sentiment score for each sentence. 
![color sents](https://github.com/escottgoodwin/news_sentiment/raw/master/static/screenshot1.png)

**Usage**

In the `main()` function, provide the full url of the RSS feed you want to analyze. 

    def main():
	    rss_url = 'http://feeds.feed.com' ## substitute with selected feed
	    html = sentchart2(rss_url)

In the terminal, call: 

    python news_sentiment.py

Analysis 

This package uses the sentiment analysis built into the [TextBlob](http://textblob.readthedocs.io/en/dev/quickstart.html) package. 

Examining the sentences, one can see how misleading the sentiments scores can be. For example, sentences that positive emotions can receive a similar score to those that merely express approval of the subject matter of the sentence. 


<!--stackedit_data:
eyJoaXN0b3J5IjpbNDMzODk0NDcwLDQwOTEyODI1Nl19
-->