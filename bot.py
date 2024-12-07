import discord
from web3 import Web3
import time
import sqlite3
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get sensitive data from environment variables
HTTP_PROVIDER = os.getenv("HTTP_PROVIDER")
SENDER_ADDRESS = os.getenv("SENDER_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CHAIN_ID = int(os.getenv("CHAIN_ID", 1))  # Default to Mainnet if not specified
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Configure bot intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Connect to an Ethereum provider
provider = Web3.HTTPProvider(HTTP_PROVIDER)
web3 = Web3(provider)

# Transaction functions
def send_eth(recipient_address):
    sender_address_checksum = web3.to_checksum_address(SENDER_ADDRESS)
    recipient_address_checksum = web3.to_checksum_address(recipient_address)
    nonce = web3.eth.get_transaction_count(sender_address_checksum)
    ether_value = web3.to_wei(100, 'ether')
    gas_price = web3.eth.gas_price

    transaction = {
        'nonce': nonce,
        'to': recipient_address_checksum,
        'value': ether_value,
        'gas': 21000,
        'gasPrice': gas_price,
        'chainId': CHAIN_ID  # Use chain ID from environment
    }

    signed_transaction = web3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
    response = web3.eth.send_raw_transaction(signed_transaction.raw_transaction)
    transaction_hash = web3.to_hex(response)
    print(f"Transaction sent. Hash: {transaction_hash}")
    return transaction_hash

# SQLite database for timestamp management
def create_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (address TEXT PRIMARY KEY, timestamp INTEGER)")
    conn.commit()
    conn.close()

def register_timestamp(address, timestamp):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO users (address, timestamp) VALUES (?, ?)", (address, timestamp))
    conn.commit()
    conn.close()

def get_timestamp(address):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp FROM users WHERE address=?", (address,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

create_table()

# Event on_ready to sync commands
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands synced: {synced}")
    except Exception as e:
        print(f"Error during sync: {e}")

# Implementation of the /faucet command
@bot.tree.command(name="faucet", description="Request 100 coin to your EVM address.")
@app_commands.describe(address="The EVM address to send coin")
async def faucet(interaction: discord.Interaction, address: str):
    user_timestamp = get_timestamp(interaction.user.id)

    if (user_timestamp is None) or ((int(time.time()) - user_timestamp) > 86400):
        try:
            tx_hash = send_eth(address)
            register_timestamp(interaction.user.id, int(time.time()))
            await interaction.response.send_message(f"Sending 100 coin to address: {address}\nTx Hash: {tx_hash}")
        except Exception as e:
            await interaction.response.send_message(f"Error during transaction: {str(e)}", ephemeral=True)
    else:
        await interaction.response.send_message("You have already withdrawn in the last 24 hours. Please try again later.", ephemeral=True)

# Run the bot
bot.run(DISCORD_TOKEN)
