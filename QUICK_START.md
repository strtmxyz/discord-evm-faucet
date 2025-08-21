# 🚀 Quick Start - Deploy Discord EVM Faucet Bot

## ⚡ Deploy in 5 minutes

### 1. Create EC2 Instance
- **AMI**: Ubuntu 22.04 LTS
- **Type**: t2.micro (Free tier)
- **Storage**: 8GB
- **Security Groups**: SSH (22), HTTP (80), HTTPS (443)

### 2. SSH Connection
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

### 3. Run Auto-Deploy Script
```bash
# Clone repository
git clone https://github.com/your-username/discord-evm-faucet.git
cd discord-evm-faucet

# Run deploy script
chmod +x deploy.sh
./deploy.sh
```

### 4. Configure Bot
```bash
# Edit .env file
nano .env

# Update the following information:
# - HTTP_PROVIDER (Infura URL)
# - SENDER_ADDRESS (sender wallet)
# - PRIVATE_KEY (private key)
# - DISCORD_TOKEN (Discord bot token)
```

### 5. Start Bot
```bash
# Start service
sudo systemctl start discord-bot

# Check status
sudo systemctl status discord-bot

# View logs
sudo journalctl -u discord-bot -f
```

## 🔧 Discord Bot Configuration

1. Visit [Discord Developer Portal](https://discord.com/developers/applications)
2. Create new Application
3. Go to Bot section → Copy Token
4. Enable permissions: Send Messages, Use Slash Commands
5. Invite bot to server using OAuth2 URL

## 📋 Quick Checklist

- [ ] EC2 instance created
- [ ] Deploy script executed
- [ ] .env file configured
- [ ] Discord bot token set
- [ ] Bot started successfully
- [ ] Test `/faucet` command in Discord

## 🚨 Quick Troubleshooting

**Bot cannot connect:**
```bash
sudo journalctl -u discord-bot -f
# Check Discord token and internet connection
```

**Bot crashes:**
```bash
sudo systemctl restart discord-bot
sudo journalctl -u discord-bot -p err
```

**Update bot:**
```bash
cd ~/discord-bot/discord-evm-faucet
git pull
sudo systemctl restart discord-bot
```

## 📚 Detailed Documentation

See `AWS_EC2_DEPLOYMENT_GUIDE.md` for more details about:
- Security configuration
- Monitoring and maintenance
- Detailed troubleshooting
- Cost optimization

---

**🎯 Goal**: Bot will send **0.1 native tokens** to each user every 24 hours via `/faucet` command
