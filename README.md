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
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.2/install.sh | bash
\. "$HOME/.nvm/nvm.sh"
nvm install 22
npm i -g pm2
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