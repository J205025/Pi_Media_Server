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
----------------------------------------
#nginx configure
$ sudo nano /etc/nginx/sites-available/pimediaserver.conf
$ sudo ln -s /etc/nginx/sites-available/pimediaserver.conf /etc/nginx/sites-enabled/

ref: https://www.edmondchuc.com/blog/deploying-python-flask-with-gunicorn-nginx-and-systemd

# vi /etc/group  add ubuntu to www-data, add www-data to ubuntu 
#gunicorn

#systemd service

# put music file at /home/ubuntu/Music/


# Description 
Music player with 1. play on client_PC and 2. play on server_Raspberry  of the Server music Files
