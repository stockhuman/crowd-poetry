# Crowd Poetry

A crowd-sourced, text-to-sound synthesis project.

```bash
# Pseudo Ansible script
sudo apt update
sudo apt upgrade -y
sudo apt install supercollider sc3-plugins supercollider-language jackd git -y
cd /etc/avahi/services/
sudo wget -c https://raw.githubusercontent.com/lathiat/avahi/master/avahi-daemon/sftp-ssh.service
sudo sudo wget -c https://raw.githubusercontent.com/lathiat/avahi/master/avahi-daemon/ssh.service
service avahi-daemon restart
sudo alsactl store
sudo systemctl enable alsa-restore
echo /usr/bin/jackd -P75 -dalsa -dhw:0 -r44100 -p1024 -n3 -o2 -sz > ~/.jackdrc
echo export QT_QPA_PLATFORM=offscreen > ~/.bashrc
echo export PATH="~/.local/bin:$PATH" > ~/.bashrc
curl -sSL https://install.python-poetry.org | python3 -
source ~/.bashrc
git clone https://github.com/stockhuman/crowd-poetry.git
```