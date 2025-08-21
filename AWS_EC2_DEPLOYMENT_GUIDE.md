# AWS EC2 Deployment Guide for Discord EVM Faucet Bot

## 📋 Prerequisites

- AWS account with EC2 access permissions
- Discord Bot Token (from Discord Developer Portal)
- Ethereum wallet address and private key
- Infura API key or other Ethereum node provider

---

## 🚀 Step 1: Create EC2 Instance

### 1.1 Access AWS Console
- Visit [AWS Console](https://console.aws.amazon.com/)
- Select the nearest region (e.g., Asia Pacific - Singapore)

### 1.2 Launch EC2 Instance
1. **Choose AMI**: Ubuntu Server 22.04 LTS (Free tier)
2. **Instance Type**: t2.micro (Free tier) or t3.small for production
3. **Configure Instance**:
   - Network: Default VPC
   - Subnet: Auto-assign Public IP
4. **Storage**: 8GB (sufficient for bot and dependencies)
5. **Security Groups**: Create new with these rules:
   ```
   SSH (22): 0.0.0.0/0 (Your IP only for production)
   HTTP (80): 0.0.0.0/0
   HTTPS (443): 0.0.0.0/0
   Custom TCP (3000): 0.0.0.0/0 (if other port needed)
   ```

### 1.3 Create Key Pair
- Create new key pair or use existing one
- Download .pem key file

---

## 🔧 Step 2: Connect and Setup EC2

### 2.1 SSH Connection
```bash
# Change key file permissions
chmod 400 your-key.pem

# SSH connection
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### 2.2 Update System
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git curl wget
```

### 2.3 Install Node.js and PM2
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PM2 globally
sudo npm install -g pm2
```

---

## 📥 Step 3: Deploy Bot Code

### 3.1 Clone Repository
```bash
# Create bot directory
mkdir -p ~/discord-bot
cd ~/discord-bot

# Clone code (replace with actual URL)
git clone https://github.com/your-username/discord-evm-faucet.git
cd discord-evm-faucet
```

### 3.2 Install Dependencies
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## ⚙️ Step 4: Configure Bot

### 4.1 Create .env file
```bash
nano .env
```

**Content of .env file:**
```env
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
```

### 4.2 Configure Discord Bot
1. Visit [Discord Developer Portal](https://discord.com/developers/applications)
2. Create new Application
3. Go to Bot section
4. Copy Bot Token and paste into .env file
5. Enable required permissions:
   - Send Messages
   - Use Slash Commands
   - Read Message History

---

## 🚀 Step 5: Run Bot

### 5.1 Test Bot
```bash
# Activate virtual environment
source venv/bin/activate

# Run bot
python3 bot.py
```

### 5.2 Setup PM2 Process Manager
PM2 provides better process management, monitoring, and auto-restart capabilities.

```bash
# Create PM2 ecosystem file
nano ecosystem.config.js
```

**Ecosystem file content:**
```javascript
module.exports = {
  apps: [{
    name: 'discord-faucet-bot',
    script: 'bot.py',
    interpreter: './venv/bin/python3',
    cwd: '/home/ubuntu/discord-bot/discord-evm-faucet',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production'
    },
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    log_file: './logs/combined.log',
    time: true
  }]
};
```

### 5.3 Start Bot with PM2
```bash
# Create logs directory
mkdir -p logs

# Start bot with PM2
pm2 start ecosystem.config.js

# Save PM2 configuration
pm2 save

# Setup PM2 to start on boot
pm2 startup
# Follow the instructions provided by PM2

# Check status
pm2 status

# View logs
pm2 logs discord-faucet-bot

# Monitor in real-time
pm2 monit
```

---

## 🔒 Step 6: Security

### 6.1 Update Security Groups
- Limit SSH access to your IP only
- Close unnecessary ports

### 6.2 Setup Firewall
```bash
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw status
```

### 6.3 Protect .env file
```bash
# Only owner can read .env file
chmod 600 .env

# Backup .env file
cp .env .env.backup
```

---

## 📊 Step 7: Monitoring and Maintenance

### 7.1 Monitor and Check Logs
```bash
# View real-time logs
pm2 logs discord-faucet-bot --lines 100

# View specific log files
tail -f logs/combined.log
tail -f logs/err.log
tail -f logs/out.log

# PM2 monitoring dashboard
pm2 monit

# Check process status
pm2 status
```

### 7.2 PM2 Management Commands
```bash
# Restart bot
pm2 restart discord-faucet-bot

# Stop bot
pm2 stop discord-faucet-bot

# Delete process
pm2 delete discord-faucet-bot

# Reload (zero-downtime restart)
pm2 reload discord-faucet-bot

# Show detailed info
pm2 show discord-faucet-bot
```

### 7.3 Update Bot
```bash
cd ~/discord-bot/discord-evm-faucet
git pull origin main
source venv/bin/activate
pip install -r requirements.txt

# Restart with PM2
pm2 restart discord-faucet-bot
```

---

## 🚨 Troubleshooting

### Bot cannot connect to Discord
- Check Discord Token in .env file
- Ensure bot has been invited to server
- Check internet connection

### Bot cannot send tokens
- Check HTTP_PROVIDER URL
- Check SENDER_ADDRESS and PRIVATE_KEY
- Check CHAIN_ID
- Check sender wallet balance

### Bot crashes or restarts continuously
- Check logs: `sudo journalctl -u discord-bot -f`
- Check for syntax errors in code
- Check file permissions

---

## 💰 Estimated Costs

- **EC2 t2.micro**: Free tier (first 12 months)
- **EC2 t3.small**: ~$15-20/month
- **Data Transfer**: ~$0.09/GB
- **Storage**: ~$0.10/GB/month

---

## 📝 Final Checklist

- [ ] EC2 instance has been created
- [ ] Bot code has been deployed
- [ ] .env file has been configured
- [ ] Discord Bot Token has been set
- [ ] Ethereum provider has been configured
- [ ] PM2 has been installed and configured
- [ ] Bot has been started with PM2 and is running stably
- [ ] Security groups have been configured
- [ ] Firewall has been enabled
- [ ] Bot has been tested with /faucet command

---

## 🔗 Useful Links

- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Infura Documentation](https://docs.infura.io/)
- [Web3.py Documentation](https://web3py.readthedocs.io/)

---

**Note**: Ensure the security of private key and Discord token. Never commit .env file to git repository.
