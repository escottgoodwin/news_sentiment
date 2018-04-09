import json
from textblob import TextBlob
from collections import Counter
import re
import os
import nltk
import feedparser
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
from IPython.core.display import HTML,display
from scipy import stats
from flask import Flask, flash, redirect, render_template, request, session, abort
import webbrowser,threading
from urllib.request import pathname2url

def art_parser(link):
    r = requests.get(link)
    page = r.text
    soup = BeautifulSoup(page,"lxml")
    for x in soup('script'):
        x.decompose()
    for x in soup('link'):
        x.decompose()
    for x in soup('meta'):
        x.decompose()
    paras = soup('p')
    atriclestrip = [art.get_text() for art in paras]
    prep_art = ' '.join(atriclestrip)
    return prep_art

def prep_articles(feed):
    try:
        d = feedparser.parse(feed)
        sec_title = d['feed']['title']
    except:
        print('error'+feed)
        pass
    links = []
    for x in range(len(d['entries'])):
        if 'http://' in d['entries'][x]['link'] or 'https://' in d['entries'][x]['link']:
            page_link = d['entries'][x]['link']
            links.append(page_link)
        else:
            print('bad link')
    articles = []
    for link in links:
        try:
            art = art_parser(link)
            articles.append(art)
        except:
            print('error'+link)
            pass
    print(len(articles))
    return articles,sec_title

def sentchart2(rsslink):

    def colorchoose1(x):
        if x > 0:
            percent = 50 * x
            shade = 'hsl(100, 100%,'  + str(int(percent)) + '%)'
        if x < 0:
            percent = 50 * abs(x)
            shade = 'hsl(0, 100%,'  + str(int(percent)) + '%)'
        if x == 0:
            shade = 'hsl(0, 100%,0%)'
        return shade

    urlbase = './sentchart/'
    try:
        d = feedparser.parse(rsslink)
        sec_title = d['feed']['title']
    except:
        print('error'+feed)
        pass

    html = '''<!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <meta name="description" content="">
            <meta name="author" content="">
            <link rel="icon" href="https://getbootstrap.com/favicon.ico">
            '''
    html += '<title>' + sec_title + '</title>'
    html += '''
                <!-- Bootstrap core CSS -->
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
            <link href="static/offcanvas.css" rel="stylesheet">
          </head>

          <body class="bg-light">

            <nav class="navbar navbar-expand-md fixed-top navbar-dark bg-dark">
              <a class="navbar-brand" href="#">News Sentiment</a>
              <button class="navbar-toggler p-0 border-0" type="button" data-toggle="offcanvas">
                <span class="navbar-toggler-icon"></span>
              </button>

              <div class="navbar-collapse offcanvas-collapse" id="navbarsExampleDefault">
                <ul class="navbar-nav mr-auto">

                    </div>
                  </li>
                </ul>
              </div>
            </nav>

            <main role="main" class="container">
              <div class="d-flex align-items-center p-3 my-3 text-white-50 bg-purple rounded box-shadow">
                <div class="lh-100">
                  <h6 class="mb-0 text-white lh-100">
                  '''
    html += sec_title
    html += '''</h6>
                </div>
              </div>'''

    averages = []
    for index,x in enumerate(d['entries']):

        page_link = x['link']
        title = x['title']
        summary = x['summary']

        try:
            rssart = art_parser(page_link)
        except:
            continue

        blobart = TextBlob(rssart)

        artsent = []
        sentiments = []
        sents = blobart.sentences
        for sent in sents:
            sentiment = sent.sentiment
            item = [sent,sentiment]
            artsent.append(item)
            sentiments.append(sentiment[0])

        avg = np.mean(sentiments)
        averages.append(avg)
        pos = [num for num in sentiments if num >0]
        neg = [num for num in sentiments if num <0]
        neu = [num for num in sentiments if num == 0]
        pospercent = len(pos) / len(sentiments)
        negpercent = len(neg) / len(sentiments)
        neupercent = len(neu) / len(sentiments)


        html += '<div class="my-3 p-3 bg-white rounded box-shadow"><h6 class="border-bottom border-gray pb-2 mb-0">'
        html += '<p><a href="' + page_link + '" target="_blank">' + title + '</a></h6></p>'
        html += '<p><b>average sentiment</b>: ' + str(avg) + '</p>'
        html += '<p><b>pos</b> - num of sents: ' + str(len(pos)) + ' - % of sents: ' + str(pospercent) + ' - avg of pos: ' + str(np.mean(pos)) + '</p>'
        html += '<p><b>neg</b> - num of sents: ' + str(len(neg)) + ' - % of sents ' + str(negpercent) + ' - avg of neg: ' + str(np.mean(neg)) + '</p>'
        html += '<p><b>neutral</b> - num of sents: ' + str(len(neu)) + ' - % of sents: ' + str(neupercent) + '</p>'

        plt.plot(sentiments)
        plt.ylabel('sentiment polarity')
        plt.xlabel('sentence number')
        imgtitle = 'image' + str(index) + '.jpg'
        plt.savefig(urlbase+imgtitle)
        plt.close()

        html += '</p> <p><img src="' + urlbase + imgtitle + '" alt="All Errors Bar Graph" > </p>'

        allsents = []
        for sent in artsent:
            shade1 = colorchoose1(float(sent[1][0]))
            asdf = '<div class="media text-muted pt-3 dont-break-out">'
            asdf += '<div style="color:'+ shade1 +'">' + str(sent[0]) + ' <i>(sentiment: ' + str(sent[1][0]) + ')</i></div></div>'
            allsents.append(asdf)
        print(len(allsents))
        htmlsents = ' '.join(allsents)

        html += htmlsents
        html +=  '</div>'

    descrip = stats.describe(averages)
    hstd = np.std(averages)

    html += '</div><div class="my-3 p-3 bg-white rounded box-shadow"><h6 class="border-bottom border-gray pb-2 mb-0">Section Stats</h6><div class="media text-muted pt-3 dont-break-out"><p> '
    html += '<b>min - max sentiment </b>' + str(descrip[1][0]) + ' - ' +  str(descrip[1][1]) + '<br>'
    html += '<b>Avg:</b> ' + str(descrip[2]) + '<br>'
    html += '<b> Variance:</b> ' + str(descrip[3]) + ' (' + str(descrip[2] + descrip[3]) + ' - ' + str(descrip[2] - descrip[3]) + ')<br>'
    html += '<b>num of arts: </b>' + str(len(averages)) + '<br>'

    plt.hist(averages)
    plt.ylabel('articles')
    plt.xlabel('sentiment')
    sectionimage = 'section_summary'
    plt.savefig(urlbase+sectionimage + '.jpg')
    plt.close()

    html += '<img class="mx-auto d-block" src="' + urlbase+sectionimage + '.jpg" alt="Cluster Chart" width="640" height="auto"></p></div></div></main>'
    html += '''
            <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
            <script>window.jQuery || document.write('<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"><\/script>')</script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>

            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/holder/2.9.4/holder.min.js"></script>
            <script src="static/offcanvas.js"></script>
          </body>
        </html>
        '''

    file_name =  sec_title + ".html"
    f= open(file_name,"w+")
    f.write(html)
    f.close()

    url = 'file:{}'.format(pathname2url(os.path.abspath(file_name)))
    webbrowser.open_new(url)

    return html


def main():
    rss_url = 'http://feeds.nytimes.com/nyt/rss/Business'
    html = sentchart2(rss_url)

if __name__ == '__main__':
    main()
