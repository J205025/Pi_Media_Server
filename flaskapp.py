#!/usr/bin/env python3
from flask import Flask,render_template,request,jsonify
from flask_apscheduler import APScheduler
from flask_cors import CORS
from threading import Thread
from datetime import date,timedelta,datetime 
#import asyncio
#import argparse

#from multiprocessing import Process
from multiprocessing.pool import ThreadPool

#import logging



import getpodcast
import os
import json
import glob
import random 
import jinja2
import RPi.GPIO as GPIO
import subprocess
import time
import threading
import vlc

#
#------------------------------------------------------------------
__dir__ = "./static/assets/"
__fileList__ = [] 
__typeList__ = ["all","pop","podcast","classical","sutra","red","jacky"] 
__fileList_Rn__ = []
__indexMax__ = 0
__indexPi__ = 0
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
__musicVlcPi__ = __musicVlcInstance__.media_player_new()
__radioVlcPi__ = __radioVlcInstance__.media_player_new()
__musicPiPlaying__ = False
__radioPiPlayingNo__ =  0
__volumePi__ = 70
__volumePiMute__ = False
__musicPiPlayMode__ = 0
__down_thread__ = None
__downStatus__ = False
__return_code__ = None
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
    file = __dir__ + __fileList__[__indexPi__]
    __musicVlcPi__.stop()
    vlcmedia  = __musicVlcInstance__.media_new(file)
    __musicVlcPi__.set_media(vlcmedia)
    __musicVlcPi__.play()
    __musicPiPlaying__ = True
    print("play:"+file)
    __keyTimerPi__= False
    __num4dPi__ = [0, 0, 0, 0]
    __num4dPi_i__ = 4
#Convert int array to decimal interger
def convert(list):
    no = sum(d * 10**i for i, d in enumerate(list[::-1]))
    return(no)

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
    global __fileList__
    global __dir__
    global __musicVlcInstance__
    global __musicVlcPi__
    global __musicPiPlaying__
    global __musicPiPlayMode__
    if (__musicPiPlayMode__ == 1):
        __indexPi__ = random.randrange(__indexMax__)
    else:
        __indexPi__ = __indexPi__ + 1
        if (__indexPi__ == __indexMax__):
            __indexPi__ = 0; 
    file = __dir__ + __fileList__[__indexPi__]
    __musicVlcPi__.stop()
    vlcmedia  = __musicVlcInstance__.media_new(file)
    __musicVlcPi__.set_media(vlcmedia)
    __musicVlcPi__.play()
    __musicPiPlaying__ = True
    print("__indexPi__:"+str(__indexPi__))
    print("Next play:"+file)

def handlePrePi():
    global __indexPi__
    global __indexMax__
    global __fileList__
    global __dir__
    global __musicVlcInstance__
    global __musicVlcPi__
    global __musicPiPlaying__
    if (__musicPiPlayMode__ == 1):
        __indexPi__ = random.randrange(__indexMax__)
    else:
        __indexPi__ = __indexPi__ - 1
    if (__indexPi__ < 0):
       __indexPi__= __indexMax__ - 1
    file = __dir__ + __fileList__[__indexPi__]
    vlcmedia  = __musicVlcInstance__.media_new(file)
    __musicVlcPi__.stop()
    __musicVlcPi__.set_media(vlcmedia)
    __musicVlcPi__.play()
    __musicPiPlaying__ = True
    print("__indexPi__:"+str(__indexPi__))
    print("Pre play:"+file)

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
        vlcmedia  = __musicVlcInstance__.media_new(file)
        __musicVlcPi__.set_media(vlcmedia)
        __musicVlcPi__.play()
        __musicPiPlaying__ = True
        print("PlayPause- Play:"+file)
        
def handleMutePi():
    global __musicVlcPi__
    global __radioVlcPi__
    global __volumePi__
    global __volumePiMute__
    if __volumePiMute__ == False :  
        __musicVlcPi__.audio_set_volume(0)
        __radioVlcPi__.audio_set_volume(0)
        __volumePiMute__ = True
    else:
        vlcvolume = __volumePi__
        __musicVlcPi__.audio_set_volume(vlcvolume)
        __radioVlcPi__.audio_set_volume(vlcvolume)
        __volumePiMute__ = False

def handleVolumeDownPi():
    global __musicVlcPi__
    global __radioVlcPi__
    global __volumePi__
    __volumePi__ = __volumePi__ -12
    if __volumePi__ < 0:
        __volumePi__ = 0 
        
    vlcvolume = __volumePi__
    __radioVlcPi__.audio_set_volume(vlcvolume)
    __musicVlcPi__.audio_set_volume(vlcvolume)

def handleVolumeUpPi():
    global __musicVlcPi__
    global __radioVlcPi__
    global __volumePi__
    __volumePi__= __volumePi__ + 12
    if __volumePi__ > 100:
        __volumePi__ = 99 
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
    print(state)
    if (__musicPiPlaying__ == True ):
        if (state == __vlcEnded__):
            handleNextPi();
        threading.Timer( 10 , continuePlaying ).start()
    else:
        threading.Timer( 10 , continuePlaying ).start()


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
    
def downPodcastFile_sh():
    N = 3
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
      command = ["/home/ubuntu/Pi_Media_Server/.venv/bin/python3", "/home/ubuntu/Pi_Media_Server/getpodcast_sh.py"]
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
    GPIO.add_event_detect(37, GPIO.FALLING, callback=handleMutePi, bouncetime=500)
    
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

threading.Timer( 10 , continuePlaying ).start()

#==============================================================================================
app = Flask(__name__)
CORS(app)
#-----------------------
class Config(object):
    SCHEDULER_API_ENABLED = True

scheduler = APScheduler()
#-----------------------
#APScheduler start
app.config.from_object(Config())
# it is also possible to enable the API directly
# scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()
#-----------------------
#==============================================================================================
@app.route('/', methods=['GET', 'POST'])
def index():
    global __dir__
    global __fileList__
    global __indexPi__
    global __musicPiPlaying__ 
    global __musicPiPlayMode__
    global __radioPiPlayingNo__ 
    global __volumePi__
    global __volumePiMute__
    if request.method == 'GET':
        return render_template('index.html')
    if request.method =='POST':
        return jsonify({
        "fileList" : __fileList__,
        "indexPi" : __indexPi__,
        "musicPiPlaying" : __musicPiPlaying__,
        "musicPiPlayMode" : __musicPiPlayMode__,
        "radioPiPlayingNo" : __radioPiPlayingNo__,
        "volumePi" : __volumePi__,
        "volumePiMute" : __volumePiMute__
         })
    
@app.route('/playPrePi', methods=['POST'])
def playPrePi():
    global __indexPi__
    global __indexMax__
    global __musicPiPlaying__
    handlePrePi();
    return jsonify({ 
           "indexPi":__indexPi__,
           "musicPiPlaying" :__musicPiPlaying__
          })
        
@app.route('/playNextPi', methods=['POST'])
def playNextPi():
    global __indexPi__
    global __indexMax__
    global __musicPiPlaying__
    handleNextPi();
    return jsonify({ 
           "indexPi":__indexPi__,
           "musicPiPlaying" :__musicPiPlaying__
          })
    
@app.route('/playSelectedPi', methods=['POST'])
def playSelectedPi():
    global __indexPi__
    global __musicPiPlaying__
    global __indexMax__
    data=request.get_json()
    num=int(data["num"])
    __indexPi__= num % __indexMax__
    handleSelectedPi();
    return jsonify({ 
           "indexPi":__indexPi__,
           "musicPiPlaying" :__musicPiPlaying__
          })

@app.route('/playPausePi', methods=['POST'])
def playPausePi():
    global __musicPiPlaying__
    global __indexPi__
    handlePlayPausePi()
    return jsonify({
        "musicPiPlaying" : __musicPiPlaying__,
        "indexPi" : __indexPi__
         })

@app.route('/setPlayModePi', methods=['POST'])
def setPlayModePi():
    global __musicPiPlayMode__
    data=request.get_json()
    __musicPiPlayMode__=int(data["mode"])
    return jsonify({
        "musicPiPlayMode" : __musicPiPlayMode__
         })
    
@app.route('/playRadioPi', methods=['POST'])
def playRadioPi():
    global __radioVlcInstance__
    global __radioPiPlayingNo__
    global __radioVlcPi__
    global __url__
    data=request.get_json()
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
    return jsonify({
        "radioPiPlayingNo" : __radioPiPlayingNo__
         })

@app.route('/volumeDownPi', methods=['POST'])
def volumeDownPi():
    global __volumePi__
    global __volumePiMute__
    handleVolumeDownPi()
    return jsonify({
        "volumePi" : __volumePi__,
        "volumePiMute" : __volumePiMute__
         })
    
@app.route('/volumeUpPi', methods=['POST'])
def volumeUpPi():
    global __volumePi__
    global __volumePiMute__
    handleVolumeUpPi()
    return jsonify({
        "volumePi" : __volumePi__,
        "volumePiMute" : __volumePiMute__
         })
    
@app.route('/volumeMutePi', methods=['POST'])
def volumeMutePi():
    global __volumePi__
    global __volumePiMute__
    handleMutePi()
    return jsonify({
        "volumePi" : __volumePi__,
        "volumePiMute" : __volumePiMute__
         })
    
@app.route('/getFileList', methods=['POST'])
def getFileList():
    global __fileList__
    global __musicPiPlaying__
    global __indexPi__
    data=request.get_json()
    style=int(data["style"])
    genFileList_sh(style)
    return jsonify({
        "fileList" : __fileList__,
        "musicPiPlaying" : __musicPiPlaying__,
        "indexPi":__indexPi__
         })
    
@app.route('/downPodcastFile', methods=['POST'])
def downPodcastFile():
    global __down_thread__
    global __downStatus__
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
    else:
        print("DonwPodcast thread is Running, please wait")
    return jsonify({
        "downStatus" : __downStatus__
         })


@app.route('/downPodcastFile2', methods=['POST'])
def downPodcastFile2():
    global __down_thread__
    global __downStatus__
    if __downStatus__ == False:
        __downStatus__ = True 
        print("downStatus: "+str(__downStatus__))
        #time.sleep(10)
        __p__=downPodcastFile_sh2()
        monitor_thread = Thread(target=process_monitor,args=(__p__,)) 
        monitor_thread.start()
        print("DownPodcast thread start to run")
        print("DownPodcast thread finished--> downStatus: "+str(__downStatus__))
    else:
        print("DonwPodcast thread is Running, please wait")
        
    return jsonify({
        "downStatus" : __downStatus__
         })





@scheduler.task('cron', id='myjob1', day='*', hour='14', minute='05', second='00')
def myjob1():
    global __indexPi__
    global __indexMax__
    __indexPi__ = 7
    #handleSelectedPi()
    print("myPlayJob executed")

@scheduler.task('cron', id='myjob2', day='*', hour='14', minute='06', second='00')
def myjob2():
    global __indexPi__
    global __indexMax__
    __indexPi__ = 7
    downPodcastFile_sh()
    print("myDownPodcastFileJob executed")
    
    
#parser = argparse.ArgumentParser()
#parser.add_argument("--workers 1 --threads 4,--worker-class gevent", type=str, default=False)
#parser.parse_args()

if __name__ == '__main__':
    #import argparse
    #parser = argparse.ArgumentParser()
    #parser.add_argument("--workers 1 --threads 4,--worker-class gevent", type=str, default=False)
    #parser.parse_args()
    
    app.run(host='0.0.0.0',port=2000,debug=False,threaded=True)
