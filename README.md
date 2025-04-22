# Crowd Poetry

A crowd-sourced, text-to-sound synthesis project.

```bash
# Pseudo Playbook, Assume Debian 12

# Common
sudo apt update
sudo apt upgrade -y
curl -sSL https://install.python-poetry.org | python3 -
echo export PATH="~/.local/bin:$PATH" > ~/.bashrc
sudo apt install git -y
git clone https://github.com/stockhuman/crowd-poetry.git

# Service (Web interface, DB) only
sudo apt install ffmpeg nginx certbot python3-certbot-nginx ufw -y
mkdir -p ~/crowd-poetry/app/python/vosk_models
cd ~/crowd-poetry/app/python/vosk_models
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
rm vosk-model-small-en-us-0.15.zip
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.2/install.sh | bash
\. "$HOME/.nvm/nvm.sh"
nvm install 22
npm i -g pm2
sudo mkdir -p /var/www/crowd-poetry
sudo cp -r ~/crowd-poetry/app/web/dist/* /var/www/crowd-poetry/
sudo chown -R www-data:www-data /var/www/crowd-poetry
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
# Write Nginx reverse proxy config, or build and serve manually
echo "server {
  listen 80;
  server_name crowd-poetry.michaelhemingway.com;
  location / {
    proxy_pass http://127.0.0.1:3001;
    proxy_http_version 1.1;
    proxy_set_header Upgrade \$http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host \$host;
    proxy_cache_bypass \$http_upgrade;
  }
}" | sudo tee /etc/nginx/sites-available/crowd-poetry
sudo ln -s /etc/nginx/sites-available/crowd-poetry /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
sudo certbot --nginx -d crowd-poetry.michaelhemingway.com
# Development only, for manually placing files
cd /etc/avahi/services/
sudo wget -c https://raw.githubusercontent.com/lathiat/avahi/master/avahi-daemon/sftp-ssh.service
sudo sudo wget -c https://raw.githubusercontent.com/lathiat/avahi/master/avahi-daemon/ssh.service
service avahi-daemon restart

# Audio device only - install on device producing the sound only
sudo apt install supercollider sc3-plugins supercollider-language jackd -y
sudo alsactl store
sudo systemctl enable alsa-restore
echo /usr/bin/jackd -P75 -dalsa -dhw:0 -r44100 -p1024 -n3 -o2 -sz > ~/.jackdrc
echo export QT_QPA_PLATFORM=offscreen > ~/.bashrc
source ~/.bashrc
```