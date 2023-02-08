#!/usr/bin/env python3 
from datetime import date,timedelta,datetime 
import getpodcast

N = 3
Ndays_ago = date.today()- timedelta(days=N)
Ndays_ago.strftime("%Y-%m-%d")
opt = getpodcast.options(
root_dir = '/home/ubuntu/Music/podcast',
date_from = str(Ndays_ago),
deleteold = True,
run = True)
podcasts = {
   "BBC" : "http://podcasts.files.bbci.co.uk/p02nq0gn.rss",
   "Daily" :"https://feeds.simplecast.com/54nAGcIl"
   }
getpodcast.getpodcast(podcasts, opt)

