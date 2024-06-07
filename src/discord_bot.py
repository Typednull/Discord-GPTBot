import discord
from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv
import os
from .openai_interpreter import *  # Adjusted import path

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Setup intents
intents = Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user":
        return
    
    if 'Nexys' in message.content:
        command_details = interpret_command(message.content)
        action = command_details.get('action', 'unknown')
        if action == 'create_channel':
            await create_channel(message, command_details.get('parameters', {}))
        elif action == 'assign_role':
            await assign_role(message, command_details.get('parameters', {}))
        elif action == 'unknown':
            await message.channel.send("I didn't understand that command.")
        elif action == 'error':
            await message.channel.send(f"Error processing command: {command_details.get('message', 'Unknown error')}")

    await bot.process_commands(message)

async def create_channel(message, params):
    guild = message.guild
    channel_name = params.get('channel_name')
    category_name = params.get('category_name')
    category = discord.utils.get(guild.categories, name=category_name)
    if not category:
        await message.channel.send(f"Category '{category_name}' not found.")
        return
    channel = await guild.create_text_channel(channel_name, category=category)
    await message.channel.send(f"Channel '{channel_name}' created in category '{category_name}'.")

async def assign_role(message, params):
    guild = message.guild
    role_name = params.get('role_name')
    user_name = params.get('user')
    if not role_name or not user_name:
        await message.channel.send("Missing necessary parameters to assign a role.")
        return
    role = discord.utils.get(guild.roles, name=role_name)
    if not role:
        await message.channel.send(f"Role '{role_name}' not found.")
        return
    member = discord.utils.get(guild.members, name=user_name)
    if not member:
        await message.channel.send(f"User '{user_name}' not found.")
        return
    await member.add_roles(role)
    await message.channel.send(f"Role '{role_name}' assigned to {user_name}.")

bot.run(TOKEN)
