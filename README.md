#Install required software
$ sudo apt install nginx
$ sudo apt install python3
$ sudo apt install python3-pip
$ pip3 install virtualenv
#Chceck Version
$ virtualenv --version
#crear Virtual enviroment
$ python3 -m venv .venv ?
or
$ virtualenv venv ? 
#Activae or Deactivate enviroment
$ source ./.ven/bin/activate 
#pip3 install packages
$ pip install -r requirements.txt
----------------------------------------
#nginx configure
$ sudo nano /etc/nginx/sites-available/pimediaserver.conf
$ sudo ln -s /etc/nginx/sites-available/pimediaserver.conf /etc/nginx/sites-enabled/
ref: https://www.edmondchuc.com/blog/deploying-python-flask-with-gunicorn-nginx-and-systemd
#gunicorn
#systemd service

$ gunicorn -w 4 --bind 0.0.0.0:8000 wsgi:app


# Description 
Music player with 1. play on client_PC and 2. play on server_Raspberry  of the Server music Files
