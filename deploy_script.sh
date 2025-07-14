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
#
#if [ ! -d "venv" ]; then
#  python3 -m venv venv
#fi
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt


sudo systemctl daemon-reload
sudo systemctl enable app.service
sudo systemctl enable bot.service
sudo systemctl restart app.service
sudo systemctl restart bot.service

echo "✅ App va Bot servislar ishga tushdi."
