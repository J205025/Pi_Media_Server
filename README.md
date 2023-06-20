STEP-1: Install python3 and required packages*******
#Install required software
$ sudo apt install python3
$ sudo apt install python3.11-venv
$ python3 -m venv .venv                    
#Activae virtual enviroment
$ source ./.ven/bin/activate 
$ sudo apt install python3-pip
$ pip3 install flask
$ pip3 install flask_apscheduler
$ pip3 install flask_cors
$ pip3 install rpi.gpio
$ pip3 install python-vlc
$ pip3 install getpodcast
$ sudo apt install gunicorn  
$ pip3 install gunicorn
$ pip3 install gunicorn[gevent]
$ sudo apt install python3-rpi.gpio
$ sudo apt install nginx
$ sudo apt install vlc
$ sudo apt install pulseaudio


----------------------------------------
#nginx configure
$ sudo cp nginx_flask.conf /etc/nginx/sites-available/
$ sudo ln -s /etc/nginx/sites-available/nginx_flask.conf /etc/nginx/sites-enabled/
ref: https://www.edmondchuc.com/blog/deploying-python-flask-with-gunicorn-nginx-and-systemd

# vi /etc/group  add ubuntu to www-data, add www-data to ubuntu 

#systemd service

# put music file at ./static/assets/

------------------------------------------------------
#mp3 file name space 
# remove space of filename
$ sudo apt install rename
# do the directories first 
$ find . -name "* *" -type d | rename 's/ /_/g'
# do the files then 
$ find . -name "* *" -type f | rename 's/ /_/g'
-----------------------------------------------------
# Description 
Music player with 1. play on client_PC and 2. play on server_Raspberry  of the Server music Files

# mount mp3 USB Drive to /media/usb1/
$sudo lsblk -o NAME,FSTYPE,UUID,MOUNTPOINTS

$ sudo vi /etc/fstab
UUID=E654-E418 /media/usb1/ vfat umask=0022,gid=1000,uid=1000,iocharset=utf8  0	0

$ sudo findmnt --verify


#samba add share folder [usb1] 
$ sudo vi /etc/samba/smb.conf  , add the following text at the  bottom of the file
[usb1]
path = /media/usb1
available = yes
browseable = yes
public = yes
writable = yes

#samba add user "ubuntu"
$ sudo pdbedit -a -u ubuntu

#mp3 volume modifification
$ sudo apt install mp3gain
- 將所有的 Mp3 音量 調整到預設 89db: 
$ sudo mp3gain -a -r -k *.mp3
-若嫌太小聲, 要調大聲到 99 db 的話, 使用 -d 10 即可: 
$ sudo mp3gain -a -r -k -d 10 *.mp3
$ sudo mp3gain -r -d 5 *.mp3 增加/減少音量 
ref:
https://www.linux.com/news/adjusting-mp3s-mp3gain/
