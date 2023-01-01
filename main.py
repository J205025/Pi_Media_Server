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
__mpg123Running__ = False  
__return_code__ = None
__playingPi__ = False
__timer_running__ = False
__t__ = None
__radioPlayingPiNo__ =  0
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
        print("play:"+mp3Pi)
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
   # PLAY NEXT PRE BACK 
    GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    threading.Timer( 5 , continuePlaying ).start()
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
   # __mp3Pc_i__ = random.randrange(__mp3_i_max__)
    __mp3Pi_i__ = random.randrange(__mp3_i_max__)
   # add openpty
    __pty_master__, __pty_slave__ = os.openpty()
    __playingPi__ = False
   # We need a way to tell if a song is already playing. Start a 
   # thread that tells if the process is running and that sets
   # a global flag with the process running status.
   #    monitor_thread = Thread(target=process_monitor,args=(__p__,)) 
   #    monitor_thread.start()
   #    time.sleep(0.1)
   #    os.write(__pty_slave__, b's')    
    print ('--- Press button #play to start playing mp3 ---')
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
        "playingPi" : __playingPi__
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
    ########################################
    data=request.get_json()
    num=int(data["num"])
    __mp3Pi_i__= num % __mp3_i_max__
    playSelected();
   #######################################
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

@app.route('/playRadioPi', methods=['POST'])
def playRadioPi():
    global __playingPi__
    global __mpg123Running__
    global __p__
    global __pty_master__
    global __radioPlayingPiNo__
    data=request.get_json()
    radioNo=int(data["radioNo"])
    if(__radioPlayingPiNo__ == radioNo ):
        os.write(__pty_slave__, b's')
        __radioPlayingPiNo__ = 0
        __playingPi__ = False
    else:
        url ="http://stream.live.vc.bbcmedia.co.uk/bbc_radio_one"
        if (__mpg123Running__ == True):
            __p__.terminate()   
            __playingPi__ = False
            __radioPlayingPiNo__ = 0
        __p__ = play_file(url, __pty_master__)
        time.sleep(0.1)
        monitor_thread = Thread(target=process_monitor,args=(__p__,)) 
        monitor_thread.start()
        __radioPlayingPiNo__ = radioNo
        __playingPi__ = True
    return jsonify({
        "radioPlayingPiNo" : __radioPlayingPiNo__,
        "playingPi" : __playingPi__,
         })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2000,debug=True)
