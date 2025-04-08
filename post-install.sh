#!/bin/bash

# Instala o Node.js (Linux/Ubuntu)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verifica a instalação
node -v
npm -v

# Instala o pacote necessário para o pytubefix
npm install youtube-po-token-generator

python -m nodeenv -p