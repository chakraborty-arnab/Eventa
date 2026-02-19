import asyncio
import os
import sys
from pathlib import Path

import discord
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))
from agent import process, process_image
from asr import transcribe

load_dotenv()

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if message.content:
        print(f"[{message.author}] text: {message.content}")
        reply = await asyncio.to_thread(process, message.content)
        await message.channel.send(reply)

    for attachment in message.attachments:
        content_type = attachment.content_type or ""
        if content_type.startswith("audio/") or attachment.filename.endswith((".ogg", ".mp3", ".wav", ".m4a", ".webm")):
            print(f"[{message.author}] audio: {attachment.filename} — transcribing...")
            audio_bytes = await attachment.read()
            text = await asyncio.to_thread(transcribe, audio_bytes, attachment.filename)
            print(f"[{message.author}] transcribed: {text}")
            reply = await asyncio.to_thread(process, text)
            await message.channel.send(reply)
        elif content_type.startswith("image/"):
            print(f"[{message.author}] image: {attachment.filename} — analysing...")
            reply = await asyncio.to_thread(process_image, attachment.url)
            await message.channel.send(reply)
        else:
            print(f"[{message.author}] attachment: {attachment.filename} ({content_type})")


client.run(DISCORD_TOKEN)
