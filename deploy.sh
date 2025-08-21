#!/bin/bash

# Discord EVM Faucet Bot - Auto Deployment Script
# Usage: chmod +x deploy.sh && ./deploy.sh

set -e  # Exit on any error

echo "🚀 Starting Discord EVM Faucet Bot deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}❌ Do not run this script as root!${NC}"
   exit 1
fi

# Update system
echo -e "${YELLOW}📦 Updating system...${NC}"
sudo apt update && sudo apt upgrade -y

# Install dependencies
echo -e "${YELLOW}🔧 Installing dependencies...${NC}"
sudo apt install -y python3 python3-pip python3-venv git curl wget

# Create bot directory
echo -e "${YELLOW}📁 Creating bot directory...${NC}"
mkdir -p ~/discord-bot
cd ~/discord-bot

# Check if repository exists
if [ -d "discord-evm-faucet" ]; then
    echo -e "${YELLOW}🔄 Updating repository...${NC}"
    cd discord-evm-faucet
    git pull origin main
else
    echo -e "${YELLOW}📥 Cloning repository...${NC}"
    git clone https://github.com/your-username/discord-evm-faucet.git
    cd discord-evm-faucet
fi

# Create virtual environment
echo -e "${YELLOW}🐍 Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo -e "${YELLOW}📦 Installing Python packages...${NC}"
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚙️ Creating .env file...${NC}"
    cat > .env << EOF
# Ethereum Provider URL
HTTP_PROVIDER=https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID

# Sender wallet address
SENDER_ADDRESS=0xYourSenderAddressHere

# Sender wallet private key
PRIVATE_KEY=YourPrivateKeyHere

# Chain ID (Sepolia testnet = 11155111, Mainnet = 1)
CHAIN_ID=11155111

# Discord Bot Token
DISCORD_TOKEN=YourDiscordBotTokenHere
EOF
    echo -e "${RED}⚠️  Please update .env file with actual information!${NC}"
    echo -e "${YELLOW}📝 Use: nano .env${NC}"
else
    echo -e "${GREEN}✅ .env file already exists${NC}"
fi

# Create systemd service
echo -e "${YELLOW}🔧 Creating systemd service...${NC}"
sudo tee /etc/systemd/system/discord-bot.service > /dev/null << EOF
[Unit]
Description=Discord EVM Faucet Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/discord-bot/discord-evm-faucet
Environment=PATH=$HOME/discord-bot/discord-evm-faucet/venv/bin
ExecStart=$HOME/discord-bot/discord-evm-faucet/venv/bin/python3 bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable service
echo -e "${YELLOW}🚀 Enabling service...${NC}"
sudo systemctl daemon-reload
sudo systemctl enable discord-bot

# Set proper permissions for .env file
echo -e "${YELLOW}🔒 Setting file permissions...${NC}"
chmod 600 .env

# Create backup
cp .env .env.backup

echo -e "${GREEN}✅ Deployment completed!${NC}"
echo ""
echo -e "${YELLOW}📋 Next steps:${NC}"
echo "1. Update .env file with actual information"
echo "2. Start bot: sudo systemctl start discord-bot"
echo "3. Check status: sudo systemctl status discord-bot"
echo "4. View logs: sudo journalctl -u discord-bot -f"
echo ""
echo -e "${GREEN}🎉 Bot is ready to run!${NC}"
