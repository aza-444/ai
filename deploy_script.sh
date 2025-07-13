#!/bin/bash
set -e

APP_DIR=~/app
REPO_DIR=$APP_DIR

echo "📁 Papkalar tayyorlanmoqda..."
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

echo "🐍 Python mavjudligi tekshirilmoqda..."
if ! command -v python3 &> /dev/null; then
  echo "❌ python3 topilmadi. Iltimos, o‘rnating."
  exit 1
fi

echo "📦 python3-venv o‘rnatilishi tekshirilmoqda..."
sudo apt-get update
sudo apt-get install -y python3-venv

if [ ! -d "venv" ]; then
  echo "🧪 Virtual muhit yaratilmoqda..."
  python3 -m venv venv
fi

if [ ! -f "venv/bin/activate" ]; then
  echo "❌ venv yaratishda muammo: 'venv/bin/activate' topilmadi."
  exit 1
fi

echo "📦 Kutubxonalar o‘rnatilmoqda..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "⚙️ app.service fayli yozilmoqda..."
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

echo "🚀 app.service ishga tushirilmoqda..."
sudo systemctl daemon-reload
sudo systemctl enable app.service
sudo systemctl restart app.service

echo "✅ App servisi ishga tushdi."

echo "⚙️ bot.service fayli yozilmoqda..."
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

echo "🚀 bot.service ishga tushirilmoqda..."
sudo systemctl daemon-reload
sudo systemctl enable bot.service
sudo systemctl restart bot.service

echo "✅ Bot servisi ishga tushdi."
