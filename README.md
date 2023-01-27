#Install required software
$ sudo apt install nginx
$ sudo apt install python3
$ sudo apt install python3-pip
$ sudo apt install mpg123
$ sudo apt install vlc
$ sudo apt install gunicorn

$ pip3 install virtualenv

#Chceck Version
$ virtualenv --version

#crear Virtual enviroment
$ python3 -m venv .venv                     or      $ virtualenv venv ? 

#Activae or Deactivate enviroment
$ source ./.ven/bin/activate 

#pip3 install packages
$ pip3 install -r requirements.txt
[
flask
wheel
gunicorn[gevent]
flask_apscheduler
pip install flask[async] 
]
----------------------------------------
#nginx configure
$ sudo nano /etc/nginx/sites-available/pimediaserver.conf
$ sudo ln -s /etc/nginx/sites-available/pimediaserver.conf /etc/nginx/sites-enabled/

ref: https://www.edmondchuc.com/blog/deploying-python-flask-with-gunicorn-nginx-and-systemd

# vi /etc/group  add ubuntu to www-data, add www-data to ubuntu 
#gunicorn

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
