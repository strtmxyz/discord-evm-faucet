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
intents.message_content = True  # Required for prefix commands
bot = commands.Bot(command_prefix='!', intents=intents)

# Connect to an Ethereum provider
provider = Web3.HTTPProvider(HTTP_PROVIDER)
web3 = Web3(provider)

# Transaction functions
def send_eth(recipient_address):
    sender_address_checksum = web3.to_checksum_address(SENDER_ADDRESS)
    recipient_address_checksum = web3.to_checksum_address(recipient_address)
    nonce = web3.eth.get_transaction_count(sender_address_checksum)
    ether_value = web3.to_wei(0.1, 'ether')
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

# Event on_ready
@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user.name}")
    print(f"Bot ID: {bot.user.id}")
    print(f"Prefix: !")
    print(f"Commands: !faucet, !info")

# Info command
@bot.command(name="info", description="Show bot information and commands")
async def info_command(ctx):
    info_msg = "🤖 **Monad Faucet Bot**\n\n"
    info_msg += "**Commands:**\n"
    info_msg += "• `!faucet <address>` - Request 0.1 MONAD tokens\n"
    info_msg += "• `!info` - Show this information\n\n"
    info_msg += "**Example:** `!faucet 0x1234...`\n"
    info_msg += "**Rate Limit:** 1 request per 24 hours\n"
    info_msg += "**Network:** Monad Testnet (Chain ID: 10143)\n"
    info_msg += "**Amount:** 0.1 MONAD per request"
    
    await ctx.send(info_msg)

# Implementation of the !faucet command
@bot.command(name="faucet", description="Request 0.1 coin to your Monad address.")
async def faucet(ctx, address: str):
    try:
        # Check if address is provided
        if not address:
            await ctx.send("❌ Please provide a valid Monad address: `!faucet <address>`")
            return
        
        # Validate address format
        if not address.startswith('0x') or len(address) != 42:
            await ctx.send("❌ Invalid address format. Please provide a valid Monad address starting with 0x")
            return
            
        user_timestamp = get_timestamp(ctx.author.id)

        if (user_timestamp is None) or ((int(time.time()) - user_timestamp) > 86400):
            try:
                # Send transaction
                tx_hash = send_eth(address)
                register_timestamp(ctx.author.id, int(time.time()))
                
                # Create success message
                success_msg = f"✅ **Faucet Success!**\n"
                success_msg += f"**Amount:** 0.1 MONAD\n"
                success_msg += f"**Address:** `{address}`\n"
                success_msg += f"**Transaction Hash:** `{tx_hash}`\n"
                success_msg += f"**Next request:** Available in 24 hours"
                
                await ctx.send(success_msg)
                print(f"Faucet request successful for user {ctx.author.id} -> {address}")
                
            except Exception as e:
                error_msg = f"❌ **Transaction Error**\n"
                error_msg += f"**Error:** {str(e)}\n"
                error_msg += f"Please try again later or contact support."
                
                await ctx.send(error_msg)
                print(f"Faucet error for user {ctx.author.id}: {str(e)}")
        else:
            remaining_time = 86400 - (int(time.time()) - user_timestamp)
            hours = remaining_time // 3600
            minutes = (remaining_time % 3600) // 60
            
            cooldown_msg = f"⏰ **Cooldown Active**\n"
            cooldown_msg += f"You can request again in **{hours}h {minutes}m**\n"
            cooldown_msg += f"Rate limit: 1 request per 24 hours"
            
            await ctx.send(cooldown_msg)
            
    except Exception as e:
        print(f"Unexpected error in faucet command: {str(e)}")
        try:
            await ctx.send("❌ An unexpected error occurred. Please try again later.")
        except:
            print("Could not send error message to user")

# Run the bot
bot.run(DISCORD_TOKEN)
