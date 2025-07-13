#!/bin/bash
set -e

APP_DIR=~/app

mkdir -p $APP_DIR
cd $APP_DIR

if [ ! -d ".git" ]; then
  git clone https://github.com/$REPO .
else
  git pull origin main
fi

if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

sudo tee /etc/systemd/system/app.service > /dev/null <<EOF
[Unit]
Description=App Service
After=network.target

[Service]
User=$USER
WorkingDirectory=$APP_DIR
Environment=PYTHONPATH=$APP_DIR
ExecStart=$APP_DIR/venv/bin/python app/main.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable app.service
sudo systemctl restart app.service
