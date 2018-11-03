# b1oki.noip.me
#### LSD [Local Server Dedicated] Pages

Required python3 pip3 virtualenv nginx uwsgi uwsgi-plugin-python3

###### prepare enviroment
Copy files to ~/server/lsd
```
cd ~/server/lsd
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip install flask
deactivate
```
###### setup server
```
sudo ln -s ~/server/lsd/lsd_nginx.conf /etc/nginx/sites-available/lsd_nginx.conf
sudo ln -s /etc/nginx/sites-available/lsd_nginx.conf /etc/nginx/sites-enabled/lsd_nginx.conf
sudo ln -s ~/server/lsd/lsd_uwsgi.ini /etc/uwsgi/apps-available/lsd_uwsgi.ini
sudo ln -s /etc/uwsgi/apps-available/lsd_uwsgi.ini /etc/uwsgi/apps-enabled/lsd_uwsgi.ini
sudo service uwsgi restart
sudo service nginx reload
```
###### ssl let's encrypt
```
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:certbot/certbot
sudo apt update
sudo apt install python-certbot-nginx
sudo certbot --nginx
```
