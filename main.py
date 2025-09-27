import discord
import os
import google.generativeai as genai

# Botの基本的な設定
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# Gemini APIの設定
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash') 

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name}')
    print('Simple test bot is ready!')
    print('--------------------------------')

@bot.event
async def on_message(message):
    # 自分自身のメッセージは無視
    if message.author == bot.user:
        return

    # ボットがメンションされた時だけ反応
    if not bot.user.mentioned_in(message):
        return

    print(f"Received a mention from {message.author.name}")
    
    async with message.channel.typing():
        try:
            # Gemini APIを呼び出し
            response = await model.generate_content_async("自己紹介をしてください")
            
            # 応答を送信
            await message.channel.send(response.text)
            print("Successfully responded.")

        except Exception as e:
            # エラー内容をDiscordとログに出力
            error_message = f"An error occurred: {e}"
            print(error_message)
            await message.channel.send(error_message)

# Botを起動
token = os.getenv('DISCORD_BOT_TOKEN')
if token:
    bot.run(token)
else:
    print("Error: DISCORD_BOT_TOKEN is not set.")
