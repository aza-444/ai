#!/bin/bash
set -e

APP_DIR=$(realpath ~/app)
REPO="aza-444/ai"
USER_NAME=$(whoami)

mkdir -p $APP_DIR
cd $APP_DIR

if [ -d ".git" ]; then
  echo "🔄 .git mavjud, yangilanmoqda..."
  git reset --hard
  git clean -fd
  git pull origin main
else
  echo "🧹 Katalog tozalanmoqda va klon qilinmoqda..."
  rm -rf ./*
  git clone https://github.com/$REPO .
fi

if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt


sudo tee /etc/systemd/system/app.service > /dev/null << EOF
[Unit]
Description=App Service
After=network.target

[Service]
User=$USER_NAME
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/python app/app/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo tee /etc/systemd/system/bot.service > /dev/null << EOF
[Unit]
Description=Bot Service
After=network.target

[Service]
User=$USER_NAME
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/python bot/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable app.service
sudo systemctl enable bot.service
sudo systemctl restart app.service
sudo systemctl restart bot.service

echo "✅ App va Bot servislar ishga tushdi."
