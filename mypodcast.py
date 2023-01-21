#! /usr/bin/env python3
from datetime import date,timedelta 
import getpodcast

N = 7
Ndays_ago = date.today()- timedelta(days=N)
Ndays_ago.strftime("%Y-%m-%d")

opt = getpodcast.options(
    date_from = str(Ndays_ago),
    deleteold = True,
    root_dir = './Podcast'
            )

podcasts = {
   "BBC" : "http://podcasts.files.bbci.co.uk/p02nq0gn.rss"
}

getpodcast.getpodcast(podcasts, opt)
