# b1oki.noip.me
#### LSD [Local Server Dedicated] Pages

Required python3 pip3 virtualenv nginx

###### prepare enviroment
Copy files to /home/sav/server/lsd
```
cd /home/sav/server/lsd
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip install flask uwsgi
deactivate
```
###### setup server
```
sudo ln -s ~/server/lsd/lsd_nginx.conf /etc/nginx/sites-available/lsd_nginx.conf
sudo ln -s /etc/nginx/sites-available/lsd_nginx.conf /etc/nginx/sites-enabled/lsd_nginx.conf
sudo ln -s ~/server/lsd/lsd_uwsgi.service /etc/systemd/system/lsd_uwsgi.service
sudo service nginx reload
sudo systemctl start lsd_uwsgi.service
sudo systemctl enable lsd_uwsgi.service
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

###### logging
```
sudo systemctl status lsd_uwsgi.service
sudo journalctl -u lsd_uwsgi.service
/var/log/nginx/lsd_access.log
/var/log/nginx/lsd_error.log
```
