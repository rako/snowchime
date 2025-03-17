import discord
from discord import app_commands
from discord.ext import commands
from google.cloud import firestore
import os
import asyncio

# Firebase Admin初期化
db = firestore.Client()
channel_collection = db.collection('youtube_channels')

# Botの設定
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# チャンネル操作関数
def add_channel(channel_id):
    """Firestoreにチャンネルを追加する"""
    doc_ref = channel_collection.document(channel_id)
    doc_ref.set({
        'channel_id': channel_id,
        'added_at': firestore.SERVER_TIMESTAMP
    })
    return True

def delete_channel(channel_id):
    """Firestoreからチャンネルを削除する"""
    doc_ref = channel_collection.document(channel_id)
    doc_ref.delete()
    return True

def get_channel_list():
    """Firestoreからチャンネルリストを取得する"""
    channels = []
    docs = channel_collection.stream()
    for doc in docs:
        channels.append(doc.id)
    return channels

def check_channel_exists(channel_id):
    """チャンネルが既に存在するか確認する"""
    doc_ref = channel_collection.document(channel_id)
    return doc_ref.get().exists

# チャンネルリスト表示用のページング View
class ChannelListView(discord.ui.View):
    def __init__(self, channels, page=0, page_size=10):
        super().__init__(timeout=300)  # 5分のタイムアウト
        self.channels = channels
        self.page = page
        self.page_size = page_size
        self.total_pages = (len(channels) + page_size - 1) // page_size

        # 最初のページでは「前へ」ボタンを無効化
        self.previous_button.disabled = page == 0
        # 最後のページでは「次へ」ボタンを無効化
        self.next_button.disabled = page >= self.total_pages - 1

    async def create_embed(self):
        start_idx = self.page * self.page_size
        end_idx = min(start_idx + self.page_size, len(self.channels))
        
        embed = discord.Embed(
            title="登録チャンネル一覧",
            description=f"ページ {self.page + 1}/{self.total_pages}",
            color=discord.Color.blue()
        )
        
        for i, channel_id in enumerate(self.channels[start_idx:end_idx], start_idx + 1):
            embed.add_field(
                name=f"{i}. チャンネル", 
                value=f"https://www.youtube.com/channel/{channel_id}", 
                inline=False
            )
        
        return embed

    @discord.ui.button(label='前へ', style=discord.ButtonStyle.primary, custom_id='prev')
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page -= 1
        # ページを更新したので、ボタンの有効/無効状態も更新
        self.previous_button.disabled = self.page == 0
        self.next_button.disabled = False
        
        await interaction.response.edit_message(
            embed=await self.create_embed(), 
            view=self
        )

    @discord.ui.button(label='次へ', style=discord.ButtonStyle.primary, custom_id='next')
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page += 1
        # ページを更新したので、ボタンの有効/無効状態も更新
        self.previous_button.disabled = False
        self.next_button.disabled = self.page >= self.total_pages - 1
        
        await interaction.response.edit_message(
            embed=await self.create_embed(), 
            view=self
        )

    async def on_timeout(self):
        # タイムアウト時には全てのボタンを無効化
        self.previous_button.disabled = True
        self.next_button.disabled = True
        # メッセージを更新（存在する場合）
        if self.message:
            await self.message.edit(view=self)

@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="showlist", description="登録済みのYouTubeチャンネル一覧を表示します")
async def show_list(interaction: discord.Interaction):
    channels = get_channel_list()
    
    if not channels:
        await interaction.response.send_message("登録されているYouTubeチャンネルはありません。")
        return
    
    view = ChannelListView(channels)
    embed = await view.create_embed()
    
    await interaction.response.send_message(embed=embed, view=view)

@bot.tree.command(name="addchannel", description="YouTubeチャンネルを追加します")
@app_commands.describe(url="YouTubeチャンネルのURL")
async def add_channel_command(interaction: discord.Interaction, url: str):
    # URLからチャンネルIDを抽出する処理
    from util import validate_input
    channel_id = validate_input(url)
    
    if not channel_id:
        await interaction.response.send_message("有効なYouTubeチャンネルURLを指定してください。")
        return
    
    # チャンネルの存在確認
    from search import search
    if not search(channel_id):
        await interaction.response.send_message("そのようなチャンネルIDは存在しません。")
        return
    
    # チャンネルが既に登録されているか確認
    if check_channel_exists(channel_id):
        await interaction.response.send_message("このチャンネルは既に登録されています。")
        return
    
    # チャンネル追加
    add_channel(channel_id)
    
    await interaction.response.send_message(f"チャンネル `{channel_id}` を追加しました。")

@bot.tree.command(name="deletechannel", description="YouTubeチャンネルを削除します")
@app_commands.describe(channel_id="削除するチャンネルID")
async def delete_channel_command(interaction: discord.Interaction, channel_id: str):
    # チャンネルが存在するか確認
    if not check_channel_exists(channel_id):
        await interaction.response.send_message("指定されたチャンネルは登録されていません。")
        return
    
    # チャンネル削除
    delete_channel(channel_id)
    
    await interaction.response.send_message(f"チャンネル `{channel_id}` を削除しました。")

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        raise ValueError("DISCORD_TOKENが設定されていません")
    
    bot.run(TOKEN)