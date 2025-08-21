module.exports = {
  apps: [{
    name: 'discord-faucet-bot',
    script: 'bot.py',
    interpreter: './venv/bin/python3',
    cwd: process.cwd(),
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
    time: true,
    // PM2+ monitoring (optional)
    pmx: false,
    // Restart delay
    restart_delay: 1000,
    // Max restarts
    max_restarts: 10,
    // Min uptime before considering stable
    min_uptime: '10s'
  }]
};
