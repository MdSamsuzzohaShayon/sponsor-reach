#!/bin/bash

set -euo pipefail

LOG_FILE="$HOME/sponsor_reach_update.log"
REPO_URL="git@github.com:MdSamsuzzohaShayon/sponsor-reach.git"
PROJECT_DIR="$HOME/sponsor-reach"
CLIENT_DEST="/var/www/client"
ENV_FILE="$PROJECT_DIR/.env"

echo "===== $(date): Starting sponsor_reach update (Auto deploy script) =====" | tee -a "$LOG_FILE"

# Function to log and exit on error
error_exit() {
    echo "[ERROR] $1" | tee -a "$LOG_FILE"
    exit 1
}

# Log current journal output
echo "[INFO] Logging previous service logs..." | tee -a "$LOG_FILE"
journalctl -u sponsor_reach.service -n 50 --no-pager | tee -a "$LOG_FILE" || echo "[WARN] Unable to read journal logs"

# Clean previous files
echo "[INFO] Cleaning old project..." | tee -a "$LOG_FILE"
rm -rf "$PROJECT_DIR" || error_exit "Failed to remove old project directory"

# Clone the repository
echo "[INFO] Cloning repository..." | tee -a "$LOG_FILE"
git clone "$REPO_URL" "$PROJECT_DIR" || error_exit "Failed to clone repository"

# Copy client folder to /var/www
echo "[INFO] Copying client folder..." | tee -a "$LOG_FILE"
sudo cp -r "$PROJECT_DIR/client" "$CLIENT_DEST" || error_exit "Failed to copy client folder"

# Activate virtual environment
cd "$PROJECT_DIR" || error_exit "Failed to cd into project directory"

echo "[INFO] Switching to master branch..." | tee -a "$LOG_FILE"
git switch master || error_exit "Failed to switch to master branch"

echo "[INFO] Creating virtual environment..." | tee -a "$LOG_FILE"
python3 -m venv .venv || error_exit "Failed to create virtual environment"

source .venv/bin/activate || error_exit "Failed to activate virtual environment"

# Create .env file
nano $ENV_FILE || error_exit "Failed to create dot env file"

pip install -r requirements.txt || error_exit "Failed to install required files"

# Restart systemd service
echo "[INFO] Reloading systemd and restarting service..." | tee -a "$LOG_FILE"
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl restart sponsor_reach.service || error_exit "Failed to restart sponsor_reach.service"

# Final status and logs
echo "[INFO] Service status:" | tee -a "$LOG_FILE"
systemctl status sponsor_reach.service --no-pager | tee -a "$LOG_FILE"

echo "[INFO] Latest service logs:" | tee -a "$LOG_FILE"
journalctl -u sponsor_reach.service -n 30 --no-pager | tee -a "$LOG_FILE"

echo "===== $(date): sponsor_reach update completed =====" | tee -a "$LOG_FILE"


# To Edit
# sudo nano /etc/systemd/system/sponsor_reach.timer
# sudo nano /etc/systemd/system/sponsor_reach.service
# systemctl list-timers --all | grep sponsor_reach
# nano /etc/systemd/system/sponsor_reach.timer
# sudo nano /etc/systemd/system/sponsor_reach.timer
# sudo systemctl daemon-reload
# sudo systemctl enable sponsor_reach.timer
# sudo systemctl start sponsor_reach.timer
# systemctl list-timers --all | grep sponsor_reach
# journalctl -u sponsor_reach.service --since "1 hour ago" --no-pager



