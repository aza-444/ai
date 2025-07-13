#!/bin/bash
set -e

APP_DIR=~/app
REPO="aza-444/ai"

# 1. Katalogni tayyorlash
mkdir -p $APP_DIR
cd $APP_DIR

# 2. Git klonlash yoki pull qilish
if [ ! -d ".git" ]; then
  echo "ℹ️ .git mavjud emas, klon qilinmoqda..."
  git clone https://github.com/$REPO .  # "." bu joriy papkaga klon qiladi
else
  echo "🔄 .git mavjud, kod yangilanmoqda..."
  git reset --hard
  git clean -fd
  git pull origin main
fi

# 3. Virtual environment
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 4. Systemd servislar
sudo tee /etc/systemd/system/app.service > /dev/null << EOF
[Unit]
Description=App service
After=network.target

[Service]
User=$USER
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/python app/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo tee /etc/systemd/system/bot.service > /dev/null << EOF
[Unit]
Description=Bot service
After=network.target

[Service]
User=$USER
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/python bot/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 5. Servislarni yangilash va ishga tushirish
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable app.service
sudo systemctl enable bot.service
sudo systemctl restart app.service
sudo systemctl restart bot.service

echo "✅ App va Bot servislar muvaffaqiyatli ishga tushdi."
