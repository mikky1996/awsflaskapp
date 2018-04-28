# awsflaskapp
## 1 step:
Create EC2 instance
## 2 step:
$ sudo apt-get update
$ sudo apt-get install apache2
$ sudo apt-get install libapache2-mod-wsgi
## 3 step:
$ sudo apt-get install python-pip
$ sudo pip install flask
## 4 step:
$ mkdir ~/flaskapp
$ sudo ln -sT ~/flaskapp /var/www/html/flaskapp
## 5 step:
$ cd ~/flaskapp
$ echo "Hello World" > index.html
## 6 step:
$ git clone https://github.com/mikky1996/awsflaskapp.git
## 7 step:
$ vim /etc/apache2/sites-enabled/000-default.conf

add:

WSGIDaemonProcess flaskapp threads=5
WSGIScriptAlias / /var/www/html/flaskapp/flaskapp.wsgi
<Directory flaskapp>
    WSGIProcessGroup flaskapp
    WSGIApplicationGroup %{GLOBAL}
    Order deny,allow
    Allow from all
</Directory>

after the line: DocumentRoot /var/www/html

## 8 step
$ sudo apachectl restart #do it each time you make changes to the sever

# More exact instructions
https://www.datasciencebytes.com/bytes/2015/02/24/running-a-flask-app-on-aws-ec2/
