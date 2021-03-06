## News Sentiment

This package analyzes the sentiment of each article in a given RSS feed. This allows an easy way to evaluate the quality of sentence level sentiment scoring. 

**Article Statistics** 

The package provides statistics about article sentiment.

![statistics](https://github.com/escottgoodwin/news_sentiment/raw/master/static/screenshot2.png)

**Sentiment Chart**

 There is a chart tracking the change in sentiment throughout the article 
![chart](https://github.com/escottgoodwin/news_sentiment/raw/master/static/screenshot3.png)

**Sentence Level Sentiment Scoring**

Finally, the text article's text is provided with a sentiment score for each sentence. Sentences are colored in accordance with sentiment score - the brighter the green, the more positive, the brighter the red, the more negative. Neutral sentences are black. 
![color sents](https://github.com/escottgoodwin/news_sentiment/raw/master/static/screenshot1.png)

At the end, statistics and chart for the entire section are presented.

**Usage**

In the `main()` function, provide the full url of the RSS feed you want to analyze. 

    def main():
	    rss_url = 'http://feeds.feed.com' ## substitute with selected feed
	    html = sentchart2(rss_url)

In the terminal, call: 

    python news_sentiment.py

**Analysis** 

This package uses the sentiment analysis built into the [TextBlob](http://textblob.readthedocs.io/en/dev/quickstart.html) package. 

Examining the sentences, one can see how misleading the sentiments scores can be. For example, sentences that express positive emotions may receive a similar score to those that merely express approval of the subject matter of the sentence. 

Some of the sentiment scoring is down right baffling: 

> The ruble dropped more than 4 percent against the dollar, and the price of government bonds fell. _(positive sentiment: 0.5)_

While this package provides an easy way to get a feel for the sentiment of a particular RSS feed, one can review the sentence level scoring to determine the reliability of the sentiment scores. 

<!--stackedit_data:
eyJoaXN0b3J5IjpbMTk2NDgwMzAwMSwxNDcwNTA5MjY4LC0xMT
U3MTU2NDIsNDA5MTI4MjU2XX0=
-->