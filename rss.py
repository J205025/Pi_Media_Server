#! /usr/bin/env python3
from datetime import date,timedelta 
import getpodcast
import feedparser

N = 27
Ndays_ago = date.today()- timedelta(days=N)
Ndays_ago.strftime("%Y-%m-%d")

opt = getpodcast.options(
    date_from = str(Ndays_ago),
    root_dir = './podcast')

Feed= feedparser.parse("http://feeds.bbci.co.uk/news/world/rss.xml")
pointer = Feed.entries[1]
print(pointer.link)



podcasts = {
   "BBC" : "http://www.bbc.co.uk/programmes/p02nq0gn"
}

getpodcast.getpodcast(podcasts, opt)
