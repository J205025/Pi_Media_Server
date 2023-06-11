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
$ pip3 install gunicorn
$ sudo apt install libffi-dev
$ pip3 install gevent
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
