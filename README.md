# Faucet Bot for Ethereum-Based Networks

This repository contains a ready-to-use Discord bot designed to function as a **faucet** for distributing cryptocurrency on Ethereum-based networks. It's perfect for new networks or testnets where you need to distribute small amounts of tokens to users.

## Features
- Securely sends cryptocurrency to specified Ethereum addresses.
- Built-in rate limiting: Users can request tokens only once every 24 hours.
- Configurable for any Ethereum-based network by setting the appropriate `CHAIN_ID` and provider URL.
- Uses environment variables to securely manage sensitive information.

---

## Requirements
- **Python 3**: Make sure Python 3 is installed on your machine.
- **Ethereum Provider**: An Ethereum-compatible node provider (e.g., [Infura](https://infura.io/), Alchemy, or a self-hosted node).

---

## Setup Guide

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/faucet-bot.git
cd faucet-bot
```

### 2. Install Dependencies
Install the required Python libraries listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
1. Open the file `.env.example` and update the variables:
    - `HTTP_PROVIDER`: Your Ethereum provider URL.
    - `SENDER_ADDRESS`: The Ethereum address from which funds will be sent.
    - `PRIVATE_KEY`: The private key of the sender address.
    - `CHAIN_ID`: The chain ID of your network (e.g., `1` for Mainnet, `5` for Goerli, or a custom chain ID).
    - `DISCORD_TOKEN`: Your Discord bot token.

2. Rename the file to `.env`:
```bash
mv .env.example .env
```

---

## Run the Bot
Start the bot with:
```bash
python bot.py
```

---

## Notes
- The bot uses SQLite for managing user timestamps. The database file `database.db` will be created in the same directory.
- The bot is configured to sync Discord slash commands automatically.

---

## Example Command
Once the bot is running and added to a Discord server, users can request tokens using the `/faucet` command:
```
/faucet address:0xYourEthereumAddressHere
```

The bot will:
- Validate the request.
- Send 0.1 native tokens to the provided address.
- Respond with the transaction hash.

---

## Troubleshooting
If you encounter issues:
- Ensure Python 3 and the required libraries are installed.
- Verify your `.env` file is correctly configured.
- Check your Ethereum provider URL and private key for correctness.

---

## Contributions
Feel free to fork the repository and submit pull requests to improve the bot!

---

## License
This project is licensed under the MIT License.

