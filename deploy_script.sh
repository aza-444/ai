#!/bin/bash
set -e

APP_DIR=~/app
REPO_DIR=$APP_DIR

mkdir -p $REPO_DIR
cd $REPO_DIR

if [ ! -d ".git" ]; then
  echo "➡️ Git repo klon qilinyapti..."
  git clone https://github.com/$REPO .
else
  echo "🔄 Mahalliy o‘zgarishlar bekor qilinmoqda va yangilanmoqda..."
  git reset --hard HEAD
  git clean -fd
  git pull origin main
fi

if ! command -v python3 &> /dev/null; then
  echo "❌ python3 topilmadi. Iltimos, uni o'rnating."
  exit 1
fi

if [ ! -d "venv" ]; then
  echo "📦 python3-venv tekshirilmoqda..."
  sudo apt-get update
  sudo apt-get install -y python3-venv

  echo "🐍 Virtual muhit yaratilmoqda..."
  python3 -m venv venv
fi

echo "📦 Kutubxonalar o‘rnatilmoqda..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "⚙️ app.service yozilmoqda..."
sudo tee /etc/systemd/system/app.service > /dev/null <<EOF
[Unit]
Description=App Service
After=network.target

[Service]
User=root
WorkingDirectory=$APP_DIR
Environment=PYTHONPATH=$APP_DIR
ExecStart=$APP_DIR/venv/bin/python app/main.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

echo "🚀 Service ishga tushirilmoqda..."
sudo systemctl daemon-reload
sudo systemctl enable app.service
sudo systemctl restart app.service

echo "✅ Deploy tugadi va app.service ishga tushdi."
echo "⚙️ bot.service yozilmoqda..."
sudo tee /etc/systemd/system/bot.service > /dev/null <<EOF
[Unit]
Description=Bot Service
After=network.target

[Service]
User=root
WorkingDirectory=$APP_DIR
Environment=PYTHONPATH=$APP_DIR
ExecStart=$APP_DIR/venv/bin/python bot/main.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

echo "🚀 Bot ishga tushirilmoqda..."
sudo systemctl daemon-reload
sudo systemctl enable bot.service
sudo systemctl restart bot.service

echo "✅ Bot ham ishga tushdi."
