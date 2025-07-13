#!/bin/bash
set -e

APP_DIR=~/app

# Katalogga kirish yoki yaratish
mkdir -p $APP_DIR
cd $APP_DIR

# Git klonlash yoki yangilash
if [ ! -d ".git" ]; then
  git clone https://github.com/${REPO}.git .
else
  git pull origin main
fi

# Virtual environment yaratish
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# ======== APP SERVICE =========
sudo tee /etc/systemd/system/app.service > /dev/null << EOF
[Unit]
Description=Python App Service
After=network.target

[Service]
User=$USER
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/python app/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# ======== BOT SERVICE =========
sudo tee /etc/systemd/system/bot.service > /dev/null << EOF
[Unit]
Description=Python Bot Service
After=network.target

[Service]
User=$USER
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/python bot/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Servislarni yangilash va ishga tushirish
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable app.service
sudo systemctl enable bot.service
sudo systemctl restart app.service
sudo systemctl restart bot.service

echo "✅ App va Bot servislar muvaffaqiyatli ishga tushdi."
