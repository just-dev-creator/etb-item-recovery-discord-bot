# EtB Item recovery discord bot
### Summary

The EtB Item recovery discord bot allows players of the Minecraft-Server Explore the Build to easily get their items back.
It was developed espacially for this usecase and can't be used for other purposes without modifying the script.

It was developed in Python using pymongo, discord-py-slash-commands and discordpy.

### Download and Install
```bash
# Download
git clone "https://github.com/just-dev-creator/etb-item-recovery-discord-bot" && cd etb-item-recovery-discord-bot

# Install libs and dependencies
pip install -r requirements.txt
```
Then, you need to set the following environment variables:
```dotenv
DISCORD_BOT_TOKEN=YOUR-BOT-TOKEN
MONGODB_CONNECTION_STRING=YOUR-CONNECTION-STRING
``` 
and set your server id(s) and team member id(s) in main.py. You can find the following snippet
in main.py:8 to main.py:11
```python
# Initialize team variable. SET YOUR TEAM MEMBERS HERE
team_members = ["YOUR TEAM MEMBER IDS HERE AS INT"]

# Initialize servers. SET YOUR SERVERS HERE
server_ids = ["YOUR SERVER IDS HERE AS INT"]
```

### Run
```bash
python main.py
```
### Upcoming changes
- [X] Make changes for easy use for everyone
- [X] Create ticket-like conversation