# Getting to a running FLask instance on EC2

```
sudo apt-get update
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi
python --version
python3 --version
alias python python3
alias python3 python
sudo apt-get install python-pip3
sudo apt-get install python-pip
pip list
pip3 list
sudo apt-get install python3-pip
sudo apt-get install libapache2-mod-wsgi-py3
pip3 --version
pip3 install flask
mkdir flaskapp
sudo ln -sT ~/flaskapp /var/www/html/flaskapp
cd flaskapp/
echo "Hello Mike" > index.html
nano flaskapp.py
nano flaskapp.wsgi
sudo nano /etc/apache2/sites-enabled/000-default.conf
sudo service apache2 restart
```
