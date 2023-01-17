#!/usr/bin/env python3
from flask import Flask,render_template,request,jsonify
from flask_cors import CORS
from threading import Thread
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
__mp3_list__ = None
__mp3_list__z__ = None
__mp3_i_max__ = 0
__mp3Pi_i__ = 0
__mp3Pc_i__ = 0 
__num4dPi_i__ = 4
__num4dPi__ = [ 0, 0, 0, 0 ]
__p__ = None
__pty_master__ = None
__pty_slave__ = None
__q__ = None
__qpty_master__ = None
__qpty_slave__ = None
__mpg123Running__ = False  
__return_code__ = None
__radiompg123Running__ = False  
__qreturn_code__ = None
__playingPi__ = False
__timer_running__ = False
__t__ = None
__radioPlayingPiNo__ =  0
__vlc__ = vlc.Instance()
__vlcplayer__ = None
__vlcVolume__ = 75
__vlcVolumeMute__ = False
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
          "url10":"http://192.168.1.192:8000/stream.ogg",
          "url11":"http://onair.family977.com.tw:8000/live.mp3",
          "url12":"https://n09.rcs.revma.com/aw9uqyxy2tzuv?rj-ttl=5&rj-tok=AAABhZollCEACdvxzVVN61ARVg",
          "url13":"https://n10.rcs.revma.com/ndk05tyy2tzuv?rj-ttl=5&rj-tok=AAABhZouFPAAQudE3-49-1PFHQ",
          "url14":"https://n09.rcs.revma.com/7mnq8rt7k5zuv?rj-ttl=5&rj-tok=AAABhZovh0cASZAucd0xcmxkvQ",
          "url15":"https://n11a-eu.rcs.revma.com/em90w4aeewzuv?rj-tok=AAABhZoyef8AtFfbdaYYtKJnaw&rj-ttl=5",
          "url16":"https://n07.rcs.revma.com/78fm9wyy2tzuv?rj-ttl=5&rj-tok=AAABhZozdbQAkV-tPDO6A5aHag",
          "url17":"http://stream.live.vc.bbcmedia.co.uk/bbc_radio_three",
          "url18":"http://stream.live.vc.bbcmedia.co.uk/bbc_radio_fourfm",
          "url19":"http://stream.live.vc.bbcmedia.co.uk/bbc_6music",
          "url20":"http://media-ice.musicradio.com:80/ClassicFMMP3"
          }
url_json=json.dumps(radioUrl)
__url__=json.loads(url_json)

#------------------------------------------------------------------
def play_file(mp3_file, pty):
    try:
        command = ['mpg123', '-C', '-q', mp3_file]
        p = subprocess.Popen( command, 
#                             ['mpg123', # The program to launch in the subprocess
#                             '-C',     # Enable commands to be read from stdin
#                             '-q',     # Be quiet
#                              mp3_file],
                              stdin=pty, # Pipe input via bytes
                              stdout=None,   
                              stderr=None
                              )
        return p
    except FileNotFoundError as e:
        raise AudioEngineUnavailable(f'AudioEngineUnavailable: {e}')

def play_list(mp3_list, pty):
    try:
        command = ['mpg123', '-C', '-q','-z'] + mp3_list
        p = subprocess.Popen( command,
#                              ['mpg123', # The program to launch in the subprocess
#                              '-C',     # Enable commands to be read from stdin
#                              '-q',     # Be quiet
#                              '-z']     # 
#                              +mp3_list,
                              stdin=pty,  # Pipe input via bytes
                              stdout=None,   
                              stderr=None
                              )
        return p
    except FileNotFoundError as e:
        raise AudioEngineUnavailable(f'AudioEngineUnavailable: {e}')
    

# Monitor a subprocess, record its state in global variables
# This function is intended to run in its own thread
def process_monitor(p):
    global __mpg123Running__
    global __return_code__
    # Indicate that the process is running at the start, it
    # should be
    __mpg123Running__ = True
    # When a process exits, p.poll() returns the code it set upon
    # completion
    __return_code__ = p.poll()
    # See whether the process has already exited. This will cause a
    # value (i.e. not None) to return from p.poll()
    if __return_code__ == None:
        # Wait for the process to complete, get its return code directly
        # from the wait() call (i.e. do not use p.poll())
        __return_code__ = p.wait()
    # When we get here, the process has exited and set a return code
    __mpg123Running__ = False
 
def qprocess_monitor(q):
    global __radiompg123Running__
    global __qreturn_code__
    # Indicate that the process is running at the start, it
    # should be
    __radiompg123Running__ = True
    # When a process exits, p.poll() returns the code it set upon
    # completion
    __qreturn_code__ = q.poll()
    # See whether the process has already exited. This will cause a
    # value (i.e. not None) to return from p.poll()
    if __qreturn_code__ == None:
        # Wait for the process to complete, get its return code directly
        # from the wait() call (i.e. do not use p.poll())
        __qreturn_code__ = q.wait()
    # When we get here, the process has exited and set a return code
    __radiompg123Running__ = False
 
 
def vlcprocess_monitor(q):
    global __radiovlcRunning__
    global _vlc_turn_code__
    # Indicate that the process is running at the start, it
    # should be
    __radiovlcRunning__ = True
    # When a process exits, p.poll() returns the code it set upon
    # completion
    __vlcreturn_code__ = q.poll()
    # See whether the process has already exited. This will cause a
    # value (i.e. not None) to return from p.poll()
    if __vlcreturn_code__ == None:
        # Wait for the process to complete, get its return code directly
        # from the wait() call (i.e. do not use p.poll())
        __vlcreturn_code__ = q.wait()
    # When we get here, the process has exited and set a return code
    __radiovlcRunning__ = False
    
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

def playSelected():
    global __p__
    global __playingPi__
    global __dir__
    global __mp3_list__
    global __mpg123Running__
    global __pty_master__
    global __num4dPi__
    global __mp3Pi_i__
    global __num4dPi_i__
    if (__mpg123Running__ == True):
        __p__.terminate() 
        time.sleep(0.1)
    mp3_file = __dir__ + __mp3_list__[__mp3Pi_i__]
    print("play:"+mp3_file)
    __p__ = play_file(mp3_file, __pty_master__)
    monitor_thread = Thread(target=process_monitor,args=(__p__,)) 
    monitor_thread.start()
    __playingPi__ = True
    __timer_running__ = False
    __num4dPi__ = [0, 0, 0, 0]
    __num4dPi_i__ = 4
#Convert int array to decimal interger
def convert(list):
    no = sum(d * 10**i for i, d in enumerate(list[::-1]))
    return(no)

def handleKeyInputPi(channel):
    global __mp3Pi_i__
    global __p__
    global __mp3_i_max__
    global __dir__
    global __playingPi__
    global __num4dPi_i__
    global __num4dPi__
    global __timer_running__
    global __t__
    if (__timer_running__ == True):
        __t__.cancel()
    Number = pressedNumber(channel)
    __num4dPi_i__ = __num4dPi_i__ - 1
    if(__num4dPi_i__ < 0):
        __num4dPi_i__ = 3 
    __num4dPi__[0] = __num4dPi__[1] 
    __num4dPi__[1] = __num4dPi__[2] 
    __num4dPi__[2] = __num4dPi__[3] 
    __num4dPi__[3] = Number 
    num = convert(__num4dPi__)
    __mp3Pi_i__ = ( num % __mp3_i_max__) - 1
    if (__mp3Pi_i__ == -1 ):
       __mp3Pi_i__ = __mp3Pi_i__ + __mp3_i_max__
    print("the NO."+str(__mp3Pi_i__ + 1)+" mp3 will be played")
    __t__ = threading.Timer(3, playSelected)
    __t__.start()
    __timer_running__ = True

def handleNext(channel):
    global __mp3Pi_i__
    global __p__
    global __mp3_i_max__
    global __mp3_list__
    global __dir__
    global __mpg123Running__
    global __playingPi__
    __mp3Pi_i__ = __mp3Pi_i__ + 1
    if (__mp3Pi_i__  > (__mp3_i_max__ -1 )):
        __mp3Pi_i__= 0 
    dir_mp3Pi = __dir__ + __mp3_list__[__mp3Pi_i__]
    print("play:"+dir_mp3Pi)
    if (__mpg123Running__ == True):
        __p__.terminate()   
    __p__ = play_file(dir_mp3Pi, __pty_master__)
    time.sleep(0.1)
    monitor_thread = Thread(target=process_monitor,args=(__p__,)) 
    monitor_thread.start()
    __playingPi__ = True

def handlePre(channel):
    global __mp3Pi_i__
    global __p__
    global __mp3_i_max__
    global __mp3_list__
    global __dir__
    global __mpg123Running__
    global __playingPi__
    __mp3Pi_i__ = __mp3Pi_i__ - 1
    if (__mp3Pi_i__ < 0):
       __mp3Pi_i__= __mp3_i_max__ - 1
    dir_mp3Pi = __dir__ + __mp3_list__[__mp3Pi_i__]
    print("play:"+dir_mp3Pi)
    if (__mpg123Running__ == True):
        __p__.terminate()
    __p__ = play_file(dir_mp3Pi, __pty_master__)
    time.sleep(0.1)
    monitor_thread = Thread(target=process_monitor,args=(__p__,)) 
    monitor_thread.start()
    __playingPi__ = True

def handlePlayPause(channel):
    global __mp3Pi_i__
    global __playingPi__
    global __mpg123Running__
    global __p__
    global __mp3_list__
    time.sleep(0.1)
    if (__mpg123Running__ == True):
        time.sleep(0.1)
        os.write(__pty_slave__, b's')
        __playingPi__ = not __playingPi__
        #__p__.stdin.write(b's')
        #__p__.stdin.flush()
    else:
        mp3Pi = __dir__ + __mp3_list__[__mp3Pi_i__]
        __p__ = play_file(mp3Pi, __pty_master__)
        print("handlePlayPause- play:"+mp3Pi)
        time.sleep(0.1)
        monitor_thread = Thread(target=process_monitor,args=(__p__,)) 
        monitor_thread.start()
        __playingPi__ = True
def handleMute(channel):
    global __playingPi__
    if (__playingPi__ == True):
        os.write(__pty_slave__, b'u')

def handleBack(channel):
    global __playingPi__
    if (__playingPi__ == True):
        os.write(__pty_slave__, b'b')

def get_files(root):
    files = []
    def scan_dir(dir):
        for f in os.listdir(dir):
            #f = os.path.join(dir, f)
            if os.path.isdir(f):
                scan_dir(f)
            elif os.path.splitext(f)[1] == ".mp3":
                files.append(f)
    scan_dir(root)
    return files

def continuePlaying():
    global __playingPi__
    global __mpg123Running__
    global __pty_master__
    global __mp3_list_z__ 
    global __p__
    if (( __mpg123Running__ == False ) and (__playingPi__ == True )):
        handleNext(8888);
        ######if want to play random###but can't trace playing's mp3#####
        #__p__ = play_list(__mp3_list_z__, __pty_master__)
        #time.sleep(0.1)
        #monitor_thread = Thread(target=process_monitor,args=(__p__,)) 
        #monitor_thread.start()
        #__playingPi__ = True
        ######if want to play random###but can't trace playing's mp3#####
        threading.Timer( 5 , continuePlaying ).start()
    else:
        threading.Timer( 5 , continuePlaying ).start()


#---------------------------------------------------------------------------------
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
    GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP)

   #callback function 
    GPIO.add_event_detect(12, GPIO.FALLING, callback=handleKeyInputPi, bouncetime=500)
    GPIO.add_event_detect(16, GPIO.FALLING, callback=handleKeyInputPi, bouncetime=500)
    GPIO.add_event_detect(18, GPIO.FALLING, callback=handleKeyInputPi, bouncetime=500)
    GPIO.add_event_detect(11, GPIO.FALLING, callback=handleKeyInputPi, bouncetime=500)
    GPIO.add_event_detect(13, GPIO.FALLING, callback=handleKeyInputPi, bouncetime=500)
    GPIO.add_event_detect(15, GPIO.FALLING, callback=handleKeyInputPi, bouncetime=500)
    GPIO.add_event_detect(29, GPIO.FALLING, callback=handlePlayPause, bouncetime=500)
    GPIO.add_event_detect(31, GPIO.FALLING, callback=handleNext, bouncetime=500)
    GPIO.add_event_detect(33, GPIO.FALLING, callback=handlePre, bouncetime=500)
    GPIO.add_event_detect(35, GPIO.FALLING, callback=handleBack, bouncetime=500)
    GPIO.add_event_detect(37, GPIO.FALLING, callback=handleMute, bouncetime=500)
    
if(True):
#---------------------------------------------------------------------
#file list Method 1
#    __mp3_list__ = [ f for f in os.listdir(r'./static/assets/.') if f[-4:] == '.mp3' ]
#    mp3_list.sort(key=lambda x:int(x[:-4]))
#--------------------------------------------------------------------
#file list Method 2
    mp3s = []; 
    for path, subdirs, files in os.walk(r'./static/assets'):
       # for name in files:
        path = path[(len(__dir__)-1):];
        path = path+"/";
        path = path[1:];
        files = [path + file for file in files];
        mp3s= mp3s + files; 
    mp3s = [ f for f in mp3s if f[-4:] == '.mp3' ];
    __mp3_list__ = mp3s;

#---------------------------------------------------------------------
#file list Methos 3
    __mp3_list_z__ = glob.glob(r'./static/assets/*.mp3')
#    __mp3_list_z__.sort(key=lambda x:int(x[25:-4]))
#---------------------------------------------------------------------
#file list Method 4
#    __mp3_list__ = get_files(__dir__)
#    __mp3_list__.sort(key=lambda x:int(x[:-4]))
#---------------------------------------------------------------------

    __mp3_i_max__ = len(__mp3_list__) 
    if not (len(__mp3_list__) > 0):
        print ("No mp3 files found!")
    print ('--- Available mp3 files ---')
    print(__mp3_list__)
    __mp3Pi_i__ = random.randrange(__mp3_i_max__)
   # add openpty
    __pty_master__, __pty_slave__ = os.openpty()
    __qpty_master__, __qpty_slave__ = os.openpty()
    __playingPi__ = False
   # We need a way to tell if a song is already playing. Start a 
   # thread that tells if the process is running and that sets
   # a global flag with the process running status.
   #    monitor_thread = Thread(target=process_monitor,args=(__p__,)) 
   #    monitor_thread.start()
   #    time.sleep(0.1)
   #    os.write(__pty_slave__, b's')    
    print ('--- Press button #play to start playing mp3 ---')
    threading.Timer( 5 , continuePlaying ).start()

#==============================================================================================
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    global __dir__
    global __mp3_list__
    global __mp3_i_max__
    global __mp3Pc_i__
    global __mp3Pi_i__
    global __radioPlayingPiNo__ 
    if request.method == 'GET':
        __mp3Pc_i__ = (__mp3Pc_i__+  1 ) % __mp3_i_max__
        print(__mp3Pc_i__)
        mp3Pc = __dir__+ __mp3_list__[__mp3Pc_i__]
        mp3Pi = __dir__+ __mp3_list__[__mp3Pi_i__]
        print(mp3Pc)
        return render_template('index.html')
    if request.method =='POST':
        return jsonify({
        "mp3_list" : __mp3_list__,
        "mp3Pi_i" : __mp3Pi_i__,
        "playingPi" : __playingPi__,
        "radioPlayingPiNo" : __radioPlayingPiNo__
         })
    
@app.route('/playPrePi', methods=['POST'])
def playPrePi():
    global __mp3Pi_i__
    global __mp3_i_max__
    handlePre(8888);
    return jsonify({ 
           "mp3Pi_i":__mp3Pi_i__,
           "playingPi" :__playingPi__
          })
        
@app.route('/playNextPi', methods=['POST'])
def playNextPi():
    global __mp3Pi_i__
    global __mp3_i_max__
    handleNext(8888);
    return jsonify({ 
           "mp3Pi_i":__mp3Pi_i__,
           "playingPi" :__playingPi__
          })
    
@app.route('/playSelectedPi', methods=['POST'])
def playSelectedPi():
    global __mp3Pi_i__
    global __playingPi__
    global __mp3_i_max__
    data=request.get_json()
    num=int(data["num"])
    __mp3Pi_i__= num % __mp3_i_max__
    playSelected();
    return jsonify({ 
           "mp3Pi_i":__mp3Pi_i__,
           "playingPi" :__playingPi__
          })

@app.route('/playPausePi', methods=['POST'])
def playPausePi():
    global __mp3Pi_i__
    global __playingPi__
    global __mpg123Running__
    global __p__
    global __mp3_list__
    time.sleep(0.1)
    if (__mpg123Running__ == True):
        time.sleep(0.1)
        os.write(__pty_slave__, b's')
        __playingPi__ = not __playingPi__
    else:
        file = __dir__ + __mp3_list__[__mp3Pi_i__]
        __p__ = play_file(file, __pty_master__)
        print("play:"+file)
        time.sleep(0.1)
        monitor_thread = Thread(target=process_monitor,args=(__p__,)) 
        monitor_thread.start()
        __playingPi__ = True   
    return jsonify({
        "playingPi" : __playingPi__,
        "mp3Pi_i" : __mp3Pi_i__
         })
#this api use mpg123 to play  stream audio , but mpg123 doesn't fully support all streaming format 
@app.route('/playRadioPi_old', methods=['POST'])
def playRadioPi_old():
    global __q__
    global __qpty_master__
    global __qpty_slave__
    global __radioPlayingPiNo__
    global __radiompg123Running__
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
        case _:
           url ="http://stream.live.vc.bbcmedia.co.uk/bbc_radio_one"
    if(__radiompg123Running__  == True):
        if(radioNo == 0):
            os.write(__qpty_slave__, b's')
            __radioPlayingPiNo__ = 0
        elif(radioNo == __radioPlayingPiNo__):
            os.write(__qpty_slave__, b's')
            __radioPlayingPiNo__ = radioNo
        else:
            __q__.terminate()   
            __q__ = play_file(url, __qpty_master__)
            time.sleep(0.1)
            qmonitor_thread = Thread(target=qprocess_monitor,args=(__q__,)) 
            qmonitor_thread.start()
            __radioPlayingPiNo__ = radioNo
    else:
        __q__ = play_file(url, __qpty_master__)
        time.sleep(0.1)
        qmonitor_thread = Thread(target=qprocess_monitor,args=(__q__,)) 
        qmonitor_thread.start()
        __radioPlayingPiNo__ = radioNo
    return jsonify({
        "radioPlayingPiNo" : __radioPlayingPiNo__,
         })


@app.route('/playRadioPi', methods=['POST'])
def playRadioPi():
    global __vlc__
    global __radioPlayingPiNo__
    global __vlcplayer__
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
        case _:
           url ="https://stream.live.vc.bbcmedia.co.uk/bbc_world_service"
    if(radioNo == 0):
        __vlcplayer__.stop()
        __radioPlayingPiNo__ = 0
    else:
        if(__radioPlayingPiNo__ != 0):
           __vlcplayer__.stop()
        __vlcplayer__ = __vlc__.media_player_new()
        print("url"+url)        
        vlcmedia  = __vlc__.media_new(url)
        __vlcplayer__.set_media(vlcmedia)
        __vlcplayer__.play()
        __radioPlayingPiNo__ = radioNo
    return jsonify({
        "radioPlayingPiNo" : __radioPlayingPiNo__,
         })

@app.route('/volumeDownPi', methods=['POST'])
def volumeDownPi():
    global __vlc__
    global __radioPlayingPiNo__
    global __vlcplayer__
    global __vlcVolume__
    __vlcVolume__ = __vlcVolume__ -  10
    if __vlcVolume__ < 0:
        __vlcVolume__ = 0 
    __vlcplayer__.audio_set_volume(__vlcVolume__)
    return jsonify({
         })
    
@app.route('/volumeUpPi', methods=['POST'])
def volumeUpPi():
    global __vlc__
    global __radioPlayingPiNo__
    global __vlcplayer__
    global __vlcVolume__
    __vlcVolume__= __vlcVolume__ + 10
    if __vlcVolume__ > 100:
        __vlcVolume__ = 99 
    __vlcplayer__.audio_set_volume(__vlcVolume__)
    return jsonify({
         })
    
@app.route('/volumeMutePi', methods=['POST'])
def volumeMutePi():
    global __vlc__
    global __radioPlayingPiNo__
    global __vlcplayer__
    global __vlcVolume__
    global __vlcVolumeMute__
    if __vlcVolumeMute__ == False :  
        __vlcplayer__.audio_set_volume(0)
        __vlcVolumeMute__ = not __vlcVolumeMute__
    else:
        __vlcplayer__.audio_set_volume(__vlcVolume__)
        __vlcVolumeMute__ = not __vlcVolumeMute__
    return jsonify({
         })
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=2000,debug=True)
