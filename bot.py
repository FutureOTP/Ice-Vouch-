import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Load config from environment or fallback file
TOKEN = os.getenv("TOKEN")
VOUCH_CHANNEL_ID = int(os.getenv("VOUCH_CHANNEL_ID", 0))
VOUCH_LOG_CHANNEL_ID = int(os.getenv("VOUCH_LOG_CHANNEL_ID", 0))
VOUCHES_FILE = "vouches.json"

# Ensure vouches.json exists
if not os.path.exists(VOUCHES_FILE):
    with open(VOUCHES_FILE, "w") as f:
        json.dump({}, f)

bot = commands.Bot(command_prefix="!", intents=intents)

def save_vouch(seller_id, reviewer_id, stars, review, categories, proof_url):
    with open(VOUCHES_FILE, "r+") as f:
        data = json.load(f)
        if seller_id not in data:
            data[seller_id] = {}
        data[seller_id][reviewer_id] = {
            "stars": stars,
            "review": review,
            "categories": categories,
            "proof_url": proof_url
        }
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

def get_stats(seller_id):
    with open(VOUCHES_FILE) as f:
        data = json.load(f)
    if seller_id not in data:
        return 0, 0
    total_stars = sum(entry["stars"] for entry in data[seller_id].values())
    count = len(data[seller_id])
    avg = round(total_stars / count, 2)
    return count, avg

@bot.event
async def on_ready():
    print(f"✅ Bot is ready as {bot.user}")

@bot.tree.command(name="vouch", description="Leave a vouch for a seller")
async def vouch(interaction: discord.Interaction, seller: discord.Member, stars: int, review: str, categories: str = "", proof: discord.Attachment = None):
    if seller.bot:
        await interaction.response.send_message("❌ You can't vouch for a bot.", ephemeral=True)
        return

    save_vouch(str(seller.id), str(interaction.user.id), stars, review, categories.split(","), proof.url if proof else None)
    count, avg = get_stats(str(seller.id))

    embed = discord.Embed(
        title=f"📩 New Vouch for {seller.display_name}",
        description=review,
        color=0x37b4a9
    )
    embed.add_field(name="⭐ Rating", value=f"{stars} Stars", inline=True)
    embed.add_field(name="✅ Categories", value=", ".join(categories.split(",")) if categories else "None", inline=True)
    embed.set_author(name=f"By {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
    embed.set_footer(text=f"Total Vouches: {count} • Avg Rating: {avg} ⭐", icon_url=seller.avatar.url if seller.avatar else None)
    if proof:
        embed.set_image(url=proof.url)

    vouch_channel = bot.get_channel(VOUCH_CHANNEL_ID)
    log_channel = bot.get_channel(VOUCH_LOG_CHANNEL_ID)
    if vouch_channel:
        await vouch_channel.send(embed=embed)
    if log_channel:
        await log_channel.send(f"📢 New vouch submitted by {interaction.user.mention} for {seller.mention}.", embed=embed)

    await interaction.response.send_message("✅ Your vouch was submitted!", ephemeral=True)

@bot.command()
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send("✅ Synced slash commands.")

bot.run(TOKEN)
