import discord
from discord.ext import commands
import pymysql
import os
from dotenv import load_dotenv
from discord import app_commands
# Load environment variables from .env file
load_dotenv()
# Set up the bot with intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    print("bot is running")
    await bot.tree.sync()  
#task 1
    
@bot.event
async def on_member_join(member):


    welcome_channel=bot.get_channel(1205319065267347506)
    #message=print("welcome to the channel" + member.name)
    await welcome_channel.send("Welcome to the channel "+member.name)
    await member.send("Welcome to the channel "+member.name)


#task 2
  
# Function to fetch data from the database
def fetch_data(query):
    connection = pymysql.connect(host=os.getenv("HOST"), user=os.getenv("USER"), password=os.getenv("PASSWORD"), db=os.getenv("DB"),charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    return cursor.fetchall()

# Event handler to add message to user_words table
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    words = message.content.split()
    for word in words:
        query = f"INSERT INTO user_words (discord_id, word) VALUES ('{message.author.id}', '{word}')"
        fetch_data(query)
        
        
@bot.tree.command(name="word_status", description="common...")
async def word_status(interaction:discord.Interaction):
    query = "SELECT word, COUNT(*) AS count FROM user_words GROUP BY word ORDER BY count DESC LIMIT 10"
    result = fetch_data(query)
    print("Result \n",result)
    formatted_result = "\n".join(f"{item['word']}: {item['count']}" for item in result)
    print("\n",formatted_result)

    await interaction.response.send_message(formatted_result)


@bot.tree.command(name="user_status",description="user sepeciif...")
async def word_status(interaction:discord.Interaction,member:discord.Member):
    query = f"SELECT word, COUNT(*) AS count FROM user_words WHERE discord_id = '{member.id}' GROUP BY word ORDER BY count DESC LIMIT 10"
    result = fetch_data(query)
    print("Result \n",result)
# Construct formatted result string
    formatted_result = "\n".join(f"{item['word']}: {item['count']}" for item in result)

    print("\n",formatted_result)

    await interaction.response.send_message(formatted_result)
    

#task3

class SelectMenu(discord.ui.Select):
    def __init__(self):
        options=[discord.SelectOption(label="admin",value="2", description="Role of admin"),
                discord.SelectOption(label="leader",value="1", description="role of leader"),
                discord.SelectOption(label="sample_youtube_bot",value="3", description=" role of sample_youtube_bot")]
        super().__init__(placeholder="Select Roles", options=options,min_values=1,max_values=1)
        
    
    async def callback(self, interaction: discord.Interaction):
    # Check if the interaction is in a guild context
        if interaction.guild is None:
        # Handle the case when the command is used in a private message
            await interaction.response.send_message("This command can only be used in a server (guild).")
            return
        selected_role_index = int(self.values[0])
        roles = interaction.guild.roles
        print("Roles",roles,"\nSelected role",selected_role_index)
        if selected_role_index < len(roles):
            selected_role = roles[selected_role_index]
            selected_role_name = selected_role.name
            print("Selected role:", selected_role_name)  # Debugging statemen
            
            member = interaction.user
            await member.add_roles(selected_role)
            print(member.id)
            query = f"INSERT INTO user_role (discord_id, role) VALUES ('{member.id}', '{selected_role_name}')"
            result = fetch_data(query)
            await interaction.response.send_message(f"Assigned {selected_role_name} to {member.id}", delete_after=4)    

        else:
            print("Invalid role index:", selected_role_index)  # Debugging statement
            await interaction.response.send_message("Invalid role index selected. Please try again.", delete_after=4)

        
class Select(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(SelectMenu())


        
@bot.tree.command(name="select-role")
async def select(interaction: discord.Interaction):
    await interaction.response.send_message(content="select role",view=Select())

a=os.getenv("DISCORD_TOKEN")
bot.run(a)
# Command to get the 10 most used words

