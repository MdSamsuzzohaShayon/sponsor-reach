!/bin/bash

# Logs
journalctl -u sponsor_reach.service

# Delete previous file
cd
rm -rf sponsor-reach

# Clone github repository
git clone git@github.com:MdSamsuzzohaShayon/sponsor-reach.git

# Copy client folder
cp -r sponsor-reach/client /var/www/

# Create and activate virtual environment
cd sponsor-reach
python -m venv .venv
source .venv/bin/activate

# Setup Environment variable
nano .env



# Systemd Logs
journalctl -u sponsor_reach.service
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl restart sponsor_reach.service
systemctl status sponsor_reach.service
journalctl -u sponsor_reach.service -e

# To Edit
# sudo nano /etc/systemd/system/sponsor_reach.timer
# sudo nano /etc/systemd/system/sponsor_reach.service
# systemctl list-timers --all | grep sponsor_reach


