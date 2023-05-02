
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import File, UploadFile
from fastapi import Response
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from threading import Thread
from datetime import date,timedelta,datetime 
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.cron import CronTrigger

#import asyncio
#import argparse
import uvicorn
import getpodcast
import os
import json
import glob
import random 
import RPi.GPIO as GPIO
import subprocess
import time
import threading
import vlc
#
#------------------------------------------------------------------
__dir__ = "./static/assets/"
__fileList__ = [] 
#                 0     1         2      3     4      5       6       7       8       9     10      11      12       13     14    15    16    17     18   19
__typeList__ = ["all","podcast","國語","台語","古典","張學友","劉德華","方宥心","原子邦妮","日語","周杰倫","鄭進一","原子邦妮","英語","pop","pop","pop","pop","紅樓夢","佛說"] 
__fileList_Rn__ = []
__indexMax__ = 0
__indexPi__ = 1
__cronIndexPi__ = 1
__indexPc__ = 0 
__num4dPi_i__ = 4
__num4dPi__ = [ 0, 0, 0, 0 ]
__keyTimerPi__= False
__timer_Key__ = None
opt = "--aout=alsa --alsa-audio-device=hw --verbose=-1"
__musicVlcInstance__ = vlc.Instance(opt)
__radioVlcInstance__ = vlc.Instance(opt)
__vlcEnded__ = vlc.State.Ended
__vlcPaused__ = vlc.State.Paused
__vlcPlaying__ = vlc.State.Playing
__vlcmedia__ = None 
__musicVlcPi__ = __musicVlcInstance__.media_player_new()
__musicVlcPiDuration__ = 0
__radioVlcPi__ = __radioVlcInstance__.media_player_new()
__musicPiPlaying__ = False
__radioPiPlayingNo__ =  0
__volumePi__ = 65
__volumePiMute__ = False
__musicPiPlayMode__ = 0
__down_thread__ = None
__downStatus__ = False
__return_code__ = None
__playRatePi__ = 1
__sleepTimePi__ = 0
__timer_Sleep__ = None
__cronTimeHour__ = '00'
__cronTimeMin__ = '00'
__cronStatus__= False
radioUrl={
          "url01":"https://stream.live.vc.bbcmedia.co.uk/bbc_world_service",
          "url02":"http://stream.live.vc.bbcmedia.co.uk/bbc_london",
          "url03":"https://npr-ice.streamguys1.com/live.mp3",
          "url04":"https://prod-18-232-88-129.wostreaming.net/foxnewsradio-foxnewsradioaac-imc?session-id=0f99acd44126cef33b40ce217c9ea1ad",
          "url05":"http://stream.live.vc.bbcmedia.co.uk/bbc_radio_five_live",
          "url06":"http://stream.live.vc.bbcmedia.co.uk/bbc_asian_network",
          "url07":"http://stream.live.vc.bbcmedia.co.uk/bbc_radio_one",
          "url08":"https://icrt.leanstream.co/ICRTFM-MP3?args=web",
          "url09":"http://stream.live.vc.bbcmedia.co.uk/bbc_radio_two",
          "url10":"http://localhost:8000/stream.ogg",
          "url11":"http://onair.family977.com.tw:8000/live.mp3",
          "url12":"https://n09.rcs.revma.com/aw9uqyxy2tzuv?rj-ttl=5&rj-tok=AAABhZollCEACdvxzVVN61ARVg",
          "url13":"https://n10.rcs.revma.com/ndk05tyy2tzuv?rj-ttl=5&rj-tok=AAABhZouFPAAQudE3-49-1PFHQ",
          "url14":"https://n09.rcs.revma.com/7mnq8rt7k5zuv?rj-ttl=5&rj-tok=AAABhZovh0cASZAucd0xcmxkvQ",
          "url15":"https://n11a-eu.rcs.revma.com/em90w4aeewzuv?rj-tok=AAABhZoyef8AtFfbdaYYtKJnaw&rj-ttl=5",
          "url16":"https://n07.rcs.revma.com/78fm9wyy2tzuv?rj-ttl=5&rj-tok=AAABhZozdbQAkV-tPDO6A5aHag",
          "url17":"http://stream.live.vc.bbcmedia.co.uk/bbc_radio_three",
          "url18":"http://stream.live.vc.bbcmedia.co.uk/bbc_radio_fourfm",
          "url19":"http://stream.live.vc.bbcmedia.co.uk/bbc_6music",
          "url20":"http://stream.live.vc.bbcmedia.co.uk/bbc_6music",
          "url21":"http://stream.live.vc.bbcmedia.co.uk/bbc_6music",
          "url22":"http://stream.live.vc.bbcmedia.co.uk/bbc_6music",
          "url23":"http://stream.live.vc.bbcmedia.co.uk/bbc_6music",
          "url24":"http://stream.live.vc.bbcmedia.co.uk/bbc_6music",
          "url25":"http://stream.live.vc.bbcmedia.co.uk/bbc_6music",
          "url26":"http://stream.live.vc.bbcmedia.co.uk/bbc_6music",
          "url27":"http://stream.live.vc.bbcmedia.co.uk/bbc_6music",
          "url28":"http://stream.live.vc.bbcmedia.co.uk/bbc_6music",
          "url29":"http://stream.live.vc.bbcmedia.co.uk/bbc_6music",
          "url30":"http://media-ice.musicradio.com:80/ClassicFMMP3"
          }
url_json=json.dumps(radioUrl)
__url__=json.loads(url_json)

#------------------------------------------------------------------
    
def pressedNumber(channel):
    if(channel ==12):
        Number = 1
        print("1 Pressed")
    elif(channel ==16):
        Number = 2
        print("2 Pressed")
    elif(channel ==18):
        Number = 3
        print("3 Pressed")
    elif(channel ==11):
        Number = 4
        print("4 Pressed")
    elif(channel ==13):
        Number = 5
        print("5 Pressed")
    elif(channel ==15):
        Number = 6
        print("6 Pressed")
    return Number

def handleSelectedPi():
    global __musicVlcInstance__
    global __musicVlcPi__
    global __musicPiPlaying__
    global __dir__
    global __fileList__
    global __num4dPi__
    global __indexPi__
    global __num4dPi_i__
    global __vlcmedia__
    #file = __dir__ + __fileList__[__indexPi__]
    handlePlayPi(__indexPi__)
    #__musicVlcPi__.stop()
    #__vlcmedia__  = __musicVlcInstance__.media_new(file)
    #__musicVlcPi__.set_media(__vlcmedia__)
    #__musicVlcPi__.play()
    #__musicPiPlaying__ = True
    #print("play:"+file)
    __keyTimerPi__= False
    __num4dPi__ = [0, 0, 0, 0]
    __num4dPi_i__ = 4
    
#Convert int array to decimal interger
def convert(list):
    no = sum(d * 10**i for i, d in enumerate(list[::-1]))
    return(no)

def handlePlayPi(index):
    global __fileList__
    global __dir__
    global __musicVlcInstance__
    global __vlcmedia__
    global __musicVlcPi__
    global __musicPiPlaying__
    file = __dir__ + __fileList__[index]
    __musicVlcPi__.stop()
    __vlcmedia__  = __musicVlcInstance__.media_new(file)
    __musicVlcPi__.set_media(__vlcmedia__)
    __musicVlcPi__.play()
    __musicPiPlaying__ = True
    print("play: "+file)
    
def handleCronPlayPi():
    global __cronIndexPi__
    global __indexPi__
    handlePlayPi(__cronIndexPi__)
    __indexPi = __cronIndexPi__
    
def handleKeyInputPi(channel):
    global __indexPi__
    global __indexMax__
    global __dir__
    global __musicPiPlaying__
    global __num4dPi_i__
    global __num4dPi__
    global __timer_Key__
    if (__keyTimerPi__== True):
        __timer_Key__.cancel()
    Number = pressedNumber(channel)
    __num4dPi_i__ = __num4dPi_i__ - 1
    if(__num4dPi_i__ < 0):
        __num4dPi_i__ = 3 
    __num4dPi__[0] = __num4dPi__[1] 
    __num4dPi__[1] = __num4dPi__[2] 
    __num4dPi__[2] = __num4dPi__[3] 
    __num4dPi__[3] = Number 
    num = convert(__num4dPi__)
    __indexPi__ = ( num % __indexMax__) - 1
    if (__indexPi__ == -1 ):
       __indexPi__ = __indexPi__ + __indexMax__
    print("the NO."+str(__indexPi__ + 1)+" mp3 will be played")
    __timer_Key__ = threading.Timer(3, handleSelectedPi)
    __timer_Key__.start()
    __keyTimerPi__= True

def handleNextPi():
    global __indexPi__
    global __indexMax__
    #global __fileList__
    #global __dir__
    #global __musicVlcInstance__
    #global __musicVlcPi__
    #global __vlcmedia__
    #global __musicPiPlaying__
    #global __musicPiPlayMode__
    if (__musicPiPlayMode__ == 1):
        __indexPi__ = random.randrange(__indexMax__)
    elif(__musicPiPlayMode__ == 0):
        __indexPi__ = __indexPi__ + 1
        if (__indexPi__ == __indexMax__):
            __indexPi__ = 0; 
    else:
        __indexPi__ = __indexPi__
    #file = __dir__ + __fileList__[__indexPi__]
    handlePlayPi(__indexPi__)
    #__musicVlcPi__.stop()
    #__vlcmedia__  = __musicVlcInstance__.media_new(file)
    #__musicVlcPi__.set_media(__vlcmedia__)
    #__musicVlcPi__.play()
    #__musicPiPlaying__ = True
    print("__indexPi__:"+str(__indexPi__))
    #print("Next play:"+file)

def handlePrePi():
    global __indexPi__
    global __indexMax__
    #global __fileList__
    #global __dir__
    #global __musicVlcInstance__
    #global __vlcmedia__
    #global __musicVlcPi__
    #global __musicPiPlaying__
    if (__musicPiPlayMode__ == 1):
        __indexPi__ = random.randrange(__indexMax__)
    if (__musicPiPlayMode__ == 0):
        __indexPi__ = __indexPi__ - 1
        if (__indexPi__ < 0):
           __indexPi__= __indexMax__ - 1
    else:
        __indexPi__ = __indexPi__
    #file = __dir__ + __fileList__[__indexPi__]
    handlePlayPi(__indexPi__)
    #__vlcmedia__  = __musicVlcInstance__.media_new(file)
    #__musicVlcPi__.stop()
    #__musicVlcPi__.set_media(__vlcmedia__)
    #__musicVlcPi__.play()
    #__musicPiPlaying__ = True
    print("__indexPi__:"+str(__indexPi__))
    #print("Pre play:"+file)

def handlePlayPausePi():
    global __indexPi__
    global __musicVlcInstance__
    global __musicVlcPi__
    global __musicPiPlaying__
    global __fileList__
    if (__musicPiPlaying__ == True):
        time.sleep(0.1)
        __musicVlcPi__.pause()
        __musicPiPlaying__ = False
    else:
        file = __dir__ + __fileList__[__indexPi__]
       # vlcmedia  = __musicVlcInstance__.media_new(file)
       # __musicVlcPi__.set_media(vlcmedia)
        __musicVlcPi__.play()
        __musicPiPlaying__ = True
        print("PlayPause- Play:"+file)
        
def handlePlayRatePi():
    global __musicVlcPi__
    global __playRatePi__
    __playRatePi__ = __playRatePi__ + 0.5
    if __playRatePi__ > 2.5:
        __playRatePi__ = 0.5
    __musicVlcPi__.set_rate(__playRatePi__)
    
def handleVolCtlPi(vol):
    global __musicVlcPi__
    global __radioVlcPi__
    global __volumePi__
    __volumePi__ = __volumePi__ + vol
    if __volumePi__ < 0:
        __volumePi__ = 0 
    if __volumePi__ > 100:
        __volumePi__ = 100 
    if __volumePi__ ==  0:
        __volumePiMute__ = True
    else:      
        __volumePiMute__ = False
    vlcvolume = __volumePi__
    __radioVlcPi__.audio_set_volume(vlcvolume)
    __musicVlcPi__.audio_set_volume(vlcvolume)
    
#def get_files(root):
#    files = []
#    def scan_dir(dir):
#        for f in os.listdir(dir):
#            #f = os.path.join(dir, f)
#            if os.path.isdir(f):
#                scan_dir(f)
#            elif os.path.splitext(f)[1] == ".mp3":
#                files.append(f)
#   scan_dir(root)
#   return files

def continuePlaying():
    global __musicVlcPi__
    global __musicPiPlaying__
    global __vlcEnded__
    global __vlcPlaying__
    state = __musicVlcPi__.get_state()
    #print(state)
    if (__musicPiPlaying__ == True ):
        if (state == __vlcEnded__):
            handleNextPi();
        threading.Timer( 10 , continuePlaying ).start()
    else:
        threading.Timer( 10 , continuePlaying ).start()

def stopPlaying():
    global __musicVlcPi__
    global __radioVlcPi__
    global __musicPiPlaying__
    global __radioPiPlayingNo__
    global __sleepTimePi__
    if (__musicPiPlaying__ ==True or __radioPiPlayingNo__ != 0):
        __musicVlcPi__.stop()
        __radioVlcPi__.stop()
        __musicPiPlaying__ = False
        __radioPiPlayingNo__ = 0
        # set SleepTimePi to NonSleep
        __sleeTimePi__ =3
        

def genFileList_sh(style):
    global __fileList__
    global __dir__
    global __musicVlcPi__
    global __musicPiPlaying__
    global __indexMax__
    global __indexPi__
    global __typeList__
    match style:
        case 0:
           subdir = __typeList__[0]
        case 1:
           subdir = __typeList__[1]
        case 2:
           subdir = __typeList__[2]
        case 3:
           subdir = __typeList__[3]
        case 4:
           subdir = __typeList__[4]
        case 5:
           subdir = __typeList__[5]
        case 6:
           subdir = __typeList__[6]
        case 7:
           subdir = __typeList__[7]
        case 8:
           subdir = __typeList__[8]
        case 9:
           subdir = __typeList__[9]
        case 10:
           subdir = __typeList__[10]
        case 11:
           subdir = __typeList__[11]
        case 12:
           subdir = __typeList__[12]
        case 13:
           subdir = __typeList__[13]
        case 14:
           subdir = __typeList__[14]
        case 15:
           subdir = __typeList__[15]
        case 16:
           subdir = __typeList__[16]
        case 17:
           subdir = __typeList__[17]
        case 18:
           subdir = __typeList__[18]
        case 19:
           subdir = __typeList__[19]
        case _:
           subdir = __typeList__[0]
    __musicVlcPi__.stop()
    __musicPiPlaying__ = False
    mp3s = []; 
    for path, subdirs, files in os.walk(__dir__ + subdir, followlinks=True):
       # for name in files:
        path = path[(len(__dir__)-1):];
        path = path+"/";
        path = path[1:];
        files = [path + file for file in files];
        mp3s= mp3s + files; 
    mp3s = [ f for f in mp3s if f[-4:] == '.mp3' ];
    mp3s.sort()
    __fileList__ = mp3s;
    __indexMax__ = len(__fileList__) 
    __indexPi__ = random.randrange(__indexMax__)
    file = __dir__ + __fileList__[__indexPi__]
    __vlcmedia__  = __musicVlcInstance__.media_new(file)
    __musicVlcPi__.set_media(__vlcmedia__)
    
def downPodcastFile_sh():
    N = 7
    Ndays_ago = date.today()- timedelta(days=N)
    Ndays_ago.strftime("%Y-%m-%d")
    opt = getpodcast.options(
    root_dir = '/home/ubuntu/Music/podcast',
    date_from = str(Ndays_ago),
    deleteold = True,
    run = True)
    podcasts = {
       "BBC" : "http://podcasts.files.bbci.co.uk/p02nq0gn.rss"
    }
    getpodcast.getpodcast(podcasts, opt)


def downPodcastFile_sh2():
    try:
      command = ["/home/ubuntu/Pi_FastAPI_Server/.venv/bin/python3", "/home/ubuntu/Pi_Media_Server/getpodcast_sh.py"]
      p = subprocess.Popen(command)
      return p
    except FileNotFoundError as e:
       raise AudioEngineUnavailable(f'AudioEngineUnavailable: {e}')

def process_monitor(p):
    global __return_code__
    global __downStatus__
    __return_code__ = p.poll()
    if __return_code__ == None:
        __return_code__ = p.wait()
    __downStatus__ = False
#----------------------------------------------------------------------------
#
#----------------------------------------------------------------------------

if(True):
    GPIO.setmode(GPIO.BOARD)
   # gpio binary  
    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   # PLAY NEXT PRE BACK MUTE 
    GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP)

   #callback function 
    GPIO.add_event_detect(12, GPIO.FALLING, callback=handleKeyInputPi, bouncetime=500)
    GPIO.add_event_detect(16, GPIO.FALLING, callback=handleKeyInputPi, bouncetime=500)
    GPIO.add_event_detect(18, GPIO.FALLING, callback=handleKeyInputPi, bouncetime=500)
    GPIO.add_event_detect(11, GPIO.FALLING, callback=handleKeyInputPi, bouncetime=500)
    GPIO.add_event_detect(13, GPIO.FALLING, callback=handleKeyInputPi, bouncetime=500)
    GPIO.add_event_detect(15, GPIO.FALLING, callback=handleKeyInputPi, bouncetime=500)
    GPIO.add_event_detect(29, GPIO.FALLING, callback=handlePlayPausePi, bouncetime=500)
    GPIO.add_event_detect(31, GPIO.FALLING, callback=handleNextPi, bouncetime=500)
    GPIO.add_event_detect(33, GPIO.FALLING, callback=handlePrePi, bouncetime=500)
    #GPIO.add_event_detect(37, GPIO.FALLING, callback=handleMutePi, bouncetime=500)
    
#---------------------------------------------------------------------
#file list Method 1
#    __fileList__ = [ f for f in os.listdir(r'./static/assets/.') if f[-4:] == '.mp3' ]
#    mp3_list.sort(key=lambda x:int(x[:-4]))
#--------------------------------------------------------------------
#file list Method 2
#    mp3s = []; 
#    for path, subdirs, files in os.walk(r'./static/assets'):
#       # for name in files:
#        path = path[(len(__dir__)-1):];
#        path = path+"/";
#        path = path[1:];
#        files = [path + file for file in files];
#        mp3s= mp3s + files; 
#    mp3s = [ f for f in mp3s if f[-4:] == '.mp3' ];
#    __fileList__ = mp3s;
#---------------------------------------------------------------------
#file list Methos 3
#    __fileListRn__ = glob.glob(r'../Music/*.mp3')
#    __fileListRn__.sort(key=lambda x:int(x[25:-4]))
#---------------------------------------------------------------------
#file list Method 4
#    __fileList__ = get_files(__dir__)
#    __fileList__.sort(key=lambda x:int(x[:-4]))
#---------------------------------------------------------------------
genFileList_sh(0)
if not (len(__fileList__) > 0):
    print ("No mp3 files found!")
print ('--- Press button #play to start playing mp3 ---')

file1 = __dir__ + __fileList__[__indexPi__]
__vlcmedia__  = __musicVlcInstance__.media_new(file1)
__musicVlcPi__.set_media(__vlcmedia__)
__musicVlcPiDuration__ = __vlcmedia__.get_duration()
threading.Timer( 10 , continuePlaying ).start()

#==============================================================================================
app = FastAPI()
origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=["*"])
templates = Jinja2Templates(directory="./templates")
app.mount("/static", StaticFiles(directory="./static"), name="static")
#-----------------------APSchedule cron job---------------
jobstore = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
scheduler = BackgroundScheduler(jobstores=jobstore)
#scheduler = BackgroundScheduler()
scheduler.start()

#----------------------------------------------------------
#==============================================================================================
@app.get('/')
async def index1():
    global __musicVlcPi__
    global __playRatePi__
    __playRatePi__ = 1
    __musicVlcPi__.set_rate(__playRatePi__)
    return FileResponse('./templates/index.html')

@app.post('/')
async def index2():
    global __dir__
    global __fileList__
    global __indexPi__
    global __musicPiPlaying__ 
    global __musicPiPlayMode__
    global __radioPiPlayingNo__ 
    global __volumePi__
    global __volumePiMute__
    global __playRatePi__
    global __cronStatus__
    global __cronTimeHour__
    global __cronTimeMin__
    global __cronIndexPi__
    return JSONResponse({
        "fileList" : __fileList__,
        "indexPi" : __indexPi__,
        "musicPiPlaying" : __musicPiPlaying__,
        "musicPiPlayMode" : __musicPiPlayMode__,
        "radioPiPlayingNo" : __radioPiPlayingNo__,
        "volumePi" : __volumePi__,
        "volumePiMute" : __volumePiMute__,
        "playRatePi" : __playRatePi__,
        "musicPiDuration":__musicVlcPiDuration__,
        "cronStatus":__cronStatus__,
        "cronTimeHour":__cronTimeHour__,
        "cronTimeMin":__cronTimeMin__,
        "cronIndexPi":__cronIndexPi__
         })
    
@app.post('/playPrePi')
async def playPrePi():
    global __indexPi__
    global __indexMax__
    global __musicPiPlaying__
    handlePrePi();
    return JSONResponse({ 
           "indexPi":__indexPi__,
           "musicPiPlaying" :__musicPiPlaying__
          })
        
@app.post('/playNextPi')
async def playNextPi():
    global __indexPi__
    global __indexMax__
    global __musicPiPlaying__
    handleNextPi();
    return JSONResponse({ 
           "indexPi":__indexPi__,
           "musicPiPlaying" :__musicPiPlaying__
          })
    
@app.post('/playIndexPi')
async def playIndexPi(request :Request):
    global __indexPi__
    global __indexMax__
    global __musicPiPlaying__
    global __vlcmedia__
    global __musicVlcPiDuration__
    data=await request.json()
    num=int(data["indexPi"])
    __indexPi__= num
   # file = __dir__ + __fileList__[__indexPi__]
    handlePlayPi(__indexPi__)
   # __musicVlcPi__.stop()
   # __vlcmedia__  = __musicVlcInstance__.media_new(file)
   # __musicVlcPi__.set_media(__vlcmedia__)
   # __musicVlcPi__.play()
   # __musicPiPlaying__ = True
   # __musicVlcPiDuration__ = __vlcmedia__.get_duration()
    print("__indexPi__:"+str(__indexPi__))
    #print("Next play:"+file)
    return JSONResponse({ 
           "indexPi":__indexPi__,
           "musicPiPlaying" :__musicPiPlaying__
          })
    
@app.post('/playSelectedPi')
async def playSelectedPi(request :Request):
    global __indexPi__
    global __musicPiPlaying__
    global __indexMax__
    global __vlcmedia__
    global __musicVlcPiDuration__
    data=await request.json()
    num=int(data["num"])
    __indexPi__= num % __indexMax__
    handleSelectedPi();
    __musicVlcPiDuration__ = __vlcmedia__.get_duration()
    print("musicPiDuration")
    print(__musicVlcPiDuration__)
    return JSONResponse({ 
           "indexPi":__indexPi__,
           "musicPiPlaying" :__musicPiPlaying__
          })

@app.post('/playPausePi')
async def playPausePi():
    global __musicPiPlaying__
    global __indexPi__
    handlePlayPausePi()
    return JSONResponse({
        "musicPiPlaying" : __musicPiPlaying__,
        "indexPi" : __indexPi__
         })

@app.post('/setPlayRatePi')
def setPlayRatePi():
    global __playRatePi__
    print("playRatePi: " + str(__playRatePi__))
    handlePlayRatePi()
    return JSONResponse({
        "playRatePi" : __playRatePi__
         })
    
@app.post('/setPlayModePi')
async def setPlayModePi(request :Request):
    global __musicPiPlayMode__
    data=await request.json()
    print(data)
    __musicPiPlayMode__=int(data["mode"])
    return JSONResponse({
        "musicPiPlayMode" : __musicPiPlayMode__
         })

@app.post('/setTimePi')
async def setTimePi(request :Request):
    global __musicVlcPi__
    data=await request.json()
    setTimePi=int(data["time"])
    __musicVlcPi__.set_time(setTimePi*1000)
    print("setTimePi:")
    return JSONResponse({
        "setTimePi" : setTimePi
         })
    
@app.post('/playRadioPi')
async def playRadioPi(request :Request):
    global __radioVlcInstance__
    global __radioPiPlayingNo__
    global __radioVlcPi__
    global __url__
    data=await request.json()
    radioNo=int(data["radioNo"])
    match radioNo:
        case 1:
           url =__url__["url01"]
        case 2:
           url =__url__["url02"]
        case 3:
           url =__url__["url03"]
        case 4:
           url =__url__["url04"]
        case 5:
           url =__url__["url05"]
        case 6:
           url =__url__["url06"]
        case 7:
           url =__url__["url07"]
        case 8:
           url =__url__["url08"]
        case 9:
           url =__url__["url09"]
        case 10:
           url =__url__["url10"]
        case 11:
           url =__url__["url11"]
        case 12:
           url =__url__["url12"]
        case 13:
           url =__url__["url13"]
        case 14:
           url =__url__["url14"]
        case 15:
           url =__url__["url15"]
        case 16:
           url =__url__["url16"]
        case 17:
           url =__url__["url17"]
        case 18:
           url =__url__["url18"]
        case 19:
           url =__url__["url19"]
        case 20:
           url =__url__["url20"]
        case 21:
           url =__url__["url21"]
        case 22:
           url =__url__["url22"]
        case 23:
           url =__url__["url23"]
        case 24:
           url =__url__["url24"]
        case 25:
           url =__url__["url25"]
        case 26:
           url =__url__["url26"]
        case 27:
           url =__url__["url27"]
        case 28:
           url =__url__["url28"]
        case 29:
           url =__url__["url29"]
        case 30:
           url =__url__["url30"]
        case _:
           url ="https://stream.live.vc.bbcmedia.co.uk/bbc_world_service"
    if(radioNo == 0):
        __radioVlcPi__.stop()
        __radioPiPlayingNo__ = 0
    else:
        if(__radioPiPlayingNo__ != 0):
           __radioVlcPi__.stop()
        vlcmedia  = __radioVlcInstance__.media_new(url)
        __radioVlcPi__.set_media(vlcmedia)
        __radioVlcPi__.play()
        __radioPiPlayingNo__ = radioNo
        print("Radio Stream URL :"+url)        
    return JSONResponse({
        "radioPiPlayingNo" : __radioPiPlayingNo__
         })

@app.post('/volumeControlPi')
async def volumeControlPi(request :Request):
    global __volumePi__
    global __volumePiMute__
    data=await request.json()
    vol=int(data["vol"])
    handleVolCtlPi(vol)
    return JSONResponse({
        "volumePi" : __volumePi__,
        "volumePiMute" : __volumePiMute__
         })
@app.post('/getMetaPi')
async def getMetaPi():
    global __fileList__
    global __musicVlcPiDuration__
    global __musicVlcPi__
    global __indexPi__
    global __volumePi__
    global __volumePiMute__
    global __musicPiPlaying__
    musicVlcPiCurrent =__musicVlcPi__.get_time()
    __musicVlcPiDuration__ = __vlcmedia__.get_duration()
    return JSONResponse({
        "durationPi" : __musicVlcPiDuration__,
        "currentPi" : musicVlcPiCurrent,
        "indexPi" : __indexPi__,
        "volumePi" : __volumePi__,
        "volumePiMute" : __volumePiMute__,
        "musicPiPlaying" : __musicPiPlaying__
         })

@app.post('/refreshMetaPi')
async def refreshMetaPi():
    global __dir__
    global __fileList__
    global __indexPi__
    global __musicPiPlaying__ 
    global __musicPiPlayMode__
    global __radioPiPlayingNo__ 
    global __volumePi__
    global __volumePiMute__
    global __playRatePi__
    global __cronStatus__
    global __cronTimeHour__
    global __cronTimeMin__
    global __cronIndexPi__
    global __musicVlcPiDuration__
    global __musicVlcPi__
    
    musicVlcPiCurrent =__musicVlcPi__.get_time()
    __musicVlcPiDuration__ = __vlcmedia__.get_duration()
    return JSONResponse({
        "fileList" : __fileList__,
        "indexPi" : __indexPi__,
        "musicPiPlaying" : __musicPiPlaying__,
        "musicPiPlayMode" : __musicPiPlayMode__,
        "radioPiPlayingNo" : __radioPiPlayingNo__,
        "volumePi" : __volumePi__,
        "volumePiMute" : __volumePiMute__,
        "playRatePi" : __playRatePi__,
        "musicPiDuration":__musicVlcPiDuration__,
        "currentPi" : musicVlcPiCurrent,
        "cronStatus":__cronStatus__,
        "cronTimeHour":__cronTimeHour__,
        "cronTimeMin":__cronTimeMin__,
        "cronIndexPi":__cronIndexPi__
         })

@app.post('/getFileList')
async def getFileList(request :Request):
    global __fileList__
    global __musicPiPlaying__
    global __indexPi__
    global __cronIndexPi__
    data=await request.json()
    style=int(data["style"])
    genFileList_sh(style)
    return JSONResponse({
        "fileList" : __fileList__,
        "musicPiPlaying" : __musicPiPlaying__,
        "indexPi":__indexPi__,
        "cronIndexPi":__cronIndexPi__
         })

@app.post('/downPodcastFile')
async def downPodcastFile():
    global __down_thread__
    global __downStatus__
    msg = "" 
    if __downStatus__ == 0:
        __downStatus__ = 1 
        print("downStatus: "+str(__downStatus__))
        #time.sleep(10)
        __down_thread__=Thread(target=downPodcastFile_sh)
        __down_thread__.start()
        print("DownPodcast thread start to run")
        __down_thread__.join()
        __downStatus__ = 0 
        print("DownPodcast thread finished--> downStatus: "+str(__downStatus__))
        msg ="DownPodcast thread finished--> downStatus: "+str(__downStatus__)
    else:
        print("DonwPodcast thread is Running, please wait")
        msg= "DonwPodcast thread is Running, please wait"
    return JSONResponse({
        "downStatus" : __downStatus__,
        "msg" : msg
         })

#this method fork a proceess run  getpodcast_sh.py
@app.post('/downPodcastFile2')
async def downPodcastFile2():
    global __down_thread__
    global __downStatus__
    msg =""
    if __downStatus__ == False:
        __downStatus__ = True 
        print("downStatus: "+str(__downStatus__))
        #time.sleep(10)
        __p__=downPodcastFile_sh2()
        monitor_thread = Thread(target=process_monitor,args=(__p__,)) 
        monitor_thread.start()
        print("DownPodcast thread start to run")
        print("DownPodcast thread finished--> downStatus: "+str(__downStatus__))
        msg ="DownPodcast thread finished--> downStatus: "+str(__downStatus__)
    else:
        print("DonwPodcast thread is Running, please wait")
        msg="DonwPodcast thread is Running, please wait"
    return JSONResponse({
        "downStatus" : __downStatus__,
        "msg" : msg
         })

@app.post('/setSleepTimePi')
async def setSleepTimePi():
    global __musicVlcPi__
    global __radioVlcPi__
    global __musicPiPlaying__
    global __radioPiPlayingNo__
    global __sleepTimePi__
    global __timer_Sleep__
    __sleepTimePi__ = (__sleepTimePi__ + 1 ) % 4
    a= [999,10,20,30]
    if (__timer_Sleep__ != None):
        __timer_Sleep__.cancel()
    __timer_Sleep__= threading.Timer( a[__sleepTimePi__]*60 , stopPlaying)
    __timer_Sleep__.start()
    return JSONResponse({
        "musicPiPlaying" : __musicPiPlaying__,
        "radioPiPlayingNo" : __radioPiPlayingNo__,
        "sleepTimePi" : __sleepTimePi__,
         })
    
@app.post('/setCron')
async def setCron(request: Request):
    global __cronTimeHour__
    global __cronTimeMin__
    global __cronStatus__
    global __cronIndexPi__
    global __dir__
    global __fileList__
    data=await request.json()
    __cronStatus__=data["cronStatus"]
    __cronIndePi__=data["cronIndexPi"]
    print("__cronStatus: "+str(__cronStatus__))
    print(type(__cronStatus__))
    num=int(data["cronIndexPi"])
    file = __dir__ + __fileList__[num]
    print(file+"will be played")
    __cronTimeHour__=int(data["setHour"])
    __cronTimeMin__=int(data["setMin"])
    print("cronTimeHour: "+str(__cronTimeHour__))
    print("cronTimeMin: "+str(__cronTimeMin__))
    if __cronStatus__ == False:
        scheduler.remove_job('my_task')
        __cronStatus__ = False
        print("scheduler job removed")
    else:
        #scheduler.add_job(id='my_task', func=handleCronPlayPi, trigger='cron', hour=__cronTimeHour__, minute=__cronTimeMin__)
        scheduler.add_job(handleCronPlayPi,CronTrigger.from_crontab('0 0 * * *'),id='my_cron_job')
        __cronStatus__ = True
        print("scheduler job added")
    return JSONResponse({
        "cronTimeHour" : __cronTimeHour__,
        "cronTimeMin" : __cronTimeMin__,
        "cronStatus" : __cronStatus__
         })

@app.post('/setCronSong')
async def setCronSong(request: Request):
    global __cronIndexPi__
    data=request.json()
    __cronIndexPi__=int(data["cronIndexPi"])
    return JSONResponse({
        "cronIndexPi" : __cronIndexPi__
         })

#@scheduler.add_job('cron', id='myjobb', day='*', hour='06', minute='00', second='00')
#async def myjobb():
#    downPodcastFile_sh2()
#    print("myDownPodcastFileJob executed")

if __name__ == '__main__':
    uvicorn.run("fast:app", port=3000, reload=True)
